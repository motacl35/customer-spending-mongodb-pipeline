from datetime import datetime
import math
from app.db.mongo import db
from app.config.settings import settings
from app.models.spending_model import SpendingRecord


def spending_level(amount):
    if amount >= 1000:
        return "High"
    elif amount >= 250:
        return "Medium"
    return "Low"


def clean_amount(value):
    amount = float(str(value).replace("$", "").replace(",", "").strip())

    if math.isnan(amount):
        raise ValueError("Amount is NaN")

    return amount


def clean_data():
    raw = db[settings.raw_collection]
    clean = db[settings.clean_collection]
    reject = db[settings.reject_collection]

    clean.drop()
    reject.drop()

    valid = []
    seen_ids = set()

    for doc in raw.find({}):
        try:
            transaction_id = str(doc["Transaction_ID"])

            if transaction_id in seen_ids:
                continue

            seen_ids.add(transaction_id)

            date = datetime.fromisoformat(str(doc["Transaction_date"]))
            amount_value = clean_amount(doc["Amount_spent"])

            new_doc = {
                "transaction_id": transaction_id,
                "transaction_date": date,
                "gender": str(doc["Gender"]).strip().title(),
                "age": int(doc["Age"]),
                "marital_status": str(doc["Marital_status"]).strip().title(),
                "state": str(doc["State_names"]).strip().title(),
                "segment": str(doc["Segment"]).strip().title(),
                "employment_status": str(doc["Employees_status"]).strip().title(),
                "payment_method": str(doc["Payment_method"]).strip().title(),
                "referral": int(doc["Referral"]),
                "amount_spent": amount_value,
                "year": date.year,
                "month": date.month,
                "spending_level": spending_level(amount_value),
            }

            validated = SpendingRecord(**new_doc)
            valid.append(validated.model_dump())

        except Exception as e:
            reject.insert_one({"error": str(e), "doc": doc})

        if len(valid) >= 5000:
            clean.insert_many(valid)
            valid = []

    if valid:
        clean.insert_many(valid)

    print("Clean count:", clean.count_documents({}))
    print("Rejected:", reject.count_documents({}))