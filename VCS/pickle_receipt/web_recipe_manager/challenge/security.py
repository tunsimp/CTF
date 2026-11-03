import os
from functools import lru_cache
from urllib.parse import urlparse

from cryptography.fernet import Fernet


class EncryptionError(Exception):
    """Raised when encryption or decryption preconditions are not met."""


@lru_cache(maxsize=1)
def _cipher(key=None):
    if key is None:
        key = 'E-LfaRyL541TMZPAO1wJ5x4eVMkp7oRoJxqEZAoSsVs='
    if not key:
        raise EncryptionError("APP_ENCRYPTION_KEY environment variable is not set")
    if isinstance(key, str):
        key = key.encode('utf-8')

    try:
        return Fernet(key)
    except Exception as exc:
        raise EncryptionError("APP_ENCRYPTION_KEY is invalid") from exc


def encrypt_data(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    return _cipher().encrypt(data)


def decrypt_data(token, key=None):
    if isinstance(token, str):
        token = token.encode('utf-8')
    return _cipher(key).decrypt(token)


def is_url_scheme_allowed(url):
    parsed = urlparse(url)
    scheme = parsed.scheme.lower()
    return scheme not in {'file', 'ftp'}
