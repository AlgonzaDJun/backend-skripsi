from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("DB_URI"))

db = client.skripsi_be

todo_collection = db["tes"]
user_collection = db["users"]
laporan_collection = db["laporans"]
chat_collection = db["chats"]
