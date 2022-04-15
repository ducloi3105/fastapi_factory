import logging
import jwt
import hashlib
import secrets
import uuid
from collections import OrderedDict
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from urllib.parse import urlparse
from subprocess import CalledProcessError, check_output
from jinja2 import FileSystemLoader, BaseLoader, Environment as JinjaEnv

from config import ENVIRONMENT, BASE_DOMAIN

from .constants import PAGINATION, VALID_DATETIME_FORMATS


def make_loggable_data(data):
    length = 1000
    result = str(data)

    if len(result) > length:
        result = result[:length] + '...'

    return result


def get_url_origin(url):
    parsed = urlparse(url)
    return '{schema}://{netloc}'.format(
        schema=parsed.scheme,
        netloc=parsed.netloc
    )


def encrypt(string, secret_key):
    if not isinstance(secret_key, bytes):
        secret_key = secret_key.encode()

    fernet = Fernet(secret_key)

    if not isinstance(string, bytes):
        string = string.encode()
    return fernet.encrypt(string).decode()


def decrypt(token, secret_key):
    if not isinstance(secret_key, bytes):
        secret_key = secret_key.encode()

    fernet = Fernet(secret_key)

    if not isinstance(token, bytes):
        token = token.encode()
    return fernet.decrypt(token).decode()


def get_now(timestamp=False, add_time=None):
    result = datetime.utcnow()
    if timestamp:
        return result.timestamp()

    if add_time:
        result = result + timedelta(seconds=add_time)

    return result


def paginate(query, page=None, per_page=None):
    if not page:
        page = PAGINATION['page']
    if not per_page:
        per_page = PAGINATION['per_page']
    return query.offset((page - 1) * per_page).limit(per_page)


def convert_string_to_datetime(string, formats):
    value = None
    for datetime_format in formats:
        try:
            value = datetime.strptime(string, datetime_format)
            break
        except ValueError:
            continue

    return value


def make_jwt_token(secret_key, expire_in=None, **kwargs):
    now = datetime.now()

    if expire_in:
        expire = now + timedelta(seconds=expire_in)

    else:
        expire = now + timedelta(seconds=7200)

    payload = OrderedDict(
        exp=expire,
        **kwargs
    )
    return jwt.encode(payload, secret_key, algorithm='HS256').decode()


def decode_jwt_token(token, secret_key, verify_exp=False):
    try:
        token_data = jwt.decode(token, secret_key,
                                options={'verify_exp': verify_exp})

    except Exception as e:
        return None
    return token_data


def hash_string(string, mode='sha256'):
    hash_handler = getattr(hashlib, mode, None)
    if not hash_handler:
        raise Exception('UnsupportedHashMode')

    if not isinstance(string, bytes):
        string = string.encode()

    return hash_handler(string).hexdigest()


def find_list_element_obj(array: list,
                          key: str,
                          value: any) -> tuple:
    result = None
    index = None
    for i, item in enumerate(array):
        if isinstance(item, dict):
            v = item[key]
        elif isinstance(item, object):
            v = getattr(item, key)
        else:
            v = item
        if v != value:
            continue

        result = item
        index = i
        break
    return result, index


def find_in_list(array: list,
                 values: dict):
    first_item = array[0]

    def check_function(item):
        match = True
        for k, v in values.items():
            if isinstance(first_item, dict):
                if k not in item:
                    match = False
                    break
                item_value = item[k]
            else:
                if not hasattr(item, k):
                    match = False
                    break
                item_value = getattr(item, k)
            if v != item_value:
                match = False
                break
        return match

    query = list(filter(lambda x: check_function(x), array))
    if not len(query):
        return None, None
    result = query[0]
    return result, array.index(result)


def gen_random_token_hex(n: int = 16):
    return secrets.token_hex(n)


def change_datetime_format(string, to_format):
    datetime_obj = convert_string_to_datetime(string, VALID_DATETIME_FORMATS)
    return datetime_obj.strftime(to_format)


def get_api_base_url():
    if ENVIRONMENT == 'local':
        base_url = f'http://{BASE_DOMAIN}:5002'
    else:
        base_url = f'https://{BASE_DOMAIN}/api/v1'

    return base_url


def execute_command(command: list):
    command = ' '.join(command).split(' ')
    try:
        output = check_output(command).decode('utf-8')
    except CalledProcessError as err:
        log.error(err.output.decode('utf-8'))
        raise err
    log.info(f'Output from command:\n{output}')
    return output


def gen_html(content, data, template_dir=None):
    if template_dir:
        loader = FileSystemLoader(template_dir)
    else:
        loader = BaseLoader()

    template_handler = JinjaEnv(
        loader=loader).from_string(content)

    return template_handler.render(
        **data
    )


def generate_message_id(suffix='@vccloud.vn'):
    if not isinstance(suffix, str):
        suffix = str(suffix)

    return ''.join(['<', str(uuid.uuid4()) + suffix, '>'])