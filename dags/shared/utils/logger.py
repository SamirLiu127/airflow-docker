"""
統一的日誌工具
用法：from shared.utils.logger import get_logger
"""
import logging
import json
from datetime import datetime


class StructuredLogger:
    """結構化日誌記錄器"""
    
    def __init__(self, name: str, level: str = 'INFO'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # 避免重複添加 handler
        if not self.logger.handlers:
            self._setup_handler()
    
    def _setup_handler(self):
        """設置日誌處理器"""
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def _log_structured(self, level: str, message: str, **context):
        """結構化日誌記錄"""
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': level,
            'message': message,
            **context
        }
        
        # 轉為 JSON 字符串
        json_log = json.dumps(log_data, ensure_ascii=False)
        
        # 根據級別記錄
        if level == 'ERROR':
            self.logger.error(json_log)
        elif level == 'WARNING':
            self.logger.warning(json_log)
        elif level == 'INFO':
            self.logger.info(json_log)
        else:
            self.logger.debug(json_log)
    
    def info(self, message: str, **context):
        """資訊日誌"""
        self._log_structured('INFO', message, **context)
    
    def error(self, message: str, **context):
        """錯誤日誌"""
        self._log_structured('ERROR', message, **context)
    
    def warning(self, message: str, **context):
        """警告日誌"""
        self._log_structured('WARNING', message, **context)
    
    def debug(self, message: str, **context):
        """除錯日誌"""
        self._log_structured('DEBUG', message, **context)


def get_logger(name: str, level: str = 'INFO') -> StructuredLogger:
    """
    取得日誌記錄器
    
    使用範例：
    from shared.utils.logger import get_logger
    
    logger = get_logger('my_dag')
    logger.info('開始處理資料', task_id='extract_data', record_count=100)
    logger.error('處理失敗', error_type='connection_error', retry_count=3)
    """
    return StructuredLogger(name, level)


def log_task_start(task_name: str, **context):
    """任務開始日誌"""
    logger = get_logger('task_monitor')
    logger.info(f'任務開始: {task_name}', task_name=task_name, **context)


def log_task_end(task_name: str, success: bool = True, **context):
    """任務結束日誌"""
    logger = get_logger('task_monitor')
    status = '成功' if success else '失敗'
    logger.info(f'任務結束: {task_name} - {status}', 
                task_name=task_name, success=success, **context)


def log_data_quality(table_name: str, record_count: int, quality_score: float = None):
    """資料品質日誌"""
    logger = get_logger('data_quality')
    logger.info('資料品質檢查', 
                table_name=table_name, 
                record_count=record_count,
                quality_score=quality_score)