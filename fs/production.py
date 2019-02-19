from fs.settings import *
import dj_database_url
from decouple import config

ENVIRONMENT = 'production'
DEBUG = False
ALLOWED_HOSTS = ['*']
DATABASES['default'] = dj_database_url.config(default=config('DATABASE_URL'))
