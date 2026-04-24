from app.db.mongo import db
from app.config.settings import settings


def create_indexes():
    clean = db[settings.clean_collection]

    clean.create_index("transaction_id")
    clean.create_index("transaction_date")
    clean.create_index("state")
    clean.create_index("segment")
    clean.create_index([("state", 1), ("transaction_date", 1)])
    clean.create_index([("segment", 1), ("transaction_date", 1)])

    print("Indexes created")