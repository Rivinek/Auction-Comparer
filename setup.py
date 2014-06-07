"""Setup file """
#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(
    name='allegro_nokaut',
    version='1.0',
    description='Application for comparison products from allegro.pl \
and nokaut.pl',
    author='Piotr Rogulski',
    author_email='piotr.rogulski@stxnext.pl',
    url='https://bitbucket.org/progulski/allegro_nokaut',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'nokaut = lib.nokaut_api:main',
            'allegro = lib.allegro_api:main'
        ]
    },
    install_requires=[
        'lxml',
        'beautifulsoap4',
        'PIL',
        'webtest',
        'nose',
        'nose-exclude',
        'nose-cov',
        'nosegae'
    ],
    test_suite='nose.collector'
)
