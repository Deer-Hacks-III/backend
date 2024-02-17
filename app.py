from authlib.integrations.flask_client import OAuth
<<<<<<< HEAD
from flask import Flask
from flask import jsonify
from os import environ as env
from db import db
import pymongo

app = Flask(__name__)

# auth0
=======
from flask import Flask, render_template, url_for, session, redirect, jsonify, request, _request_ctx_stack
from functools import wraps
from jose import jwt
from os import environ as env
from pymongo import MongoClient
from six.moves.urllib.request import urlopen

import json

AUTH0_DOMAIN = '{yourDomain}'
API_AUDIENCE = "https://bargain/api"
ALGORITHMS=["RS256"]

app = Flask(__name__)

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token

def requires_auth(f):
    """Determines if the Access Token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                "description":
                                    "incorrect claims,"
                                    "please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                "description":
                                    "Unable to parse authentication"
                                    " token."}, 401)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                        "description": "Unable to find appropriate key"}, 401)
    return decorated

oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)

list = pymongo.collection.Collection(db, 'list')

@app.route("/")
def home():
    return "hi"

@app.route("/list/", methods=["POST"])
def add_upc(upc):
    # json.loads(request.data)
    if not get_upc(upc):
        list.insert_one({'upc': upc})
        return jsonify({'upc_added': True}), 200
    else: # upc already in the database
        return jsonify({'upc_added': False}), 400


@app.route("/list/<int:upc>", methods=["GET"])
def get_upc(upc: int):
    result = list.find_one({'upc': upc})

    if result:
        return jsonify({'upc_exists': True}), 200
        # return False
    else:
        return jsonify({'upc_exists': False}), 404
        # return True

@app.route('/list/<int:upc>', methods=['DELETE'])
def delete_upc(upc: int):
    if get_upc(upc):
        list.delete_one({'upc': upc})
        return jsonify({'upc_deleted': True}), 200
    else:
        return jsonify({'upc_deleted': False}), 400

@app.route('/list/', methods=['GET'])
def get_all_upcs():
    return jsonify([x for x in list.find({}, {"_id": 0, "upc": 1})]) # maybe add id too?

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")
