import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from app.db.mongo import db
from app.config.settings import settings

st.title("Customer Spending Dashboard")

# Load data from MongoDB aggregated collections
monthly = pd.DataFrame(
    list(db[settings.agg_monthly].find({}, {"_id": 1, "total_spent": 1}))
)

category = pd.DataFrame(
    list(db[settings.agg_category].find({}, {"_id": 1, "total_spent": 1}))
)

# Monthly Spending Chart
st.header("Monthly Spending")

if not monthly.empty:
    monthly["year"] = monthly["_id"].apply(lambda x: x["year"])
    monthly["month"] = monthly["_id"].apply(lambda x: x["month"])

    monthly["date"] = pd.to_datetime(
        monthly["year"].astype(str) + "-" + monthly["month"].astype(str)
    )

    monthly["date_label"] = monthly["date"].dt.strftime("%b %Y")
    monthly["total_spent"] = pd.to_numeric(monthly["total_spent"], errors="coerce")
    monthly = monthly.sort_values("date")

    st.dataframe(monthly[["date_label", "total_spent"]].head())

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly["date_label"], monthly["total_spent"], marker="o")

    ax.set_xlabel("Month")
    ax.set_ylabel("Total Spending")
    ax.set_title("Monthly Spending Trend")

    ax.set_xticks(range(0, len(monthly), 6))
    ax.set_xticklabels(monthly["date_label"].iloc[::6], rotation=45)

    st.pyplot(fig)

else:
    st.write("No monthly data found.")

# Spending by Segment
st.header("Spending by Segment")

if not category.empty:
    category = category.rename(columns={"_id": "segment"})
    category["total_spent"] = pd.to_numeric(category["total_spent"], errors="coerce")
    category = category.sort_values("total_spent", ascending=False)

    st.dataframe(category[["segment", "total_spent"]].head())

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.bar(category["segment"], category["total_spent"])

    ax2.set_xlabel("Segment")
    ax2.set_ylabel("Total Spending")
    ax2.set_title("Spending by Customer Segment")

    plt.xticks(rotation=45)

    st.pyplot(fig2)

else:
    st.write("No category data found.")