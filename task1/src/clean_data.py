import os
import pandas as pd
from dotenv import load_dotenv
from task1.logging_config import logger

# Load environment variables from .env
load_dotenv()
raw_data_path = os.getenv("RAW_DATA_PATH")

try:

    df = pd.read_csv(raw_data_path)
    logger.info(f"Loaded dataset successfully: {df.shape[0]} rows, {df.shape[1]} columns.")

    # Remove duplicate rows
    initial_count = df.shape[0]
    df = df.drop_duplicates()
    logger.info(f"Removed {initial_count - df.shape[0]} duplicate rows.")

    # Fill missing values in key columns with 'Unknown'
    for col in ['health', 'spc_latin', 'spc_common']:
        if col in df.columns:
            missing_before = df[col].isnull().sum()
            df[col].fillna('Unknown', inplace=True)
            logger.info(f"Filled {missing_before} missing values in '{col}' column with 'Unknown'.")

    # Optionally, fill missing values in 'sidewalk' with 'NoDamage'
    if 'sidewalk' in df.columns:
        missing_before = df['sidewalk'].isnull().sum()
        df['sidewalk'].fillna('NoDamage', inplace=True)
        logger.info(f"Filled {missing_before} missing values in 'sidewalk' column with 'NoDamage'.")

    # Convert 'created_at' column to datetime format
    if 'created_at' in df.columns:
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        logger.info("Converted 'created_at' column to datetime format.")

    # Drop rows where 'tree_id' is missing (if critical)
    if 'tree_id' in df.columns:
        before_drop = df.shape[0]
        df = df.dropna(subset=['tree_id'])
        logger.info(f"Dropped {before_drop - df.shape[0]} rows with missing 'tree_id'.")

    # Additional cleaning steps can be added here in the future (MAYBE) (e.g., filtering out extreme values)

    # Define output path for the cleaned dataset
    output_dir = os.path.join("task1", "data", "processed")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "cleaned_tree_data.csv")

    # Save the cleaned dataset
    df.to_csv(output_file, index=False)
    logger.info(f"Cleaned dataset saved to {output_file}. Final shape: {df.shape[0]} rows, {df.shape[1]} columns.")

    logger.info("Data cleaning process completed successfully.")

except Exception as e:
    logger.exception("An error occurred during data cleaning:")
    raise
