from distutils.log import error
import json
import os
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from settings import *


## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

def get_token_auth_header():
    #Obtains access tokens from the authorization header

    #Fetch the authorization header
    auth_header = request.headers.get('Authorization', None)

    #If no authorization header is present, raise an error.
    if not auth_header:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected'
        }, 401)

    #If there's an authorization header, split it at whitespaces to break it into parts.
    parts = auth_header.split()

    #See if the first part contains the string 'bearer', if not raise an error
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    #If the first part contains 'bearer', confirm that there's a second part
    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    #If there's a second part, confirm that there are only two parts
    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    #If everything is fine, return the second part as the token.
    token = parts[1]
    return token



def check_permissions(permission, payload):

    if 'permissions' not in payload:
        #If payload does not contain permissions raise an error.
        raise AuthError({
            'code': 'permissions_missing',
            'description': '"permissions" is expected in payload.'
        }, 400)

    if permission not in payload['permissions']:
        #If the specified permission is not in payload permissions, raise an error
        raise AuthError({
            'code': 'invalid_permissions',
            'description': 'Payload permissions must include "permission"'
        }, 403)

    #If everytihng is okay, return True
    return True


'''
    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''


def verify_decode_jwt(token):

    # Set the contents of the open url to a variable: jsonurl
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')

    # Read the contents and convert it to a json object: jwks
    jwks = json.loads(jsonurl.read())

    unverified_header = jwt.get_unverified_header(token)

    # Set the rsa_key as an empty dictionary
    rsa_key = {}

    # If the unverified header does not contain a Key Id, raise an "invalid_header" AuthError
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed'
        }, 401)

    # For every key in jwks keys, check to see if the key id matches the key id of the unverified header
    # If there's a match, populate the rsa_key dictionary with key: value pairs
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    # If the rsa_key dictionary has valid elements, create a payload and return payload with decoded content
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        # If the payload contains an expired token, raise a "token_expired" AuthError
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token has expired.'
            }, 401)

        # If it contains invalid claims, raise an "invalid_claims" AuthError
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please check the audience and issuer.'
            }, 401)

        # If other exception occours, raise an "invlaid_header" AuthError
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Invalid header. Unable to parse authentication token.'
            }, 400)

    # If the rsa_key dictionary has no valid elements, raise an "invalid_header" AuthError.
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Invalid header. Unable to find appropriate key.'
    }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except:
               abort(401)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
