import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'Input your Auth0 Domian'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'input API audience'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


###To Generate token from authorization#######
def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        abort(401)
        #raise AuthError({
        #    'code': 'authorization_header_missing',
        #    'description': 'Authorization header is expected.'
        #}, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        abort(401)
        #raise AuthError({
        #    'code': 'invalid_header',
        #    'description': 'Authorization header must start with "Bearer".'
        #}, 401)

    elif len(parts) == 1:
        abort(401)
        #raise AuthError({
        #    'code': 'invalid_header',
        #    'description': 'Token not found.'
        #}, 401)

    elif len(parts) > 2:
        abort(401)
        #raise AuthError({
        #    'code': 'invalid_header',
        #    'description': 'Authorization header must be bearer token.'
        #}, 401)

    token = parts[1]
    return token

#####to Generate token payload######
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        abort(401)
        #raise AuthError({
        #    'code': 'invalid_header',
        #    'description': 'Authorization malformed.'
        #}, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
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

        except jwt.ExpiredSignatureError:
            abort(401)
            #raise AuthError({
            #    'code': 'token_expired',
            #    'description': 'Token expired.'
            #}, 401)

        except jwt.JWTClaimsError:
            abort(401)
            #raise AuthError({
            #    'code': 'invalid_claims',
            #    'description': 'Incorrect claims. Please, check the audience and issuer.'
            #}, 401)
        except Exception:
            abort(400)
            #raise AuthError({
            #    'code': 'invalid_header',
            #    'description': 'Unable to parse authentication token.'
            #}, 400)
    abort(400)
    #raise AuthError({
    #            'code': 'invalid_header',
    #            'description': 'Unable to find the appropriate key.'
    #        }, 400)

######TO CHECK PERMISSIONS ON TOKEN PAYLOAD######
def check_token_permissions(permission, payload):
    if 'permissions' not in payload:
        abort(400)
    ####checking if the endpoint permission exist in payload
    if permission not in payload['permissions']:
        abort(403)
    return True

#### for endpoints authorization#####
def endpoint_auth(permission = ''):
    def required_auth(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except:
                abort(403)
            ###########Checking Permission on payload######
            check_token_permissions(permission,payload)
            return f(*args, **kwargs)
        return wrapper
    return required_auth
