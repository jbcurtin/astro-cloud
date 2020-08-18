# astro-cloud

`astro-cloud` provides multiple API tiers to access large files from numerous Static Storage Provides. Initial release
of this software includes support for loading FITS headers from Amazon Web Services Static Storage Service or a service
with HTTP Range header implemented ( Caddy, Nginx, and Apache2 )

## Install

```
$ pip install -U astro-cloud
```

## Let's access FITS Headers from the Transiting Exoplanet Survey Satellite

Registry of Open Data on AWS provides a bucket called `stpubdata`. It contains data uploaded from the [Transiting
Exoplanet Survey Satellite](https://tess.mit.edu/). The type of data files we'll be working with in this tutoral are
about 44GB. If we downloaded or scanned the entire file, it'll cost about $1.05. Instead `astro-cloud` scans the headers
of the FITS files and calculates the data offsets, then jumps to the next header and downloads that until all headers
have been found

```
#!/usr/bin/env python

from astro_cloud.fits import load_headers, CloudService, PaymentSolution

url = 'https://s3.us-east-1.amazonaws.com/stpubdata/tess/public/mast/tess-s0022-4-4-cube.fits'
for header in load_headers(url, CloudService.S3, PaymentSolution.AWSRequestPayer):
    if header.fits.get('SIMPLE', False) is True:
        header_keys = [key for key in header.fits.keys()]
        print(f'Primary Header: {len(header_keys)}')

    else:
        xtension = header.fits['XTENSION']
        header_keys = [key for key in header.fits.keys()]
        print(f'{xtension} Header Key Length: {len(header_keys)}')

```

### Loading Headers from you're own Static Storage Service and not AWS, GCP, Azure, or Digital Ocean

```
#!/usr/bin/env python

from astro_cloud.fits.index.base import load_headers

url = 'https://github.com/jbcurtin/astro-cloud/blob/main/astro_cloud_test_data/tess2020061235921-s0022-4-4-0174-s_ffic.fits?raw=true'
for header in load_headers(url, auth=None):
    if header.fits.get('SIMPLE', False) is True:
        header_keys = [key for key in header.fits.keys()]
        print(f'Primary Header: {len(header_keys)}')

    else:
        xtension = header.fits['XTENSION']
        header_keys = [key for key in header.fits.keys()]
        print(f'{xtension} Header Key Length: {len(header_keys)}')
```

## Dedication to Performance

`astro-cloud` returns as many `astropy` datatypes as possible. Where ever possible everything is kept in memory and
never touches disk to help keep operations running quickly without much slowdown. There are also plans to implement
cluster computing frameworks such as DASK and Python `mulitprocessing` module.

## Maintenance

Please feel welcome to open a conversation with us on `astropy` slack channel and tell me how you'd like to use this package!

http://astropy-slack-invite.herokuapp.com/

We'll be in the `#fits` channel

### FITS Support

We're aware that there are many different ways of loading a FITS file. This package currently offers basic
support of the FITS format. As more issues are discovered, we'll add support for more types of FITS files. Please open
an issue and include a copy of the data you're testing against. We'll look into adding support for it

## File Format Specific API Tier

`astro-cloud` multiple API tiers provides access to perform complex operations on files being accessed from a Static Service Provider.
The highest tier being an implemantion of authentication layers for all major Static Storage Provides

* Amazon Web Services: Simple Storage Service ( AWS: S3 )
* Digital Ocean: Spaces ( Spaces by Digital Ocean ) [ planned support ]
* Google Compute Plateform: Object Storage ( GCP: Object Storage ) [ planned support ]
* Microsoft Azure: Blob Storage ( Azure: Blob Storage ) [ planned support ]

### Flexible Image Transport System Examples

#### AWS S3

Lets load headers from a FITS file on AWS S3 inside the bucket `stpubdata`

```
#!/usr/bin/env python

from astro_cloud.fits import load_headers, CloudService, PaymentSolution

url = 'https://s3.us-east-1.amazonaws.com/stpubdata/tess/public/mast/tess-s0022-4-4-cube.fits'
for header in load_headers(url, CloudService.S3, PaymentSolution.AWSRequestPayer):
    print(header.fits.get('XTENSION'))

```

### Low Level Cloud API

Of the multiple API tiers, the lowest tier is Low Level Cloud API. Downloading a whole FITS file from a Static Storage
Provider is possible by using `psf/requests` or passing an `AuthBase` into a different `load_headers`. Underneath everything
`astro-cloud` uses the HTTP Header `Range` to request partial content from a provider or service

```
#!/usr/bin/env python
import os
import requests

from astro_cloud.auth.aws import AWSAuth

from astropy.io import fits

CHUNK_SIZE = 1024
ENCODING = 'utf-8'
url = 'https://s3.amazonaws.com/datum-storage.org/fits-files/502nmos.fits'
filename = os.path.basename(url)
filepath = f'/tmp/{filename}'

response = requests.get(url, auth=AWSAuth(request_payer=True), headers={
    'Range': 'bytes=0-2779',
})
assert response.status_code == 206

primary_header = fits.Header.fromstring(response.content.decode(ENCODING))
assert primary_header['SIMPLE'] is True

# Save the file to the file-system and load it with `fits.io`
streaming_response = requests.get(url, auth=AWSAuth(request_payer=True), headers={}, stream=True)
assert streaming_response.status_code == 200
with open(filepath, 'wb') as file_stream:
    for part in streaming_response.iter_content(CHUNK_SIZE):
        file_stream.write(part)

fits_file = fits.open(filepath)
print(fits_file.info())
```
