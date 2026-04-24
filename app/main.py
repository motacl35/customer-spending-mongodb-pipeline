from app.ingestion.ingest_raw import ingest_raw
from app.cleaning.clean_data import clean_data
from app.db.indexes import create_indexes
from app.aggregation.build_aggregates import build_aggregates


def main():
    print("Starting pipeline...")

    ingest_raw()
    clean_data()
    create_indexes()
    build_aggregates()

    print("Pipeline finished.")


if __name__ == "__main__":
    main()