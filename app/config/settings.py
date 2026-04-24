from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    mongo_uri: str = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017")
    mongo_db: str = os.getenv("MONGO_DB", "customer_spending_db")
    csv_path: str = os.getenv("CSV_PATH", "data/customer_spending_1M_2018_2025.csv")

    raw_collection: str = os.getenv("RAW_COLLECTION", "spending_raw")
    clean_collection: str = os.getenv("CLEAN_COLLECTION", "spending_clean")
    reject_collection: str = os.getenv("REJECT_COLLECTION", "rejected_records")

    agg_monthly: str = os.getenv("AGG_MONTHLY", "agg_monthly")
    agg_category: str = os.getenv("AGG_CATEGORY", "agg_category")
    agg_customer: str = os.getenv("AGG_CUSTOMER", "agg_customer")


settings = Settings()