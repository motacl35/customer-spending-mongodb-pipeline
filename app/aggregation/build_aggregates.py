from app.db.mongo import db
from app.config.settings import settings


def safe_insert(collection_name, records):
    collection = db[collection_name]
    if records:
        collection.insert_many(records)
    else:
        print("No records for", collection_name)


def build_aggregates():
    clean = db[settings.clean_collection]

    db[settings.agg_monthly].drop()
    db[settings.agg_category].drop()
    db[settings.agg_customer].drop()

    monthly = [
        {
            "$group": {
                "_id": {"year": "$year", "month": "$month"},
                "total_spent": {"$sum": "$amount_spent"},
                "transaction_count": {"$sum": 1},
                "average_spent": {"$avg": "$amount_spent"},
            }
        },
        {"$sort": {"_id.year": 1, "_id.month": 1}},
    ]

    category = [
        {
            "$group": {
                "_id": "$segment",
                "total_spent": {"$sum": "$amount_spent"},
                "transaction_count": {"$sum": 1},
                "average_spent": {"$avg": "$amount_spent"},
            }
        },
        {"$sort": {"total_spent": -1}},
    ]

    customers = [
        {
            "$group": {
                "_id": "$state",
                "total_spent": {"$sum": "$amount_spent"},
                "transaction_count": {"$sum": 1},
                "average_spent": {"$avg": "$amount_spent"},
            }
        },
        {"$sort": {"total_spent": -1}},
        {"$limit": 20},
    ]

    safe_insert(settings.agg_monthly, list(clean.aggregate(monthly)))
    safe_insert(settings.agg_category, list(clean.aggregate(category)))
    safe_insert(settings.agg_customer, list(clean.aggregate(customers)))

    print("Aggregates done")