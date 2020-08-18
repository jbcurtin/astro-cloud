import numpy as np

from astro_cloud.fits.constants import BLOCK_SIZE
from astro_cloud.fits.datatypes import FITSHeader

def as_np_dtype(bitpix: int) -> np.dtype:
    '''
    Image XTENSION has a BITPIX header that represents a datatype. This function takes that header and converts
        it to np.dtype
    '''
    if bitpix == 8:
        return np.dtype(np.uint8)

    elif bitpix == 16:
        return np.dtype(np.uint16)

    elif bitpix == 32:
        return np.dtype(np.uint32)

    elif bitpix == -32:
        return np.dtype(np.float32)

    elif bitpix == -64:
        return np.dtype(np.float64)

    raise NotImplementedError(f'BITPIX[{bitpix}] not implemented')

def find_next_header_offset(header: FITSHeader) -> int:
    '''
    Each FITS XTENSION has enough information to predict the next location of the next XTENSION header. Here we'll
        take in the offset and length and return a new offset which includes the data length difference
    '''
    if header.fits.get('SIMPLE', False) is True:
        # Primary Header
        return header.offset + header.length

    elif header.fits.get('XTENSION', None) in ['IMAGE']:
        # https://ui.adsabs.harvard.edu/abs/1994A%26AS..105...53P/abstract
        # http://articles.adsabs.harvard.edu/pdf/1994A%26AS..105...53P
        B: int = as_np_dtype(header.fits['BITPIX']).itemsize
        G: int = header.fits['GCOUNT']
        P: int = header.fits['PCOUNT']
        N: typing.List[int] = [header.fits[f'NAXIS{idx}'] for idx in range(1, header.fits['NAXIS'] + 1)]
        S: int = B * G * (P + np.prod(N))
        return int(S / BLOCK_SIZE) * BLOCK_SIZE + header.offset + header.length

    elif header.fits.get('XTENSION', None) in ['BINTABLE']:
        # NAXIS1 = number of bytes per row
        # NAXIS2 = number of rows in the table
        return header.fits['NAXIS1'] * header.fits['NAXIS2'] + header.offset + header.length

    elif header.fits.get('XTENSION', None) in ['TABLE']:
        raise NotImplementedError('TABLE')

    else:
        # import pdb; pdb.set_trace()
        pass

    raise NotImplementedError

