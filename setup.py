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

def check_for_gpu():
    if platform.system() == 'Windows':
        nvidia_smi = spawn.find_executable('nvidia-smi')
        if nvidia_smi is None:
            nvidia_smi = f"{os.environ['systemdrive']}\\Program Files\\NVIDIA Corporation\\NVSMI\\nvidia-smi.exe"
    else:
        nvidia_smi = 'nvidia-smi'
    
    try:
        with Popen([nvidia_smi, '-L'], stdout=PIPE) as proc:
            isGPU = bool(proc.stdout.read())
    except:
        isGPU = False
    return isGPU

# Add your dependencies in requirements.txt
# Note: you can add test-specific requirements in tox.ini
requirements = []
with open('requirements.txt') as f:
    for line in f:
        stripped = line.split("#")[0].strip()
        if len(stripped) > 0:
            requirements.append(stripped)

USE_GPU_VERSION = check_for_gpu()
if USE_GPU_VERSION:
    requirements.append('tensorflow-gpu==2.4.2')
else:
    requirements.append('tensorflow==2.4.2')

# https://github.com/pypa/setuptools_scm
# use_scm = {"write_to": "napari_yapic_prediction/_version.py"}

def local_scheme(version):
    return ""

setup(
    name='napari-yapic-prediction',
    author='Duway Nicolas Lesmes Leon',
    author_email='dlesmesleon@hotmail.com',
    license='GNU GPL v3.0',
    url='https://github.com/yapic/napari-yapic-prediction',
    description='Napari widget plugin to perform yapic model segmentation prediction in the napari window',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=requirements,
    use_scm_version={"local_scheme": local_scheme},
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
        'napari.plugin': [
            'napari-yapic-prediction = napari_yapic_prediction',
        ],
    },
)
