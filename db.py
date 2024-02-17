from flask import Flask
import pymongo
from app import app
CONNECTION_STRING = "mongodb+srv://demouser:<1HqeX4d6BuZtrajq>@workshop.buro7dq.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('flask_mongodb_atlas')
user_collection = pymongo.collection.Collection(db, 'user_collection')

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)