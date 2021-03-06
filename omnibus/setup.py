import os
from setuptools import find_packages, setup
from finitelycomputable_microsites_setup import (
        version, base_setup, wsgi_extras_require,
)

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='omnibus',
    version=version,
    packages=find_packages('.'),
    description='The microsites of finitelycomputable.net run inside Django',
    long_description=README,
    long_description_content_type="text/x-rst",
    scripts=[
        'manage.py',
        'cherry-server.py',
        'bjoern-server.py',
        'finitelycomputable_microsites_setup.py'],
    install_requires=[
        'Django~=3.0',
        'finitelycomputable-idtrust-django==' + version],
    extras_require=wsgi_extras_require,
    url='http://www.finitelycomputable.net/wsgi_info',
    **base_setup
)
