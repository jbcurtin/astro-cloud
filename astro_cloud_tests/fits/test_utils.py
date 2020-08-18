from astro_cloud_tests.pytest_utils import fits_files

def test__as_np_dtype__uint8():
    import numpy as np

    from astro_cloud.fits.utils import as_np_dtype

    assert as_np_dtype(8) == np.dtype(np.uint8)

def test__as_np_dtype__uint16():
    import numpy as np

    from astro_cloud.fits.utils import as_np_dtype

    assert as_np_dtype(16) == np.dtype(np.uint16)

def test__as_np_dtype__uint32():
    import numpy as np

    from astro_cloud.fits.utils import as_np_dtype

    assert as_np_dtype(32) == np.dtype(np.uint32)

def test__as_np_dtype__float32():
    import numpy as np

    from astro_cloud.fits.utils import as_np_dtype

    assert as_np_dtype(-32) == np.dtype(np.float32)

def test__as_np_dtype__float64():
    import numpy as np

    from astro_cloud.fits.utils import as_np_dtype

    assert as_np_dtype(-64) == np.dtype(np.float64)

def test__find_next_header_offset__primary_header():
    from astro_cloud.fits.datatypes import FITSHeader
    from astro_cloud.fits.utils import find_next_header_offset

def test__find_next_header_offset__table(fits_files):
    from astro_cloud.fits.datatypes import FITSHeader
    from astro_cloud.fits.utils import find_next_header_offset

    # import pdb; pdb.set_trace()
    # import sys; sys.exit(1)

