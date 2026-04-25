# Customer Spending Analytics Pipeline

## Project Overview
This project implements a full Big Data pipeline using MongoDB to process and analyze 1 million customer spending transactions from 2018–2025. 

The system ingests raw data, cleans and validates records, stores structured data, and generates aggregated insights that are visualized through a dashboard.


## Platform Chosen and Why
**MongoDB** was selected as the primary platform because:

- It efficiently handles large-scale, semi-structured data
- JSON-style documents match the structure of transaction records
- Built-in aggregation pipelines allow fast analytics
- Indexing improves query performance for large datasets

MongoDB provides flexibility and scalability needed for Big Data processing.


## Dataset Description
- Dataset: Customer Spending (1,000,000 records)
- Time Range: 2018–2025

### Key Fields:
- Transaction_ID
- Transaction_date
- Gender
- Age
- State_names
- Segment
- Payment_method
- Amount_spent

This dataset is large and complex enough to require proper data cleaning, validation, and aggregation.


## Architecture
Pipeline flow:

```
CSV Dataset
↓
Raw MongoDB Collection
↓
Cleaning + Validation (Pydantic)
↓
Clean MongoDB Collection
↓
Aggregation Layer
↓
Streamlit Dashboard
```

The system uses Docker to run MongoDB locally and Python to handle ingestion, processing, and analytics.

## Setup Instructions

### 1. Clone Repository
``` bash
git clone https://github.com/motacl35/customer-spending-mongodb-pipeline
cd customer-spending-mongodb-pipeline
```

### 2. Install Dependencies
``` bash
uv venv
source .venv/bin/activate
uv add pandas pymongo pydantic python-dotenv streamlit matplotlib pytest mypy
```
### 3. Start MongoDB
``` bash
docker compose up -d
```
### 4. Run the Pipeline 
``` bash
uv run python -m app.main
```
### 5. View the Dashboard
``` bash
streamlit run app/dashboard/dashboard.py
```
## Pipeline Stages
1. Raw Layer
- Loads 1,000,000 records into MongoDB
- Stores original dataset without modification

2. Clean Layer
- Removes duplicates
- Normalizes text values
- Converts date formats
- Adds derived fields:
    - year
    - month
    - spending_level
- Validates records using Pydantic
- Stores invalid records in a rejected_records collection

3. Aggregated Layer
- Creates summary datasets:
    - Monthly spending trends
    - Spending by customer segment
    - Top states by total spending

These aggregated collections are stored back into MongoDB.

## Query Optimization and Indexing

Indexes were created on key fields such as transaction_date, segment, and state.

These fields were selected because they are frequently used in aggregation queries and dashboard visualizations. For example:

Monthly trend analysis relies on transaction dates
Segment analysis depends on the segment field

Indexing these fields improves query performance and reduces computation time.

Sharding was not implemented because the dataset size can be efficiently handled on a single-node setup. However, the pipeline is designed to scale if needed.

## Reliability and Validation

Data validation is handled using Pydantic models
Invalid records are separated into a rejected_records collection. This prevents bad data from affecting analytics

This ensures data integrity and reflects real-world pipeline reliability practices.

## Running Tests
``` bash
pytest
```
## The project includes tests that validate:

- Data cleaning logic
- Schema validation
- Aggregation correctness

## Type Checking
``` bash
mypy app
```
Mypy is used to enforce type safety and improve code reliability.

## Visualizations

The dashboard presents insights using aggregated data:

Monthly Spending Trend

→ Shows how customer spending changes over time

Spending by Customer Segment

→ Identifies high-value customer groups

Top States by Total Spending

→ Highlights geographic areas with the highest spending

Each visualization is tied to a business question and supports data-driven decision making.

## Screenshots

## Running
![Running](images/running.png)

## Test
![Test](images/test.png)

## Website Preview
![monthly_spending](images/monthly_spending.png)

![spending_segment](images/spending_segment.png)
Examples to include:

MongoDB collection counts
Sample documents
Aggregated data
Dashboard visuals
Team Members

## Team members
- Clevis Mota  
- Jackson Downing   
- William Drain 

## Notes

This project was designed to simulate a real-world data pipeline. It demonstrates ingestion, transformation, validation, aggregation, and visualization of large-scale data using MongoDB and Python.

The implementation reflects engineering best practices, including modular design, validation, indexing, and reproducibility.