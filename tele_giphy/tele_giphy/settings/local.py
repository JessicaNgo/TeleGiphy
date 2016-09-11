from .base import *

INSTALLED_APPS = INSTALLED_APPS + [
    'debug_toolbar',
]

ALLOWED_HOSTS = ['localhost']

DEBUG = True