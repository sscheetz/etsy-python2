#!/usr/bin/python
import os
from setuptools import setup

this_dir = os.path.realpath(os.path.dirname(__file__))
long_description = open(os.path.join(this_dir, 'README.md'), 'r').read()

setup(
    name = 'etsy2',
    version = '0.7.0',
    author = 'Sean Scheetz',
    author_email = 'contact_through_github@gmail.com',
    description = 'Python access to the Etsy API',
    license = 'GPL v3',
    keywords = 'etsy api handmade',
    packages = ['etsy2'],
    long_description = long_description,
    long_description_content_type="text/markdown",
    test_suite = 'test',
    project_urls = {
        'Source Code': 'https://github.com/sscheetz/etsy-python2'
    },
    install_requires=['requests_oauthlib'],
)