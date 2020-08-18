# astro-cloud

`astro-cloud` provides three API tiers to access large files from numerous Static Storage Provides. Initial release
of this software includes support for loading FITS headers from Amazon Web Services Static Storage Service or an service
with HTTP loaded onto it

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
for header in load_headers(url, CloudService.AWS, PaymentSolution.AWSRequestPayer):
    print(header.__class__)
    if header.fits.get('SIMPLE', False) is True:
        print('Primary Header: {header}')

    else:
        xtension = header.fits['XTENSION']
        print('{xtension} Header: {header}')

```

## Dedication to Performance

`astro-cloud` returns as many `astropy` datatypes as possible. Where ever possible everything is kept in memory and
never touches disk to help keep operations running quickly without much slowdown. There are also plans to implement
cluster computing frameworks such as DASK and Python `mulitprocessing` module.

## Maintenance

Please feel welcome to open a conversation with me on `astropy` slack channel and tell me how you'd like to use this package!

http://astropy-slack-invite.herokuapp.com/

I'll be in the `#fits` channel


## File Format Specific API Tier

`astro-cloud` three API tiers provides access to perform complex operations on files being accessed from a Static Service Provider.
The highest being an implemantion of authentication layers for all major Static Storage Provides.

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
for header in load_headers(url, CloudService.AWS, PaymentSolution.AWSRequestPayer):
    print(header.fits.get('XTENSION'))

```

#### Low Level Cloud API

Downloading a whole FITS file from a Static Storage Provider is possible to. `astro-cloud` uses the HTTP Header `Range`
to request partial content from a provider or service. We can bypass that by using `psf/requests` instead of `load_headers`.

```
import requests

from astro_cloud.auth.aws import AWSAuth

from astropy.io import fits

CHUNK_SIZE = 1024
ENCODING = 'utf-8'
url = 'https://s3.us-east-1.amazonaws.com/datum-storage.org/fits-files/502nmos.fits'
filename = os.path.basename(url)
filepath = f'/tmp/{filename}'

response = requests.get(url, auth=AWSAuth(request_payer=True), headers={
    'Range': '0-2779',
})
assert response.status_code in [200, 204]

primary_header = fits.Header.from_string(response.content.decode(ENCODING))
print(primary_header)


# Save the file to the file-system and load it with `fits.io`
streaming_response = request.get(url, auth=AWSAuth(request_payer=True), headers={}, stream=True)
with open(filepath, 'wb') as file_stream:
    for part in streaming_response.iter_content(CHUNK_SIZE):
        file_stream.write(part)

fits_file = fits.open(filepath)
print(fits_file)

```
