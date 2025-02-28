import os
import psycopg2
from dotenv import load_dotenv
from task1.logging_config import logger


dotenv_path = os.getenv("DOTENV_PATH")
load_dotenv(dotenv_path)

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")

SQL_FILE_PATH = os.getenv("CREATE_TABLE_SQL_PATH")


try:
    logger.info("Connecting to PostgreSQL to create the table...")

    # Establish connection to PostgreSQL
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()

    # Read and execute the SQL script
    with open(SQL_FILE_PATH, "r") as sql_file:
        sql_commands = sql_file.read()
        cur.execute(sql_commands)
        conn.commit()

    logger.info("Table 'nyc_trees' created successfully in PostgreSQL.")

    cur.close()
    conn.close()

except Exception as e:
    logger.exception("An error occurred while creating the table:")
    raise
