from pymongo import MongoClient

db_connection = MongoClient("mongodb+srv://Sadanon:1234@cluster0.rmsa1et.mongodb.net/?retryWrites=true&w=majority")
db = db_connection.CS403

collection_image = db["image"]
