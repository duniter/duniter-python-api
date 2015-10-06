from setuptools import setup, find_packages
import ucoinpy

setup(
    name='ucoinpy',

    version=ucoinpy.__version__,

    packages=find_packages(),

    author="Caner & inso",

    author_email="insomniak.fr@gmail.com",

    description="A python implementation of [uCoin](https://github.com/ucoin-io/ucoin) API",

    long_description=open('README.md').read(),
    
    # Active la prise en compte du fichier MANIFEST.in
    include_package_data=True,
    url='https://github.com/ucoin-io/ucoin-python-api',
    test_suite="_ucoinpy_test",

    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        "Topic :: Communications",
    ],
 

)