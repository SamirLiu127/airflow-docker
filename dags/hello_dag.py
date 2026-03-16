from datetime import datetime

from airflow.decorators import dag, task

from shared.config import default_dag_args, DAG_ENVIRONMENT
from shared.utils import get_logger


@task
def hello_world():
    logger = get_logger("debug")
    logger.info(f"Hello World!!!({DAG_ENVIRONMENT=})")

@dag(
    dag_id='hello_dag',
    start_date=datetime(2025, 1, 1),
    schedule=None,
    tags=['example', 'test'],
    description='A simple Airflow test DAG',
    default_args=default_dag_args,
)
def hello_dag():
    """測試 DAG"""
    hello_world()


hello_dag()
