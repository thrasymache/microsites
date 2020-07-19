#! /usr/bin/env python
import os
from setuptools import setup
from finitelycomputable_microsites_setup import (
        version, base_setup, wsgi_extras_require,
)

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='finitelycomputable-helloworld-cherrypy-falcon',
    version=version,
    py_modules=['finitelycomputable.helloworld_cherrypy'],
    entry_points={
        'console_scripts': [
            'finitelycomputable-helloworld-cherrypy = finitelycomputable.helloworld_cherrypy:run']
        },
    description='hello_world in CherryPy from an implementation in Falcon',
    long_description=README,
    long_description_content_type="text/x-rst",
    scripts=['finitelycomputable_microsites_setup.py'],
    install_requires=['CherryPy<19'],
    extras_require=wsgi_extras_require,
    url='http://www.finitelycomputable.net/hello_world',
    **base_setup
)