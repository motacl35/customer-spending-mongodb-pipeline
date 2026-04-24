import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from app.db.mongo import db
from app.config.settings import settings

st.title("Customer Spending Dashboard")

monthly = pd.DataFrame(list(db[settings.agg_monthly].find()))
category = pd.DataFrame(list(db[settings.agg_category].find()))

st.header("Monthly Spending")
fig, ax = plt.subplots()
ax.plot(monthly["total"])
st.pyplot(fig)

st.header("Spending by Category")
fig2, ax2 = plt.subplots()
ax2.bar(category["_id"], category["total"])
st.pyplot(fig2)