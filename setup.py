"""Install vb2Py

Much of the following code is copied from the vb2py.PythonCard installation script
because the original setup.py would copy files to all sorts of weird location
on Linux.

You must run this to create the setup distribution from the site-packages!

"""

import glob
import os
import setuptools
import vb2py.projectconverter
import vb2py.utils


grammar_files = glob.glob(vb2py.utils.relativePath('grammars', '*.*'))
doc_files = glob.glob(vb2py.utils.relativePath('doc', '*.*'))

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='vb2Py',
    version=vb2py.projectconverter.__version__,
    description="Visual Basic to Python Converter",
    author="Paul Paterson",
    author_email="paulpaterson@users.sourceforge.net",
    url="http://vb2py.sourceforge.net",
    packages=setuptools.find_packages(),
    long_description=long_description,
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    ],
    install_requires=[
        'mako',
        'chardet',
        'flask',
        'flask_cors',
        'simpleparse',
        'docutils',
    ],
    package_data={
        'vb2py': ['vb2py.ini'],
        'vb2py.grammars': grammar_files,
        'vb2py.doc': doc_files,
    },
    python_requires='>=3.6',
)
