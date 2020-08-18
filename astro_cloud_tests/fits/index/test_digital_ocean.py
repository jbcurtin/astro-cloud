from astro_cloud_tests.pytest_utils import fits_files

def test__load_headers(fits_files):
    from astro_cloud.fits.index.digital_ocean import load_headers
