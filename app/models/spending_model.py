from pydantic import BaseModel, field_validator
from datetime import datetime


class SpendingRecord(BaseModel):
    transaction_id: str
    transaction_date: datetime
    gender: str
    age: int
    marital_status: str
    state: str
    segment: str
    employment_status: str
    payment_method: str
    referral: int
    amount_spent: float
    year: int
    month: int
    spending_level: str

    @field_validator("amount_spent")
    @classmethod
    def validate_amount(cls, value):
        if value <= 0:
            raise ValueError("Amount spent must be positive")
        return value

    @field_validator("gender", "marital_status", "state", "segment", "employment_status", "payment_method")
    @classmethod
    def clean_text(cls, value):
        return str(value).strip().title()