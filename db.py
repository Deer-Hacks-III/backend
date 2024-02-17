from flask import Flask
import pymongo
from app import app

CONNECTION_STRING = "mongodb+srv://mainuser:demopassword@workshop.buro7dq.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING, server_api=pymongo.server_api.ServerApi('1'))
db = client.get_database('grocery')
list = pymongo.collection.Collection(db, 'list')

# app.config["MONGO_URI"] = "mongodb+srv://mainuser:demopassword@workshop.buro7dq.mongodb.net/?retryWrites=true&w=majority"
# mongo = pymongo.PyMongo(app)

# @app.route("/list/", methods=["POST"])
def add_upc(upc):
    # json.loads(request.data)
    if not get_upc(upc):
        list.insert_one({'upc': upc})
    else: # upc already in the database
        print("adding not success")


# @app.route("/list/<int:upc>", methods=["GET"])
def get_upc(upc: int):
    result = list.find_one({'upc': upc})

    if not result:
        # return Flask.jsonify({'upc_exists': False}), 404
        return False
    else:
        # return Flask.jsonify({'upc_exists': True}), 200
        return True

# @app.route('/list/<int:upc>', methods=['DELETE'])
def delete_upc(upc: int):
    if get_upc(upc):
        # return Flask.jsonify({'upc_deleted': True}), 200
        list.delete_one({'upc': upc})
        print("deleted")
    else:
        # return Flask.jsonify({'upc_deleted': False}), 400
        print("not deleted")

def get_all_upcs():
    return Flask.jsonify([x for x in list.find({}, {"_id": 0, "upc": 1})]) # maybe add id too?

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)