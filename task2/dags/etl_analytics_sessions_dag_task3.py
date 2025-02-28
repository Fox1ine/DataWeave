from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
import subprocess
import os


from dotenv import load_dotenv
load_dotenv("/opt/airflow/.env")

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 2, 26),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

@dag(
    default_args=default_args,
    schedule_interval="*/10 * * * *",
    catchup=False,
    dag_id="etl_analytics_sessions",
)
def etl_pipeline():
    start = EmptyOperator(task_id="start")

    projects = os.getenv("PROJECTS", "").split(",")

    extract_tasks = []
    enrich_tasks = []
    load_tasks = []

    for project in projects:
        project = project.strip()
        if not project:
            continue

        @task(task_id=f"extract_{project}")
        def extract(project=project):
            subprocess.run(["python", "/opt/airflow/scripts/extract_data.py", project], check=True)

        @task(task_id=f"enrich_{project}")
        def enrich(project=project):
            subprocess.run(["python", "/opt/airflow/scripts/enrich_data.py", project], check=True)

        @task(task_id=f"load_{project}")
        def load(project=project):
            subprocess.run(["python", "/opt/airflow/scripts/load_to_analit_bd.py", project], check=True)

        extract_task = extract()
        enrich_task = enrich()
        load_task = load()

        extract_tasks.append(extract_task)
        enrich_tasks.append(enrich_task)
        load_tasks.append(load_task)

    end = EmptyOperator(task_id="end")

    start >> extract_tasks >> enrich_tasks >> load_tasks >> end

dag = etl_pipeline()
