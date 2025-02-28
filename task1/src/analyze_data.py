import os
import pandas as pd
from dotenv import load_dotenv
from task1.logging_config import logger


dotenv_path = os.getenv("DOTENV_PATH")
load_dotenv(dotenv_path)
raw_data_path = os.getenv("RAW_DATA_PATH")
logger.info("Loaded environment variables.")


try:
    logger.info("Starting data analysis...")

    df = pd.read_csv(raw_data_path)
    logger.info(f"Loaded dataset successfully: {df.shape[0]} rows, {df.shape[1]} columns.")

    logger.info("Dataset Information:")
    logger.info(df.info())

    missing_values = df.isnull().sum()
    missing_values = missing_values[missing_values > 0]
    if not missing_values.empty:
        logger.info("Missing Values per Column:")
        logger.info(missing_values)

    duplicates = df.duplicated().sum()
    logger.info(f"Number of Duplicate Rows: {duplicates}")

    logger.info("Summary Statistics for Numerical Columns:")
    logger.info(df.describe())

    if 'status' in df.columns:
        logger.info("Unique Values in 'status' Column:")
        logger.info(df['status'].unique())
    if 'health' in df.columns:
        logger.info("Distribution of 'health' Column:")
        logger.info(df['health'].value_counts())
    if 'curb_loc' in df.columns:
        logger.info("Distribution of 'curb_loc' Column:")
        logger.info(df['curb_loc'].value_counts())

    logger.info("Data analysis completed successfully.")

except Exception as e:
    logger.exception("An error occurred during data analysis:")
    raise
