#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from subprocess import Popen, PIPE
from distutils import spawn
import platform
import codecs
from setuptools import setup, find_packages


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


# Add your dependencies in requirements.txt
# Note: you can add test-specific requirements in tox.ini
requirements = []
with open('requirements.txt') as f:
    for line in f:
        stripped = line.split("#")[0].strip()
        if len(stripped) > 0:
            requirements.append(stripped)

setup(
    name='napari-yapic-prediction',
    version='0.2.0',
    author='Duway Nicolas Lesmes Leon, Pranjal Dhole',
    author_email=('dlesmesleon@hotmail.com, dhole.pranjal@gmail.com'),
    license='GNU GPL v3.0',
    url='https://github.com/yapic/napari-yapic-prediction',
    description='napari widget that performs image segmentation with yapic model in the napari window. Install TENSORFLOW to use this plugin.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=requirements,
    setup_requires=['setuptools_scm'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Framework :: napari',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    entry_points={
        "napari.manifest": [
            "napari-yapic-prediction = napari_yapic_prediction:napari.yaml",
        ],
    },
    package_data={"napari_yapic_prediction": ["napari.yaml"]},
)
