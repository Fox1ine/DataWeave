from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

@dag(
    default_args={
        "owner": "airflow",
        "depends_on_past": False,
        "start_date": datetime(2025, 2, 26),
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    schedule_interval="0 * * * *",
    catchup=False,
    dag_id="weather_dag",
)
def weather_pipeline():
    start = EmptyOperator(task_id="start")

    @task
    def fetch_weather_data():
        from fetch_weather import fetch_weather_raw
        fetch_weather_raw()

    @task
    def process_weather_data():
        from fetch_weather import process_weather_data
        process_weather_data()

    end = EmptyOperator(task_id="end")

    fetched = fetch_weather_data()
    processed = process_weather_data()

    start >> fetched >> processed >> end

dag = weather_pipeline()
