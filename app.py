from authlib.integrations.flask_client import OAuth
from flask import Flask
from flask import jsonify
from os import environ as env
from db import db
import pymongo

app = Flask(__name__)

# auth0
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

if __name__ == '__main__':
	app.run(debug=True)