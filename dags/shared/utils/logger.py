import logging

from shared.config import DAG_ENVIRONMENT


def get_logger(name: str):
    """
    取得日誌記錄器（單例）

    Args:
        name: Logger 名稱，建議使用 DAG ID 或模組名稱

    Returns:
        標準 logging.Logger 實例，直接使用以避免 Airflow 顯示錯誤的檔案名稱

    Examples:
        >>> logger = get_logger('my_dag')
        >>> logger.info('開始處理資料')
        >>> logger.info('處理完成')
    """
    logger = logging.getLogger(name)
    logger_level = logging.INFO if DAG_ENVIRONMENT == "prod" else logging.DEBUG
    logger.setLevel(logger_level)
    return logger
