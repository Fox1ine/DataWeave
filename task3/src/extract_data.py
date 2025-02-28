import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from task3.src.logg_config import logger


dotenv_path = "/opt/airflow/.env"
logger.info(f"Loading .env from: {dotenv_path}")
load_dotenv(dotenv_path)

extracted_data_path = os.getenv("EXTRACTED_DATA_PATH")
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # task3/

full_extracted_path = os.path.join(base_dir, extracted_data_path)
os.makedirs(full_extracted_path, exist_ok=True)

logger.info(f"Data will be saved to: {full_extracted_path}")

# Dynamically load connections for all projects
DB_CONNECTIONS = {
    f"project_{i}": os.getenv(f"PROJECT_{i}_DB_URL")
    for i in range(1, 11) if os.getenv(f"PROJECT_{i}_DB_URL")
}

def extract_data():
    sessions_list = []
    events_list = []

    for project, db_url in DB_CONNECTIONS.items():
        logger.info(f"Extracting data from {project}...")
        engine = create_engine(db_url)

        sessions_query = "SELECT * FROM user_sessions"
        df_sessions = pd.read_sql(sessions_query, engine)

        events_query = """
        SELECT user_id, id AS session_id, COUNT(*) AS events_count 
        FROM events 
        GROUP BY user_id, id
        """
        df_events = pd.read_sql(events_query, engine)

        df_sessions["project"] = project
        df_events["project"] = project

        sessions_list.append(df_sessions)
        events_list.append(df_events)

    df_sessions_all = pd.concat(sessions_list, ignore_index=True)
    df_events_all = pd.concat(events_list, ignore_index=True)

    df_sessions_all = df_sessions_all.merge(
        df_events_all, how="left", left_on=["id", "user_id", "project"], right_on=["session_id", "user_id", "project"]
    )
    df_sessions_all["events_count"] = df_sessions_all["events_count"].fillna(0).astype(int)
    df_sessions_all = df_sessions_all.drop(columns=["session_id"])

    logger.info("Data extraction completed successfully!")
    output_file = os.path.join(full_extracted_path, "extracted_sessions.csv")
    df_sessions_all.to_csv(output_file, index=False)

    logger.info(f"data saved to {output_file}")

if __name__ == "__main__":
    extract_data()
