def test__github():
    from astro_cloud.fits.index.base import load_headers

    url = 'https://github.com/jbcurtin/astro-cloud/blob/main/astro_cloud_test_data/502nmos.fits?raw=true'

    for header in load_headers(url, auth=None):
        if header.fits.get('SIMPLE', False) is True:
            header_keys = [key for key in header.fits.keys()]
            print(f'Primary Header: {len(header_keys)}')
    
        else:
            xtension = header.fits['XTENSION']
            header_keys = [key for key in header.fits.keys()]
            print(f'{xtension} Header Key Length: {len(header_keys)}')

