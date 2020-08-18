import os
import pytest

from astro_cloud_tests.pytest_constants import ENCODING
from astro_cloud_tests.pytest_utils import aws_credential_filepath, aws_credential_filepath__empty

def test__aws_auth():
    import requests

    from astro_cloud.auth.aws import AWSAuth
    test_file_filepath = '/tmp/test-file.txt'
    url = 'https://s3.us-east-1.amazonaws.com/datum-storage.org/test-file.txt'
    with open(test_file_filepath, 'wb') as stream:
        stream.write(b'testing AWSAuth on s3 services\n')

    response = requests.get(url, headers={})
    assert response.status_code == 403
    response = requests.get(url, headers={}, auth=AWSAuth())
    assert response.status_code in [404, 200]
    response = requests.post(url, headers={}, auth=AWSAuth(), data=open(test_file_filepath).read())
    assert response.status_code == 405
    response = requests.put(url, headers={}, auth=AWSAuth(), data=open(test_file_filepath).read())
    assert response.status_code == 200
    response = requests.get(url, headers={})
    assert response.status_code == 403
    response = requests.get(url, headers={}, auth=AWSAuth())
    assert response.status_code == 200
    response = requests.delete(url, headers={}, auth=AWSAuth())
    assert response.status_code == 204
    response = requests.get(url, headers={}, auth=AWSAuth())
    assert response.status_code == 404

def test__load_aws_context__credential_file(aws_credential_filepath, monkeypatch):
    from astro_cloud.auth import aws as auth_aws
    from astro_cloud.auth.aws import load_aws_auth_context, AWSService

    monkeypatch.setattr(auth_aws, 'AWS_CREDENTIAL_FILE_LOCATION', aws_credential_filepath)
    auth_context = load_aws_auth_context()
    assert auth_context.access_key == 'one'
    assert auth_context.secret_key == 'two'
    assert auth_context.region == 'three'
    assert auth_context.service == AWSService.S3

def test__load_aws_context__credential_file__second_profile(aws_credential_filepath, monkeypatch):
    from astro_cloud.auth import aws as auth_aws
    from astro_cloud.auth.aws import load_aws_auth_context, AWSService

    monkeypatch.setattr(auth_aws, 'AWS_CREDENTIAL_FILE_LOCATION', aws_credential_filepath)
    os.environ['AWS_PROFILE'] = 'second-profile'
    auth_context = load_aws_auth_context()
    assert auth_context.access_key == 'omega'
    assert auth_context.secret_key == 'psi'
    assert auth_context.region == 'chi'
    assert auth_context.service == AWSService.S3
    del os.environ['AWS_PROFILE']

def test__load_aws_context__none(aws_credential_filepath__empty, monkeypatch):
    from astro_cloud.auth import aws as auth_aws
    from astro_cloud.auth.aws import load_aws_auth_context, AWSService

    monkeypatch.setattr(auth_aws, 'AWS_CREDENTIAL_FILE_LOCATION', aws_credential_filepath__empty)
    auth_context = load_aws_auth_context()
    assert auth_context.access_key == None
    assert auth_context.secret_key == None
    assert auth_context.region == None
    assert auth_context.service == AWSService.S3

def test__load_aws_context__ENVVars(aws_credential_filepath__empty, monkeypatch):
    from astro_cloud.auth import aws as auth_aws
    from astro_cloud.auth.aws import load_aws_auth_context, AWSService

    monkeypatch.setattr(auth_aws, 'AWS_CREDENTIAL_FILE_LOCATION', aws_credential_filepath__empty)
    os.environ['AWS_ACCESS_KEY_ID'] = 'env-one'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'env-two'
    os.environ['AWS_DEFAULT_REGION'] = 'env-three'
    auth_context = load_aws_auth_context()
    assert auth_context.access_key == 'env-one'
    assert auth_context.secret_key == 'env-two'
    assert auth_context.region == 'env-three'
    assert auth_context.service == AWSService.S3
    del os.environ['AWS_ACCESS_KEY_ID']
    del os.environ['AWS_SECRET_ACCESS_KEY']
    del os.environ['AWS_DEFAULT_REGION']

def test__load_aws_context__ENVVars_with_credential_file(aws_credential_filepath, monkeypatch):
    from astro_cloud.auth import aws as auth_aws
    from astro_cloud.auth.aws import load_aws_auth_context, AWSService

    monkeypatch.setattr(auth_aws, 'AWS_CREDENTIAL_FILE_LOCATION', aws_credential_filepath)
    os.environ['AWS_ACCESS_KEY_ID'] = 'env-one'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'env-two'
    os.environ['AWS_DEFAULT_REGION'] = 'env-three'
    auth_context = load_aws_auth_context()
    assert auth_context.access_key == 'env-one'
    assert auth_context.secret_key == 'env-two'
    assert auth_context.region == 'env-three'
    assert auth_context.service == AWSService.S3
    del os.environ['AWS_ACCESS_KEY_ID']
    del os.environ['AWS_SECRET_ACCESS_KEY']
    del os.environ['AWS_DEFAULT_REGION']

def test__get_canonical_headers():
    from astro_cloud.auth import aws as auth_aws
    from astro_cloud.auth.aws import get_canonical_headers, AMZDATE_FORMAT

    from datetime import datetime

    timestamp = datetime.utcnow()
    host = 's3.us-east-1.amazonaws.com'
    expected_ordered_headers = 'host;x-amz-date'
    expected_ordered = '\n'.join([f'host:{host}', f'x-amz-date:{timestamp.strftime(AMZDATE_FORMAT)}'])
    expected_ordered = f'{expected_ordered}\n'
    ordered_headers, ordered = get_canonical_headers(timestamp, host)
    assert ordered_headers == expected_ordered_headers
    assert ordered == expected_ordered

def test__get_canonical_headers__payer_request():
    from astro_cloud.auth import aws as auth_aws
    from astro_cloud.auth.aws import get_canonical_headers, AMZDATE_FORMAT

    from datetime import datetime

    timestamp = datetime.utcnow()
    host = 's3.us-east-1.amazonaws.com'
    expected_ordered_headers = 'host;x-amz-date;x-amz-request-payer'
    expected_ordered = '\n'.join([
        f'host:{host}',
        f'x-amz-date:{timestamp.strftime(AMZDATE_FORMAT)}',
        'x-amz-request-payer:requester',
    ])
    expected_ordered = f'{expected_ordered}\n'
    ordered_headers, ordered = get_canonical_headers(timestamp, host, True)
    assert ordered_headers == expected_ordered_headers
    assert ordered == expected_ordered

def test__get_canonical_querystring():
    from astro_cloud.auth import aws as auth_aws
    from astro_cloud.auth.aws import get_canonical_querystring

    url = 'https://s3.us-east-1.amazonaws.com/datum-storage.org/test-file.txt'
    assert get_canonical_querystring(url) == ''

def test__get_payload_hash():
    import hashlib

    from astro_cloud.auth import aws as auth_aws
    from astro_cloud.auth.aws import get_payload_hash

    payload_body = b'aoeu'
    expected_payload = hashlib.sha256(payload_body).hexdigest()
    assert expected_payload == get_payload_hash(payload_body)

def test__sign__str_input():
    import hashlib
    import hmac

    from astro_cloud.auth import aws as auth_aws
    from astro_cloud.auth.aws import sign

    str_input_key = 'key'
    str_input_value = 'value'
    expected_value = hmac.new(
            str_input_key.encode(ENCODING),
            str_input_value.encode(ENCODING),
            hashlib.sha256).digest()

    assert expected_value == sign(str_input_key, str_input_value)

def test__sign__bytes_input():
    import hashlib
    import hmac

    from astro_cloud.auth.aws import sign

    bytes_input_key = b'key'
    str_input_value = 'value'
    expected_value = hmac.new(
        bytes_input_key,
        str_input_value.encode(ENCODING),
        hashlib.sha256).digest()

    assert expected_value == sign(bytes_input_key, str_input_value)

def test__get_signature_key(aws_credential_filepath):
    from astro_cloud.auth.aws import get_signature_key, DATESTAMP_FORMAT, sign, load_aws_auth_context
    
    from datetime import datetime
    key = 'key'
    timestamp = datetime.utcnow()
    region = load_aws_auth_context().region
    service = load_aws_auth_context().service
    kDate = sign(f'AWS4{key}', timestamp.strftime(DATESTAMP_FORMAT))
    kRegion = sign(kDate, region)
    kService = sign(kRegion, service)
    kSigning = sign(kService, 'aws4_request')

    assert kSigning == get_signature_key(key, timestamp, region, service)



