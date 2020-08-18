import enum
import typing

import numpy as np

from astropy.io import fits

class PaymentSolution(enum.Enum):
    AWSRequestPayer = 'aws-request-payer'

class CloudService(enum.Enum):
    S3 = 'amazon-web-services-static-storage-service'
    ObjectStorage = 'google-cloud-platform-object-storage'
    BlobStorage = 'azure-blob-storage'
    Spaces = 'digital-ocean-spaces'

class FITSHeader(typing.NamedTuple):
    offset: int
    length: int
    fits: fits.Header
