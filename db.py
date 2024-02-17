from flask import Flask
import pymongo
from app import app

CONNECTION_STRING = "mongodb+srv://mainuser:demopassword@workshop.buro7dq.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING, server_api=pymongo.server_api.ServerApi('1'))
db = client.get_database('grocery')
list = pymongo.collection.Collection(db, 'list')

# app.config["MONGO_URI"] = "mongodb+srv://mainuser:demopassword@workshop.buro7dq.mongodb.net/?retryWrites=true&w=majority"
# mongo = pymongo.PyMongo(app)

# @app.route("/upc/", methods=["POST"])
def add_upc(upc):
    if not get_upc(upc):
        list.insert_one({'upc': upc})
    else: # upc already in the database
        pass


# @app.route("/upc/", methods=["GET"])
def get_upc(upc):
    result = list.find_one()

    if not result:
        # return Flask.jsonify({'upc_exists': False}), 404
        return False
    else:
        # return Flask.jsonify({'msg': True}), 200
        return True


def delete_upc(upc):
    if get_upc(upc):
        list.delete_one({'upc': upc})

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)