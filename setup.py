from setuptools import setup, find_packages

setup(
    name='duniter-mirage',

    version="0.1.4",

    packages=find_packages(),

    author="inso",

    author_email="insomniak.fr@gmail.com",

    description="A python mock server of [duniter](https://github.com/duniter/duniter) API",

    long_description=open('README.md').read(),

    # Active la prise en compte du fichier MANIFEST.in
    include_package_data=True,
    url='https://github.com/Insoleet/mirage',

    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Topic :: Communications",
    ],
    dependency_links=("git+https://github.com/duniter/duniter-python-api.git@dev",)

)
