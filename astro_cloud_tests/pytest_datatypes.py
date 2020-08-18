import typing

from astropy.io import fits
from astropy.io.fits.hdu.hdulist import HDUList

class FITSTestFile(typing.NamedTuple):
    name: str
    url: str  # Source path where the data can currently be found online
    fits: typing.List[fits.Header]
    cache_path: str  # Path to store the data within astro_cloud's cloud to speed up test coverage
