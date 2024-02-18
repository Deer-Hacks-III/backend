from authlib.integrations.flask_oauth2 import ResourceProtector
from authlib.integrations.flask_client import OAuth
from flask import Flask, url_for, session, redirect
from flask import jsonify
from db import db
from validator import Auth0JWTBearerTokenValidator
import pymongo

app = Flask(__name__)
oauth = OAuth(app)
oauth.register(
    'auth0',
    client_id='QSKLcy8v0jrQXXpTqGiLeTooKhjTSHid',
    client_secret='u1G5K9P6-Ugrlq4H6FZibNWVoH6mAJNnUVik1p-Yq746slm1TEezSdNNJFtZcquM',
    api_base_url='https://dev-mzldvbqnuyiy4310.us.auth0.com',
    access_token_url='https://dev-mzldvbqnuyiy4310.us.auth0.com/oauth/token',
    authorize_url='https://dev-mzldvbqnuyiy4310.us.auth0.com/authorize',
    client_kwargs={'scope': 'openid profile email'},
)

list = pymongo.collection.Collection(db, 'list')

require_auth = ResourceProtector()

validator = Auth0JWTBearerTokenValidator(
    "dev-mzldvbqnuyiy4310.us.auth0.com",
    "https://bargain/api"
)
require_auth.register_token_validator(validator)


@app.route("/api/public")
def public():
    """No access token required."""
    response = (
        "Hello from a public endpoint! You don't need to be"
        " authenticated to see this."
    )
    return jsonify(message=response)


@app.route("/api/private")
@require_auth(None)
def private():
    """A valid access token is required."""
    response = (
        "Hello from a private endpoint! You need to be"
        " authenticated to see this."
    )
    return jsonify(message=response)


@app.route("/api/private-scoped")
@require_auth("read:messages")
def private_scoped():
    """A valid access token and scope are required."""
    response = (
        "Hello from a private endpoint! You need to be"
        " authenticated and have a scope of read:messages to see"
        " this."
    )
    return jsonify(message=response)

@app.route("/")
def home():
    return "hi"

@app.route("/list/", methods=["POST"])
def add_upc(upc: int):
    if not list.find_one({'upc': upc}):
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
    if list.find_one({'upc': upc}):
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
        redirect_uri='http://localhost:5000/callback'
    )

@app.route("/callback")
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token.json()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

