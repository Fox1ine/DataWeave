import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from task3.src.logg_config import logger

dotenv_path = os.getenv("DOTENV_PATH")
load_dotenv(dotenv_path)

extracted_data_path = os.getenv("EXTRACTED_DATA_PATH")
enriched_data_path = "data/enriched_sessions"

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
extracted_data_path = os.path.join(base_dir, extracted_data_path)
enriched_data_path = os.path.join(base_dir, enriched_data_path)

os.makedirs(enriched_data_path, exist_ok=True)

analytics_db_url = os.getenv("ANALYTICS_DB_URL")
engine_analytics = create_engine(analytics_db_url)

extracted_sessions_file = os.path.join(extracted_data_path, "extracted_sessions.csv")


def enrich_sessions():
    """Enrich session data with transactions and exchange rates"""
    logger.info("Starting session enrichment process.")

    # Load extracted session data
    df_sessions = pd.read_csv(extracted_sessions_file)
    df_sessions["session_date"] = pd.to_datetime(df_sessions["last_activity_at"]).dt.date
    logger.info(f"Loaded session data: {df_sessions.shape}")

    # Extract transactions and exchange rates
    transactions_query = """
    SELECT user_id, created_at, amount, currency, success
    FROM transactions
    WHERE success = true
    """
    df_transactions = pd.read_sql(transactions_query, engine_analytics)
    df_transactions["created_date"] = pd.to_datetime(df_transactions["created_at"]).dt.date

    exchange_rates_query = """
    SELECT currency_from, currency_to, exchange_rate, currency_date
    FROM exchange_rates
    """
    df_exrates = pd.read_sql(exchange_rates_query, engine_analytics)
    df_exrates["currency_date"] = pd.to_datetime(df_exrates["currency_date"]).dt.date

    logger.info(f"Loaded transactions: {df_transactions.shape}")
    logger.info(f"Loaded exchange rates: {df_exrates.shape}")

    # Group transactions by user and date
    df_trans_grouped = df_transactions.groupby(["user_id", "created_date"]).agg({
        "amount": "sum"
    }).reset_index()
    df_trans_grouped.rename(columns={"amount": "transactions_sum"}, inplace=True)

    # Merge exchange rates and convert amount to USD
    df_trans_grouped = df_trans_grouped.merge(
        df_exrates,
        left_on=["created_date"],
        right_on=["currency_date"],
        how="left"
    )
    df_trans_grouped["transactions_sum_usd"] = df_trans_grouped["transactions_sum"] * df_trans_grouped["exchange_rate"]
    df_trans_grouped = df_trans_grouped[["user_id", "created_date", "transactions_sum_usd"]]

    # Find the first successful transaction per user and date
    df_first_trans = df_transactions.sort_values(by=["created_at"]).groupby(
        ["user_id", "created_date"]).first().reset_index()
    df_first_trans = df_first_trans.merge(
        df_exrates,
        left_on=["created_date"],
        right_on=["currency_date"],
        how="left"
    )
    df_first_trans["first_successful_transaction_usd"] = df_first_trans["amount"] * df_first_trans["exchange_rate"]
    df_first_trans = df_first_trans[["user_id", "created_date", "created_at", "first_successful_transaction_usd"]]
    df_first_trans.rename(columns={"created_at": "first_successful_transaction_time"}, inplace=True)

    # Merge session data with transactions
    df_sessions = df_sessions.merge(
        df_trans_grouped,
        left_on=["user_id", "session_date"],
        right_on=["user_id", "created_date"],
        how="left"
    ).drop(columns=["created_date"])

    df_sessions = df_sessions.merge(
        df_first_trans,
        left_on=["user_id", "session_date"],
        right_on=["user_id", "created_date"],
        how="left"
    ).drop(columns=["created_date"])

    df_sessions["transactions_sum_usd"] = df_sessions["transactions_sum_usd"].fillna(0)
    df_sessions["first_successful_transaction_usd"] = df_sessions["first_successful_transaction_usd"].fillna(0)

    logger.info("Session enrichment completed successfully!")

    # Save enriched data
    output_file = os.path.join(enriched_data_path, "enriched_sessions.csv")
    df_sessions.to_csv(output_file, index=False)
    logger.info(f"Data saved to {output_file}")


if __name__ == "__main__":
    enrich_sessions()
