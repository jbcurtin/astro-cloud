import typing

from astro_cloud.auth.azure import AzureAuth
from astro_cloud.fits.datatypes import FITSHeader, PaymentSolution
from astro_cloud.fits.index import base as index_base

def load_headers(url: str, payment_solution: PaymentSolution) -> typing.List[FITSHeader]:
    if payment_solution is None:
        return index_base.load_headers(url, auth=AzureAuth())

    raise NotImplementedError(f'Unsupported Payment Solution[{payment_solution}]')
