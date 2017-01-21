from setuptools import setup, find_packages
import duniterpy
import os
import re


def which(program):
    """
    Detect whether or not a program is installed.
    Thanks to http://stackoverflow.com/a/377028/70191
    """
    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)

    fpath, _ = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

EDITABLE_REQUIREMENT = re.compile(r'^-e (?P<link>(?P<vcs>git|svn|hg|bzr).+#egg=(?P<package>.+)-(?P<version>\d(?:\.\d)*))$')

install_requires = []
dependency_links = []

for requirement in (l.strip() for l in open('requirements.txt')):
    match = EDITABLE_REQUIREMENT.match(requirement)
    if match:
        assert which(match.group('vcs')) is not None, \
            "VCS '%(vcs)s' must be installed in order to install %(link)s" % match.groupdict()
        install_requires.append("%(package)s==%(version)s" % match.groupdict())
        dependency_links.append(match.group('link'))
    else:
        install_requires.append(requirement)

setup(
    name='duniterpy',

    version=duniterpy.__version__,

    packages=find_packages(),

    author="inso, canercanda, s_b",

    author_email="insomniak.fr@gmail.com",

    description="A python implementation of [duniter](https://github.com/duniter/duniter) API",

    long_description=open('README.md').read(),

    # Active la prise en compte du fichier MANIFEST.in
    include_package_data=True,
    url='https://github.com/duniter/duniter-python-api',
    test_suite="tests",

    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Topic :: Communications",
    ],
    install_requires=install_requires,
    dependency_links=dependency_links

)