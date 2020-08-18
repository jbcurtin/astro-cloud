import os
import sys

from setuptools import find_packages, setup

# Always reference code-origin
# https://github.com/django/django/blob/master/setup.py#L7

PACKAGE_NAME = 'astro-cloud'
CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 7)
ENCODING = 'utf-8'

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version of astro-cloud requires Python {}.{}, but you're trying to
install it on Python {}.{}.
This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have pip >= 9.0 and setuptools >= 24.2, then try again:
    $ pip install -U pip setuptools
    $ pip install -U astro-cloud
This will install the latest version of astro-cloud which works on your
version of Python
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)


EXCLUDE_FROM_PACKAGES = []
version = '0.0.1'

INSTALL_REQUIRES = [
    'requests==2.24.0',
    'astropy==4.0.1.post1'
]
description = 'A utility to make accessing static content in the cloud, efficient'

def read(fname):
  with open(os.path.join(os.path.dirname(__file__), fname)) as f:
    return f.read()

setup(
    name='astro-cloud',
    version=version,
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    url='https://github.com/jbcurtin/astro-cloud',
    author="Joseph Curtin <42@jbcurtin.io",
    author_email='astro-cloud@jbcurtin.io',
    description=description,
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    scripts=[],
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': []
    },
    zip_safe=False,
    classifiers=[
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3 :: Only',
  ],
  project_urls={}
)

