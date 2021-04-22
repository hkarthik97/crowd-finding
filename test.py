import pymongo
from pymongo import MongoClient
cluster = MongoClient("mongodb+srv://karthik:karthik@cluster0.dva2k.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",tls=True,tlsAllowInvalidCertificates=True)
db = cluster["myFirstDatabase"]
collection = db["People"]
post = {"People":10}
collection.insert_one(post)