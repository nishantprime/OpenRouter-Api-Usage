import os
from pymongo import MongoClient

mongo_key = os.getenv('mongo_key')
client = MongoClient(mongo_key)

database = 'Chats'
collection_name = 'OpenRouter'
collection = client[database][collection_name]
