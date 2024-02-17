from flask import Flask
import pymongo

CONNECTION_STRING = "mongodb+srv://mainuser:demopassword@workshop.buro7dq.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING, server_api=pymongo.server_api.ServerApi('1'))
db = client.get_database('grocery')

# app.config["MONGO_URI"] = "mongodb+srv://mainuser:demopassword@workshop.buro7dq.mongodb.net/?retryWrites=true&w=majority"
# mongo = pymongo.PyMongo(app)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)