from omnibus.settings.base import *

DEBUG = False

ALLOWED_HOSTS = [
    'finitelycomputable.nfshost.com',
    'www.finitelycomputable.net',
    'localhost', '127.0.0.1']
#CSRF_COOKIE_SECURE = True
INSTALLED_APPS += [
]
MIDDLEWARE += [
]
#SECURE_BROWSER_XSS_FILTER = True
#SECURE_CONTENT_TYPE_NOSNIFF = True
#SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#SECURE_HSTS_PRELOAD = True
#SECURE_HSTS_SECONDS = 60
#SECURE_SSL_REDIRECT = True
#SESSION_COOKIE_SECURE = True
ROOT_URLCONF = 'omnibus.urls'
X_FRAME_OPTIONS = 'DENY'
