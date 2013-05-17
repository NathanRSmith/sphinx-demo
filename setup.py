
name = 'sphinx-demo'
version = '0.1'
packages = ['sphinx_demo']
author = 'Nathan Smith'
author_email = 'nsmith13@nd.edu'
description = 'Sphinx demonstration based on Django tutorial'
url = ''
install_requires = []


####### DO NOT EDIT BELOW THIS LINE UNLESS YOU CAN'T HELP IT ##################

import os

try:
    from setuptools import setup
except:
    from distutils.core import setup

package_data = {}
for package in packages:
    packagepath = package.replace('.','/')
    cwd = os.getcwd()
    os.chdir(packagepath)
    non_pyfiles = [line.strip() for line in os.popen('find . -type f | egrep -v "py.*$"').readlines()]
    os.chdir(cwd)
    package_data[package] = non_pyfiles

setup(
    name=name,
    version=version,
    packages=packages,
    author=author,
    author_email=author_email,
    description=description,
    zip_safe=False,
    package_data = package_data,
    include_package_data = True,
    install_requires = install_requires,
)