import typing

from astro_cloud.fits.datatypes import CloudService, FITSHeader, PaymentSolution
from astro_cloud.fits.index import aws, gcp, azure, digital_ocean

def load_headers(url: str, service: CloudService, payment_solution: PaymentSolution=None) -> typing.List[FITSHeader]:
    if service is CloudService.S3:
        return aws.load_headers(url, payment_solution)

    elif service is CloudService.ObjectStorage:
        return gcp.load_headers(url, payment_solution)

    elif service is CloudService.BlobStorage:
        return azure.load_headers(url, payment_solution)

    elif service is CloudService.Spaces:
        return digital_ocean.load_headers(url, payment_solution)

    else:
        raise NotImplementedError(f'Cloud Service[{cloud_service}] not implemented')


