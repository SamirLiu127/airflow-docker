# Airflow LocalExecutor Template

Docker 單機部署的 Apache Airflow 3.1.8 模板，使用 LocalExecutor + PostgreSQL。

## 服務架構

| 服務 | 說明 |
|------|------|
| `airflow-apiserver` | Web UI & REST API (port 8080) |
| `airflow-scheduler` | 排程器，同時執行 tasks |
| `airflow-dag-processor` | DAG 檔案解析器 |
| `postgres:17` | Metadata 資料庫 |

## 快速開始

```bash
# 1. 設置環境變數
cp .env.example .env
# 編輯 .env，填入三組金鑰（產生方式見 .env.example 註解）

# 2. 初始化 & 啟動
make init
make up
```

Web UI: http://localhost:8080　帳號/密碼：`airflow` / `airflow`

## Makefile 指令

```bash
make init     # 初始化資料庫（首次使用）
make up       # 啟動服務
make down     # 停止服務
make restart  # 重啟服務
make clean    # 完全清理（含 volumes & images）
```

## 專案結構

```
├── dags/
│   ├── hello_dag.py       # 範例 DAG
│   └── shared/            # 共享模組（支援熱重載，無需重啟容器）
│       ├── config.py      # default_args & 環境設定
│       └── utils/         # logger 等工具
├── Dockerfile             # 基於 apache/airflow:3.1.8
├── docker-compose.yaml
├── requirements.txt       # 額外 pip 套件
└── .env.example
```

## DAG 開發範例

```python
from airflow.decorators import dag, task
from datetime import datetime
from shared.config import default_dag_args, DAG_ENVIRONMENT
from shared.utils import get_logger

@task
def my_task():
    get_logger("my_dag").info(f"env={DAG_ENVIRONMENT}")

@dag(dag_id='my_dag', start_date=datetime(2025, 1, 1),
     schedule=None, default_args=default_dag_args)
def my_dag():
    my_task()

my_dag()
```

> `DAG_ENVIRONMENT` 由 `AIRFLOW__DAG_ENV` 環境變數控制（預設 `dev`），`prod` 環境自動套用更高的 retries。

## 新增套件

編輯 `requirements.txt` 後執行：

```bash
make clean && make init && make up
```
