from functools import wraps
from flask import abort, session
import hashlib
import os
import jwt
import datetime
import re

def generate_key(x): return os.urandom(x).hex()

FLASK_SECRET_KEY = '108df1d82a562fed8cbe4129886ef747d39a22662ec7d83c21bb8a80a935637e996fa8e2cc733734ef54e51fdcb9c950676ccd0c97b33779b6b7d838e0e3eb3250445ef05b5fcb5e86474ecb6ddd0ffbedfd2ab62a536da2da3edd378eb55040c88a3e6c95912e5e82fbee0e18f374bac9adc4efe1aec892a96d267fba1939e7fbecafaf25f0353fec89ec731a0c66286eea7ac512d13cefa8e37624741dab4c99a4c48b65fe18ad5e101b0a9e9dd811b618ee96b95913ed1468b59cd13821a17a6c3ae0ef4aeca913fcc00bfc44d732b715e93034337ce537b8afc51fbe4b58ccde1cd2537d89e86a95d36c6ef264965b46549e1081d23750e54c0aefcfd8e5'
jwt_key = '2583c471f9445dc10245f74233768701562661b4211cc5619e7528f0d27b6a3c6ea7697379a90a0166c71525e8bf055931b3908e8e572db0642d3b2d0d79a064bf0cc97795149232f7a984935f8ee66ad8c0cbec50af0e8784bfe424ed96570b566fe408f65d0f95f317eeab7b09f49513463dfd16e613417005e6fc93d2cc6bfbc1845623b1ac5aebe85e7c044176dac98d5a338e5a81628fdcd771bda5ebb552ad3af4cdb37e5d54f24457e166d94c27d9fff676513c0adbceb3e357ed13c2b156e6359d71b046d484ad91b79cf66110818718d2072378c472342b4bdc164d1383b0a5b96ccd7c2905524d8447bf261f063a538bcad421b5d7904b87251194'

def create_JWT(email: str, role="regular"):
    utc_time = datetime.datetime.now(datetime.UTC)
    token_expiration = utc_time + datetime.timedelta(minutes=1000)
    data = {
        'email': 'flag@gmail',
        "exp": token_expiration,
        'role': "admin"
    }
    encoded = jwt.encode(data, jwt_key, algorithm='HS256')
    return encoded


def verify_JWT(token):
    try:
        token_decode = jwt.decode(
            token,
            jwt_key,
            algorithms='HS256'
        )
        return token_decode
    except:
        return abort(401, 'Invalid authentication token!')


def is_valid_email(email):
    # Don't support long emails addr
    if len(email) > 50:
        return False
    # Canonical email addresses according to RFC 5322
    email_regex = r'([#-\'*+/-9=?A-Z^-~-]+(\.[#-\'*+/-9=?A-Z^-~-]+)*|"([]#-[^-~ \t]|(\\[\t -~]))+")@([#-\'*+/-9=?A-Z^-~-]+(\.[#-\'*+/-9=?A-Z^-~-]+)*|\[[\t -Z^-~]*])'
    if re.fullmatch(email_regex, email, re.IGNORECASE):
        return True
    return False

def create_hash(password):
    sha256_hash = hashlib.sha256(password.encode())
    return sha256_hash.hexdigest()

def verify_password(hashedPassword, password):
    sha256_hash = create_hash(password)
    if sha256_hash == hashedPassword:
        return True
    else:
        return False

def timestamp():
    return datetime.now()

def is_authenticated(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = session.get('auth')
        print(token)
        if not token:
            return abort(401, 'Unauthorized access detected!!')

        verify_JWT(token)

        return f(*args, **kwargs)

    return decorator


def is_admin(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = session.get('auth')
        if not token:
            return abort(401, 'Unauthorized access detected!!')

        decoded_token = verify_JWT(token)
        if decoded_token["role"] != "admin":
            return abort(401, 'Unauthorized access detected!!')
        
        return f(*args, **kwargs)

    return decorator

def escape_html(s):
    # Define a mapping of special characters to HTML entities
    html_escape_table = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
        "`": "&#96;"
    }
    # Use a list comprehension to replace each special character with its HTML entity
    return ''.join(html_escape_table.get(c, c) for c in s)