import pandas as pd
from app.db.mongo import db
from app.config.settings import settings


def ingest_raw():
    collection = db[settings.raw_collection]
    collection.drop()

    chunk_size = 50000
    total = 0

    for chunk in pd.read_csv(settings.csv_path, chunksize=chunk_size):
        records = chunk.where(pd.notnull(chunk), None).to_dict("records")
        collection.insert_many(records)

        total += len(records)
        print("Inserted:", total)

    print("Raw complete:", collection.count_documents({}))