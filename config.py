import yaml
import os

ROOT_PATH = os.path.dirname(__file__)

CONFIG_FILE_PATH = os.path.join(ROOT_PATH, 'env.yaml')

if os.path.exists(CONFIG_FILE_PATH):
    with open(CONFIG_FILE_PATH, 'r') as r_file:
        data = yaml.safe_load(r_file)
else:
    data = dict()

ENVIRONMENT = data.get('ENVIRONMENT', 'local')

SECRET_KEY = data.get('SECRET_KEY', 'secret_key')

MONGO_URI = data.get('MONGO_URI', 'mongo_uri')
POSTGRES_URI = data.get('POSTGRES_URI', 'postgres_uri')
POSTGRES_ASYNC_URI = data.get("POSTGRES_ASYNC_URI", "postgres_async_uri")
BASE_DOMAIN = data.get('BASE_DOMAIN', 'localhost')

REDIS = data.get('REDIS', {
    'host': 'localhost',
    'port': 6379,
    'password': 'password'
})


class ApiConfig(object):
    ENV = ENVIRONMENT

    SECRET_KEY = SECRET_KEY

    DEBUG = ENVIRONMENT != 'production'

    MAX_CONTENT_LENGTH = 15 * 1024 * 1024

    PROPAGATE_EXCEPTIONS = True


class CeleryConfig(object):
    broker_url = 'redis://:{password}@{host}:{port}/{db}'.format(
        password=REDIS['password'],
        port=REDIS['port'],
        host=REDIS['host'],
        db=0
    )


class ImapConfig:
    imap_host = data.get('IMAP_HOST', 'imap_host')
    imap_port = data.get('IMAP_PORT', 'imap_port')
    message_id_prefix = data.get('MESSAGE_ID_SUFFIX', 'message_id_suffix')