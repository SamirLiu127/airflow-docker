import os
from datetime import timedelta

DAG_ENVIRONMENT = os.getenv("AIRFLOW__DAG_ENV", "dev")

# Default arguments for all tasks
default_dag_args = {
    "owner": "Samir Liu",
    "retries": 3 if DAG_ENVIRONMENT == "prod" else 1,
    "retry_delay": timedelta(minutes=1) if DAG_ENVIRONMENT == "prod" else timedelta(seconds=5),
}
