#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# with open(path.join(here, 'VERSION')) as version_file:
#   version = version_file.read().strip()
long_description = "Package with addons for datajoint-python."


setup(
    name='djaddon',
    version='0.1.0.dev1',
    description="Addons to datajoint-python",
    long_description=long_description,
    author='Fabian Sinz',
    author_email='sinz@bcm.eud',
    license="GNU LGPL",
    url='https://github.com/datajoint/datajoint-addons',
    keywords='database organization',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['datajoint', 'gitpython'],
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: LGPL License',
        'Topic :: Database :: Front-Ends',
    ],
)
