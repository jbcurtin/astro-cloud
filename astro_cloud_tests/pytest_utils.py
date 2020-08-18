import os
import json
import pytest
import requests
import typing

from astropy.io import fits

from astro_cloud_tests.pytest_constants import ENCODING, PYTEST_DATA_DIR, DATUM_STORAGE_BASE_URL__FITS, \
    PYTEST_TEMPLATE_DIR
from astro_cloud_tests.pytest_datatypes import FITSTestFile

def load_template(template_name: str) -> str:
    template_path = os.path.join(PYTEST_TEMPLATE_DIR, template_name)
    if not os.path.exists(template_path):
        raise IOError(f'Unable to find template[{template_name}]')

    with open(template_path, 'rb') as stream:
        return stream.read().decode(ENCODING)

def json_file_to_fits_headers(filepath: str) -> typing.List[fits.Header]:
    headers = []
    with open(filepath, 'rb') as stream:
        for entry in json.loads(stream.read()):
            header = fits.Header()
            for key, value in entry.items():
                header[key] = value

            headers.append(header)

    return headers

@pytest.fixture
def fits_files():
    records: typing.List[FITSTestFile] = []
    # Messier 17
    #  Primary HDU
    #  Table HDU
    name = 'messier-17'
    url = None
    fits_headers = [fits.open(os.path.join(PYTEST_DATA_DIR, '502nmos.fits'))]
    cache_url = f'{DATUM_STORAGE_BASE_URL__FITS}/502nmos.fits'
    records.append(FITSTestFile(name, url, fits_headers, cache_url))

    # Tess DataCube AWS
    name = 'tess-s0022'
    url = 'https://s3.us-east-1.amazonaws.com/stpubdata/tess/public/mast/tess-s0022-4-4-cube.fits'
    fits_headers = json_file_to_fits_headers(f'{PYTEST_DATA_DIR}/tess-s0022-4-4-cube-headers.json')
    cache_url = None
    records.append(FITSTestFile(name, url, fits_headers, cache_url))
    return {test_file.name: test_file for test_file in records}

@pytest.fixture
def aws_credential_filepath():
    template = load_template('aws/credentials-file.txt')

    filepath = '/tmp/aws-credentials'
    with open(filepath, 'wb') as stream:
        stream.write(template.encode(ENCODING))

    return filepath

@pytest.fixture
def aws_credential_filepath__empty():
    filepath = '/tmp/aws-credentials-none'
    if os.path.exists(filepath):
        os.remove(filepath)

    return filepath
