from flask import Flask
import pymongo
from app import app
CONNECTION_STRING = "mongodb+srv://mainuser:demopassword@workshop.buro7dq.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING, server_api=pymongo.server_api.ServerApi('1'))
db = client.get_database('flask_mongodb_atlas')
user_collection = pymongo.collection.Collection(db, 'user_collection')

@app.route("/upc/", methods=["POST"])
def add_upc():
    pass

@app.route("/upc/", methods=["GET"])
def get_upc():
    pass

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)