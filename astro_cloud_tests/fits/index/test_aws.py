import json
import pytest

from astro_cloud_tests.pytest_utils import fits_files

def test__load_headers__aws__request_payer(fits_files):
    from astro_cloud.fits.datatypes import PaymentSolution
    from astro_cloud.fits.index.aws import load_headers

    fits_headers = load_headers(fits_files['tess-s0022'].url, PaymentSolution.AWSRequestPayer)
    for header_idx, local_header in enumerate(fits_files['tess-s0022'].fits):
        for key, value in local_header.items():
            assert value == fits_headers[header_idx].fits[key]

