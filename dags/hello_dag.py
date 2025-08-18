from airflow.decorators import dag, task
from datetime import datetime, timedelta

from shared.config.settings import get_config

@task
def hello_world():
    print("Hello World!!!")
    return "Hello World 完成"

@task
def hello_config():
    print("Now is: ", datetime.now())
    try:
        config = get_config()  # 暫時註解掉
        print(f"Database host: {config.database.host}")
        print("模擬配置載入成功")
        return "Config 載入成功 (模擬)"
    except Exception as e:
        print(f"Config 載入失敗: {e}")
        return f"Config 載入失敗: {e}"


default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(seconds=3),
}

@dag(
    dag_id='hello_dag',
    start_date=datetime(2025, 1, 1),
    schedule=None,
    tags=['example', 'test'],
    description='A simple Airflow test DAG',
    default_args=default_args,
)
def hello_dag():
    """測試 DAG"""
    hello_world() >> hello_config()

# 建立 DAG 實例 
hello_dag_instance = hello_dag()
