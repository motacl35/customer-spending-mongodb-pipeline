from pymongo import MongoClient
from app.config.settings import settings

print("Mongo URI being used:", settings.mongo_uri)

client = MongoClient(settings.mongo_uri)
db = client[settings.mongo_db]