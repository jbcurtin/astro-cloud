import os

ENCODING = 'utf-8'
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PYTEST_DATA_DIR = f'{PROJECT_DIR}/astro_cloud_test_data'
PYTEST_TEMPLATE_DIR = f'{PROJECT_DIR}/astro_cloud_test_templates'
# We'll use AWS for datum storage right now
DATUM_STORAGE_BASE_URL = 'https://s3.us-east-1.amazonaws.com/datum-storage.org'
DATUM_STORAGE_BASE_URL__FITS = f'{DATUM_STORAGE_BASE_URL}/fits-files'
