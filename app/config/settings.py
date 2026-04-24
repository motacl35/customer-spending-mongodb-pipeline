from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    mongo_uri: str = os.getenv("MONGO_URI")
    mongo_db: str = os.getenv("MONGO_DB")
    csv_path: str = os.getenv("CSV_PATH")

    raw_collection: str = os.getenv("RAW_COLLECTION")
    clean_collection: str = os.getenv("CLEAN_COLLECTION")
    reject_collection: str = os.getenv("REJECT_COLLECTION")

    agg_monthly: str = os.getenv("AGG_MONTHLY")
    agg_category: str = os.getenv("AGG_CATEGORY")
    agg_customer: str = os.getenv("AGG_CUSTOMER")


settings = Settings()