import os
from datetime import timedelta
import json

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

XML = False
IF_MATCH = True
BANDWIDTH_SAVER = False
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S+0000'

APPLICATION_NAME = os.environ.get('APP_NAME', 'Superdesk')
server_url = urlparse(os.environ.get('SUPERDESK_URL', 'http://localhost:5000/api'))
CLIENT_URL = os.environ.get('SUPERDESK_CLIENT_URL', 'http://localhost:9000')
URL_PROTOCOL = server_url.scheme or None
SERVER_NAME = server_url.netloc or None
URL_PREFIX = server_url.path.lstrip('/') or ''
VALIDATION_ERROR_STATUS = 400

CACHE_CONTROL = 'max-age=0, no-cache'

X_DOMAINS = '*'
X_MAX_AGE = 24 * 3600
X_HEADERS = ['Content-Type', 'Authorization', 'If-Match']


MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'liveblog')
if os.environ.get('MONGOLAB_URI'):
    MONGO_URI = os.environ.get('MONGOLAB_URI')
elif os.environ.get('MONGODB_PORT'):
    MONGO_URI = '{0}/{1}'.format(os.environ.get('MONGODB_PORT').replace('tcp:', 'mongodb:'), MONGO_DBNAME)

ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL', 'http://localhost:9200')
ELASTICSEARCH_INDEX = os.environ.get('ELASTICSEARCH_INDEX', 'liveblog')
if os.environ.get('ELASTIC_PORT'):
    ELASTICSEARCH_URL = os.environ.get('ELASTIC_PORT').replace('tcp:', 'http:')

REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
if os.environ.get('REDIS_PORT'):
    REDIS_URL = os.environ.get('REDIS_PORT').replace('tcp:', 'redis:')
BROKER_URL = os.environ.get('CELERY_BROKER_URL', REDIS_URL)
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', REDIS_URL)
CELERY_ALWAYS_EAGER = (os.environ.get('CELERY_ALWAYS_EAGER', False) == 'True')
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['pickle', 'json']  # it's using pickle when in eager mode

CELERYBEAT_SCHEDULE = {
    'auth_session_purge': {
        'task': 'apps.auth.session_purge',
        'schedule': timedelta(minutes=30)
    }
}

SENTRY_DSN = os.environ.get('SENTRY_DSN')
SENTRY_INCLUDE_PATHS = ['superdesk']

INSTALLED_APPS = [
    'apps.auth',
    'apps.users',
    'superdesk.upload',
    'superdesk.notification',
    'superdesk.activity',
    'superdesk.storage.amazon.import_from_amazon',

    'apps.archive',
    'apps.preferences',
    'apps.groups',
    'apps.prepopulate',

    'liveblog.blogs',
    'liveblog.posts'
]

RESOURCE_METHODS = ['GET', 'POST']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']
EXTENDED_MEDIA_INFO = ['content_type', 'name', 'length']
RETURN_MEDIA_AS_BASE64_STRING = False

AMAZON_CONTAINER_NAME = os.environ.get('AMAZON_CONTAINER_NAME', '')
AMAZON_ACCESS_KEY_ID = os.environ.get('AMAZON_ACCESS_KEY_ID', '')
AMAZON_SECRET_ACCESS_KEY = os.environ.get('AMAZON_SECRET_ACCESS_KEY', '')
AMAZON_REGION = os.environ.get('AMAZON_REGION', '')


RENDITIONS = {
    'picture': {
        'thumbnail': {'width': 220, 'height': 120},
        'viewImage': {'width': 640, 'height': 640},
        'baseImage': {'width': 1400, 'height': 1400},
    },
    'avatar': {
        'thumbnail': {'width': 60, 'height': 60},
        'viewImage': {'width': 200, 'height': 200},
    }
}

SERVER_DOMAIN = 'localhost'

BCRYPT_GENSALT_WORK_FACTOR = 12
RESET_PASSWORD_TOKEN_TIME_TO_LIVE = int(os.environ.get('RESET_PASS_TTL', 1))  # The number of days a token is valid
# The number of days an activation token is valid
ACTIVATE_ACCOUNT_TOKEN_TIME_TO_LIVE = int(os.environ.get('ACTIVATE_TTL', 7))

# email server
MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
MAIL_PORT = int(os.environ.get('MAIL_PORT', 465))
MAIL_USE_TLS = json.loads(os.environ.get('MAIL_USE_TLS', 'False').lower())
MAIL_USE_SSL = json.loads(os.environ.get('MAIL_USE_SSL', 'True').lower())
MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'liveblogsf@gmail.com')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'fabric2010')
ADMINS = [MAIL_USERNAME]

# LDAP settings
LDAP_SERVER = os.environ.get('LDAP_SERVER', '')  # Ex: ldap://sourcefabric.org
LDAP_SERVER_PORT = os.environ.get('LDAP_SERVER_PORT', 389)

# Fully Qualified Domain Name. Ex: sourcefabric.org
LDAP_FQDN = os.environ.get('LDAP_FQDN', '')

# LDAP_BASE_FILTER limit the base filter to the security group. Ex: OU=Superdesk Users,dc=sourcefabric,dc=org
LDAP_BASE_FILTER = os.environ.get('LDAP_BASE_FILTER', '')

# change the user depending on the LDAP directory structure
LDAP_USER_FILTER = os.environ.get('LDAP_USER_FILTER', "(&(objectCategory=user)(objectClass=user)(sAMAccountName={}))")

# LDAP User Attributes to fetch. Keys would be LDAP Attribute Name and Value would be Supderdesk Model Attribute Name
LDAP_USER_ATTRIBUTES = {'givenName': 'first_name', 'sn': 'last_name', 'displayName': 'display_name',
                        'mail': 'email', 'ipPhone': 'phone'}

if LDAP_SERVER:
    INSTALLED_APPS.append('apps.auth.ldap')
else:
    INSTALLED_APPS.append('apps.auth.db')

SUPERDESK_TESTING = (os.environ.get('SUPERDESK_TESTING', 'false').lower() == 'true')

# The number of minutes since the last update of the Mongo auth object after which it will be deleted
SESSION_EXPIRY_MINUTES = 240
