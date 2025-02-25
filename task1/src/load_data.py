import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from task1.logging_config import logger

# Load environment variables
load_dotenv()
db_url = os.getenv("DATABASE_URL")
cleaned_file = os.getenv("CLEANED_DATA_PATH")

try:
    df = pd.read_csv(cleaned_file)
    logger.info(f"Loaded cleaned dataset: {df.shape[0]} rows, {df.shape[1]} columns.")

    # Rename columns to match PostgreSQL table column names
    df.rename(columns={
        "community board": "community_board",
        "council district": "council_district",
        "census tract": "census_tract",
    }, inplace=True)

    # Insert data into the PostgreSQL table
    engine = create_engine(db_url)
    df.to_sql("nyc_trees", engine, if_exists="append", index=False)
    logger.info("Data loaded into PostgreSQL table 'nyc_trees' successfully.")

except Exception as e:
    logger.exception("An error occurred while loading data into PostgreSQL:")
    raise
