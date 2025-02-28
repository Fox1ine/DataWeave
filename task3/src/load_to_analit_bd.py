import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from task3.src.logg_config import logger

dotenv_path = "/opt/airflow/.env"
load_dotenv(dotenv_path)

# Get paths from .env
enriched_data_path = os.getenv("ENRICHED_DATA_PATH")
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

full_enriched_path = os.path.join(base_dir, enriched_data_path)
analytics_db_url = os.getenv("ANALYTICS_DB_URL")
engine = create_engine(analytics_db_url)

enriched_sessions_file = os.path.join(full_enriched_path, "enriched_sessions.csv")

def get_last_session_date():
    query = "SELECT MAX(created_at) FROM analytics_sessions"
    with engine.connect() as conn:
        result = conn.execute(text(query)).fetchone()
    return result[0] if result and result[0] else None

def get_next_session_id():
    query = "SELECT COALESCE(MAX(session_id), 0) + 1 FROM analytics_sessions"
    with engine.connect() as conn:
        result = conn.execute(text(query)).fetchone()
    return result[0]

def load_data_to_db():
    logger.info("Starting data load process.")
    df_sessions = pd.read_csv(enriched_sessions_file)
    df_sessions["created_at"] = pd.to_datetime(df_sessions["created_at"])

    next_session_id = get_next_session_id()
    df_sessions.insert(0, "session_id", range(next_session_id, next_session_id + len(df_sessions)))

    df_sessions.to_sql("analytics_sessions", engine, if_exists="append", index=False)
    logger.info("Data successfully loaded into analytics_sessions table.")

if __name__ == "__main__":
    load_data_to_db()
