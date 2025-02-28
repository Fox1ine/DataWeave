import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

DATA_PATH = os.getenv("DATA_RAW_PATH")


DB_CONFIG = {
    "project_a": {
        "url": os.getenv("PROJECT_A_DB_URL"),
        "tables": {
            "user_sessions": "project_a_user_sessions.csv",
            "pages": "project_a_pages.csv",
            "events": "project_a_events.csv"
        }
    },
    "project_b": {
        "url": os.getenv("PROJECT_B_DB_URL"),
        "tables": {
            "user_sessions": "project_b_user_sessions.csv",
            "pages": "project_b_pages.csv",
            "events": "project_b_events.csv"
        }
    },
    "project_c": {
        "url": os.getenv("PROJECT_C_DB_URL"),
        "tables": {
            "user_sessions": "project_c_user_sessions.csv",
            "pages": "project_c_pages.csv",
            "events": "project_c_events.csv"
        }
    },
    "analytics": {
        "url": os.getenv("ANALYTICS_DB_URL"),
        "tables": {
            "transactions": "transactions.csv",
            "exchange_rates": "exchange_rates.csv"
        }
    }
}

def load_csv_to_db(db_name, table_name, file_path, db_url):
    try:
        # Преобразуем URL для psycopg2 (убираем префикс +psycopg2)
        dsn = db_url.replace("postgresql+psycopg2://", "postgresql://")
        conn = psycopg2.connect(dsn)
        cur = conn.cursor()
        with open(file_path, 'r', encoding='utf-8') as f:
            # Формируем команду COPY с указанием имени таблицы
            copy_sql = sql.SQL("COPY {} FROM STDIN WITH CSV HEADER").format(sql.Identifier(table_name))
            cur.copy_expert(copy_sql, f)
        conn.commit()
        cur.close()
        conn.close()
        print(f"[{db_name}] Данные успешно загружены в таблицу '{table_name}' из файла {file_path}")
    except Exception as e:
        print(f"[{db_name}] Ошибка при загрузке таблицы '{table_name}' из файла {file_path}: {e}")

def main():
    for db_name, config in DB_CONFIG.items():
        db_url = config["url"]
        for table_name, filename in config["tables"].items():
            file_path = os.path.join(DATA_PATH, filename)
            if os.path.exists(file_path):
                load_csv_to_db(db_name, table_name, file_path, db_url)
            else:
                print(f"[{db_name}] Файл не найден: {file_path}")

if __name__ == "__main__":
    main()
