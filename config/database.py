from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://arjun:arjun@cluster0.j0ywwgr.mongodb.net/?retryWrites=true&w=majority"
)

db = client.skripsi_be

todo_collection = db["tes"]
user_collection = db["users"]
laporan_collection = db["laporans"]
