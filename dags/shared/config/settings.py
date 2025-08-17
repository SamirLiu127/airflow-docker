"""
使用 Pydantic + .env 的配置管理工具
用法：from shared.config.settings import get_config, AppConfig
"""
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from airflow.models import Variable


class DatabaseConfig(BaseSettings):
    """資料庫配置"""
    host: str = Field(default="localhost", description="資料庫主機")
    port: int = Field(default=5432, description="資料庫端口")
    database: str = Field(default="airflow", description="資料庫名稱")
    user: str = Field(default="airflow", description="使用者名稱")
    password: str = Field(default="airflow", description="密碼")
    
    class Config:
        env_prefix = "DATABASE_"  # 環境變數前綴：DATABASE_HOST, DATABASE_PORT 等
        env_file = ".env"


class AppConfig(BaseSettings):
    """應用程式配置 - 純 .env 方式"""
    environment: str = Field(default="development", description="環境")
    debug: bool = Field(default=False, description="除錯模式")
    
    class Config:
        env_file = ".env"  # 支援 .env 檔案
    
    @property
    def database(self) -> DatabaseConfig:
        """取得資料庫配置"""
        return DatabaseConfig()


# 全域配置實例
_app_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """
    取得應用程式配置
    
    使用範例：
    from shared.config.settings import get_config
    
    config = get_config()
    print(config.database.host)  # 從 .env 中讀取 DATABASE_HOST
    print(config.etl.batch_size)  # 從 .env 中讀取 ETL_BATCH_SIZE
    """
    global _app_config
    if _app_config is None:
        _app_config = AppConfig()
    return _app_config


def get_airflow_variable(key: str, default_value=None, deserialize_json: bool = False):
    """
    從 Airflow Variables 取得值，支援 fallback 到配置
    
    使用範例：
    batch_size = get_airflow_variable('ETL_BATCH_SIZE', get_config().etl.batch_size)
    """
    try:
        return Variable.get(key, default_var=default_value, deserialize_json=deserialize_json)
    except Exception:
        return default_value


def set_airflow_variable(key: str, value, serialize_json: bool = False):
    """設定 Airflow Variable"""
    Variable.set(key, value, serialize_json=serialize_json)


# 常用快捷函數
def get_database_config() -> DatabaseConfig:
    """取得資料庫配置"""
    return get_config().database


if __name__ == "__main__":
    print(get_database_config())