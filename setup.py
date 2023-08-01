#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

import io
import os
import sys
from shutil import rmtree
import re
from setuptools import find_packages, setup, Command
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel


def get_property(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(project + '/__init__.py').read())
    return result.group(1)
   
        
# Package meta-data.
NAME = 'pygmtools'
DESCRIPTION = 'pygmtools provides graph matching solvers in Python API and supports numpy and pytorch backends. ' \
              'pygmtools also provides dataset API for standard graph matching benchmarks.'
URL = 'https://pygmtools.readthedocs.io/'
AUTHOR = get_property('__author__', NAME)
VERSION = get_property('__version__', NAME)
REQUIRED = [
     'requests>=2.25.1', 'scipy>=1.4.1', 'Pillow>=7.2.0', 'numpy>=1.18.5', 'easydict>=1.7', 'appdirs>=1.4.4', 'tqdm>=4.64.1','wget>=3.2'
]
EXTRAS = {}

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION
 
    
class CustomBdistWheelCommand(_bdist_wheel):
    def run(self):
        ori_dir = os.getcwd()
        os.chdir(os.path.join(NAME,'astar'))
        os.system("python get_astar.py")
        os.chdir(ori_dir)
        self.root_is_pure = False
        self.py_limited_api = False
        super().run()

        
class UploadCommand(Command):
    """Support setup.py upload."""
    def run(self):
        os.system('twine upload dist/*')
        sys.exit()


setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    package_data={NAME: ['*.pyd','*.so'], "tests": ["test_a_star/*"]},
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='Mulan PSL v2',
    python_requires='>=3.7',
    classifiers=[
        'License :: OSI Approved :: Mulan Permissive Software License v2 (MulanPSL-2.0)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Environment :: GPU :: NVIDIA CUDA',
        'Environment :: Console',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
        'bdist_wheel': CustomBdistWheelCommand,
    },
)
