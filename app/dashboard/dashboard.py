import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from app.db.mongo import db
from app.config.settings import settings

st.title("Customer Spending Dashboard")

monthly = pd.DataFrame(list(db[settings.agg_monthly].find()))
category = pd.DataFrame(list(db[settings.agg_category].find()))

st.header("Monthly Spending")

if not monthly.empty:
    monthly["date_label"] = monthly["_id"].apply(
        lambda x: str(x["year"]) + "-" + str(x["month"]).zfill(2)
    )

    fig, ax = plt.subplots()
    ax.plot(monthly["date_label"], monthly["total_spent"])
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Spending")
    ax.set_title("Monthly Spending Trend")
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.write("No monthly data found.")

st.header("Spending by Segment")

if not category.empty:
    fig2, ax2 = plt.subplots()
    ax2.bar(category["_id"], category["total_spent"])
    ax2.set_xlabel("Segment")
    ax2.set_ylabel("Total Spending")
    ax2.set_title("Spending by Customer Segment")
    plt.xticks(rotation=45)
    st.pyplot(fig2)
else:
    st.write("No category data found.")