import os
import psycopg2
from dotenv import load_dotenv
from task1.logging_config import logger

# Load environment variables from .env
load_dotenv()
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")


try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    logger.info("Connection to PostgreSQL is successful!")
    conn.close()
except ConnectionError as e:
    logger.error(f"Connection error: {e}")
    raise
