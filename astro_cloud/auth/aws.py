import collections
import configparser
import enum
import hashlib
import hmac
import logging
import os
import typing

from datetime import datetime
from requests.auth import AuthBase
from urllib.parse import quote, urlparse
from requests.models import PreparedRequest

from astro_cloud.constants import ENCODING

PWN: typing.TypeVar = typing.TypeVar('PWN')

AMZDATE_FORMAT: str = '%Y%m%dT%H%M%SZ'
DATESTAMP_FORMAT: str = '%Y%m%d'
QUOTE_SAFE_CHARS: str = '/-_.~'

AWS_CREDENTIAL_FILE_LOCATION = os.path.expanduser('~/.aws/credentials')

logger = logging.getLogger(__file__)

class AWSService(typing.NamedTuple):
    S3 = 's3'  # simple-storage-server
    EC2 = 'ec2'  # elastic-compute-cloud

class AWSAuthContext(typing.NamedTuple):
    access_key: str
    secret_key: str
    region: str
    service: AWSService

def load_aws_auth_context() -> AWSAuthContext:
    '''
    Loads AWS Credentials in a simular fashion to as boto3. If a credentials file is found, it'll take from that. If
      ENV-Vars are found, they're overwrite corrolating entries from the credentials

    https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html
    '''
    aws_profile = os.environ.get('AWS_PROFILE', 'default')
    if os.path.exists(AWS_CREDENTIAL_FILE_LOCATION):
        parser = configparser.ConfigParser()
        with open(AWS_CREDENTIAL_FILE_LOCATION, 'rb') as stream:
            parser.read_string(stream.read().decode(ENCODING))

        access_key = parser.get(aws_profile, 'aws_access_key_id')
        secret_key = parser.get(aws_profile, 'aws_secret_access_key')
        region = parser.get(aws_profile, 'region')

    else:
        logger.info('Unable to locate AWS Credential file')
        access_key = None
        secret_key = None
        region = None

    access_key = os.environ.get('AWS_ACCESS_KEY_ID', access_key)
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY', secret_key)
    region = os.environ.get('AWS_DEFAULT_REGION', region)
    return AWSAuthContext(access_key, secret_key, region, AWSService.S3)

def get_canonical_headers(timestamp: datetime, host: str, request_payer: bool = False) -> str:
    '''
    timestamp is a datetime object to be used in other functions, later to be signed into the signature
    host is a string representing the AWSService URL. For s3, this could be: http://s3.us-east-1.amazonaws.com/datum/
    '''
    headers: typing.Dict[str, str] = {
        'host': host,
        'x-amz-date': timestamp.strftime(AMZDATE_FORMAT)
    }
    if request_payer:
        headers['x-amz-request-payer'] = 'requester'

    ordered_headers = []
    ordered = []
    for key in sorted(headers.keys()):
        ordered_headers.append(key)
        ordered.append(f'{key}:{headers[key]}')

    ordered_headers = ';'.join(ordered_headers)
    ordered = '\n'.join(ordered)
    return ordered_headers, f'{ordered}\n'

def get_canonical_url(url: str) -> str:
    url_parts = urlparse(url)
    if url_parts.path:
        return quote(url_parts.path, safe=QUOTE_SAFE_CHARS)

    return quote('/', safe=QUOTE_SAFE_CHARS)

def get_canonical_querystring(url: str) -> str:
    url_parts = urlparse(url)
    if url_parts.query == '':
        return ''

    # https://github.com/DavidMuller/aws-requests-auth/blob/969bc643f8386bc796c30d71e78c59af7f82f6b2/aws_requests_auth/aws_auth.py#L202
    raise NotImplementedError
    sorted_querystring: str = sorted(url_parts.query.split('&'))
    import pdb; pdb.set_trace()
    pass

def get_payload_hash(payload_body: bytes = None) -> str:
    payload_body = payload_body or bytes()
    try:
        payload_body = payload_body.encode('utf-8')
    except (AttributeError, UnicodeDecodeError):
        pass

    return hashlib.sha256(payload_body).hexdigest()

def sign(key: typing.Union[str, bytes], value: str) -> bytes:
    if isinstance(key, str):
        key: bytes = key.encode(ENCODING)

    return hmac.new(key, value.encode(ENCODING), hashlib.sha256).digest()

def get_signature_key(key: str, timestamp: datetime, region: str, service: AWSService) -> bytes:
    kDate: str = sign(f'AWS4{key}', timestamp.strftime(DATESTAMP_FORMAT))
    kRegion: str = sign(kDate, region)
    kService: str = sign(kRegion, service)
    kSigning: str = sign(kService, 'aws4_request')
    return kSigning

class AWSAuth(AuthBase):
    _request_payer: bool
    def __init__(self: PWN, request_payer: bool=False) -> None:
        self._request_payer = request_payer

    def __call__(self: PWN, request: 'requests.Request') -> 'requests.Request':
        timestamp = datetime.utcnow()
        aws_context = load_aws_auth_context()
        request_host: str = urlparse(request.url).netloc

        payload_hash = get_payload_hash(request.body)
        signed_headers, canonical_headers = get_canonical_headers(timestamp, request_host, self._request_payer)
        canonical_request = '\n'.join([
            request.method,
            get_canonical_url(request.url),
            get_canonical_querystring(request.url),
            canonical_headers,
            signed_headers,
            payload_hash,
        ])

        algorithm: str = 'AWS4-HMAC-SHA256'
        credential_scope: str = f'{timestamp.strftime(DATESTAMP_FORMAT)}/{aws_context.region}/{aws_context.service}/aws4_request'
        hashed_request: str = hashlib.sha256(canonical_request.encode(ENCODING)).hexdigest()
        string_to_sign = f'{algorithm}\n{timestamp.strftime(AMZDATE_FORMAT)}\n{credential_scope}\n{hashed_request}'
        signing_key = get_signature_key(aws_context.secret_key, timestamp, aws_context.region, aws_context.service)
        signature = hmac.new(
            signing_key,
            string_to_sign.encode(ENCODING),
            hashlib.sha256).hexdigest()

        auth_header = f'{algorithm} Credential={aws_context.access_key}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}'
        request.headers['Authorization'] = auth_header
        request.headers['x-amz-date'] = timestamp.strftime('%Y%m%dT%H%M%SZ')
        request.headers['x-amz-content-sha256'] = payload_hash
        if self._request_payer:
            request.headers['x-amz-request-payer'] = 'requester'

        return request
