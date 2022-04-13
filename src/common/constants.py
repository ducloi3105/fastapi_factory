import os
import json

import config

ROOT_DIR = os.path.dirname(config.__file__)

TMP_DIR = os.path.join(ROOT_DIR, 'tmp')
if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)

PHONE_REGEX = r'^(\+8[0-9]{9,12})$|^(0[0-9]{6,15})$'

DICT_KEY_SEPARATOR = '~|~'

HTTP_METHODS = [
    'GET',
    'PUT',
    'PATCH',
    'POST',
    'DELETE'
]

STRING_LENGTH = {
    'UUID4': 36,
    'EX_SHORT': 50,
    'SHORT': 100,
    'MEDIUM': 500,
    'LONG': 1000,
    'EX_LONG': 5000,
    'LARGE': 10000,
    'EX_LARGE': 100000
}

ISO_FORMAT = '%Y-%m-%dT%H:%M:%S'

VALID_DATETIME_FORMATS = [
    ISO_FORMAT,
    '%Y-%m-%dT%H:%M:%SZ',
    '%Y-%m-%dT%H:%M:%S+00:00',
    '%Y-%m-%dT%H:%M:%S',
    '%Y-%m-%dT%H:%M',
    '%Y-%m-%d %H:%M',
    '%d/%m/%Y %H:%M'
]

PAGINATION = {
    'page': 1,
    'per_page': 50
}

MESSAGE_STATES = [
    'draft',
    'sending',
    'sending failed',
    'sent',
    'actions_pending',
    'actions_committed'
]