from pymongo import MongoClient

db_client = MongoClient('mongodb://localhost:27017')

dbs = db_client["phinance"]
trades_db = dbs["trades"];