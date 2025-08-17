# 🚁 Apache Airflow 3.0.4 快速建構專案

一個基於 Docker 的 Apache Airflow 3.0.4 快速啟動模板，專為資料挖掘和 ETL 管道開發設計。

## ✨ 特色

- 🐳 **Docker 容器化**: 一鍵啟動完整 Airflow 環境
- ⚡ **Airflow 3.0.4**: 最新版本，支援 TaskFlow API
- 🔧 **開箱即用**: 預配置開發環境和工具
- 📁 **智能模組管理**: 解決 shared 模組導入問題
- 🎯 **GCP Composer 相容**: 支援雲端部署
- 📋 **Makefile 工具**: 簡化開發操作

## 🚀 快速開始

### 1. 克隆專案
```bash
git clone <repository-url>
cd airflow
```

### 2. 建立必要目錄
```bash
mkdir -p ./dags ./logs ./plugins ./config
```

### 3. 設置環境變數
```bash
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
```

### 4. 一鍵啟動
```bash
make quickstart
```

### 5. 訪問 Web UI
打開瀏覽器訪問: http://localhost:8080

**註**: 由於已設定 `AIRFLOW__CORE__SIMPLE_AUTH_MANAGER_ALL_ADMINS=true`，無需登入即可使用所有功能。

## 📂 專案結構

```
airflow/
├── dags/                    # DAG 定義
│   ├── simple_dag.py        # 簡單測試 DAG
│   ├── test_dag.py          # 配置測試 DAG
│   └── shared/              # 共享工具模組
│       ├── config/          # 配置管理 (Pydantic)
│       └── utils/           # 工具函數
├── plugins/                 # Airflow 插件
├── config/                  # 環境配置
├── logs/                    # 執行日誌
├── .env                     # 環境變數
├── docker-compose.yaml      # Docker 服務
├── Dockerfile              # 自定義映像檔
├── requirements.txt        # Python 依賴
└── Makefile               # 開發工具
```

## 🛠️ 常用指令

### 基本操作
```bash
make up          # 啟動服務
make down        # 停止服務
make restart     # 重啟服務
make logs        # 查看日誌
make shell       # 進入容器
```

### DAG 管理
```bash
make dag-list                        # 列出所有 DAG
make dag-trigger DAG_ID=simple_dag   # 觸發 DAG
make dag-test DAG_ID=simple_dag      # 測試 DAG
```

### 維護除錯
```bash
make status      # 檢查服務狀態
make clean       # 完全清理重置
make rebuild     # 重建映像檔並重啟
```

## 📝 DAG 開發範例

使用 TaskFlow API 建立新的 DAG：

```python
from airflow.decorators import dag, task
from datetime import datetime
from shared.config.settings import get_config

@task
def extract_data():
    """資料萃取任務"""
    config = get_config()
    print(f"連接資料庫: {config.database.host}")
    return "萃取完成"

@task
def transform_data(data):
    """資料轉換任務"""
    print(f"轉換資料: {data}")
    return "轉換完成"

@dag(
    dag_id='my_etl_pipeline',
    start_date=datetime(2025, 1, 1),
    schedule=None,
    tags=['etl', 'example']
)
def my_etl_pipeline():
    """我的 ETL 管道"""
    extracted = extract_data()
    transformed = transform_data(extracted)

# 建立 DAG 實例
my_etl_pipeline()
```

## ⚙️ 配置管理

### 環境變數配置 (.env)
```bash
# 資料庫設定
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=analytics

# ETL 設定
ETL_BATCH_SIZE=1000
ETL_RETRY_COUNT=3

# 監控設定
MONITORING_ENABLED=true
LOG_LEVEL=INFO
```

### Pydantic 配置類別
```python
# dags/shared/config/settings.py
from pydantic_settings import BaseSettings
from pydantic import Field

class DatabaseConfig(BaseSettings):
    host: str = Field(default="localhost")
    port: int = Field(default=5432)
    name: str = Field(default="airflow")
    
    class Config:
        env_prefix = "DATABASE_"
        env_file = ".env"

def get_config():
    return DatabaseConfig()
```

## 🔧 Airflow 3.0.4 特色

### TaskFlow API
- 使用 `@task` 裝飾器替代傳統 Operator
- 自動處理 XCom 和任務依賴
- 更簡潔的程式碼結構

### 微服務架構
- `airflow-apiserver`: API 服務和 Web UI
- `airflow-scheduler`: 排程器
- `airflow-dag-processor`: DAG 處理器
- `airflow-triggerer`: 觸發器服務

### 模組導入解決方案
- `shared/` 模組放在 `dags/` 目錄下
- 自動重新載入，無需重啟容器
- 避免 `plugins/` 目錄的重啟限制

## 🚀 部署到 GCP Composer

### 1. 準備部署檔案
```bash
# 打包 DAGs 和 shared 模組
tar -czf dags.tar.gz dags/

# 上傳 requirements.txt
gsutil cp requirements.txt gs://your-composer-bucket/
```

### 2. 部署到 Composer
```bash
# 建立 Composer 環境
gcloud composer environments create my-airflow-env \
    --location=asia-east1 \
    --airflow-version=3.0.4

# 上傳 DAGs
gcloud composer environments storage dags import \
    --environment=my-airflow-env \
    --location=asia-east1 \
    --source=dags/
```

## 📦 依賴管理

### 新增 Python 套件
1. 編輯 `requirements.txt`
2. 重建映像檔: `make rebuild`

## 🤝 貢獻指南

1. Fork 專案
2. 建立功能分支: `git checkout -b feature/new-feature`
3. 提交變更: `git commit -am 'Add new feature'`
4. 推送分支: `git push origin feature/new-feature`
5. 建立 Pull Request

## 📄 授權

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

## 🆘 支援

- 📚 [Apache Airflow 官方文件](https://airflow.apache.org/docs/)
- 🐛 [問題回報](../../issues)
- 💬 [討論區](../../discussions)

---

**快速開始指令**: `make quickstart` 🚀