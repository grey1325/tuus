from datetime import datetime
import logging
import os
from typing import Optional

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# Подключение к MongoDB
client = MongoClient(
    host=os.getenv("MONGO_HOST", "localhost"), port=int(os.getenv("MONGO_PORT", 27017))
)

db = client["sfmshop_logs"]
logs_collection = db["logs"]


class LogServiceMongo:
    def __init__(
        self, connection_string="mongodb://localhost:27017/", db_name="sfmshop"
    ):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.logs_collection = self.db["logs"]

    def log_error(self, message: str, stack_trace: Optional[str] = None):
        """Логировать ошибку"""
        log_entry = {
            "type": "error",
            "message": message,
            "stack_trace": stack_trace,
            "timestamp": datetime.utcnow(),
        }
        self.logs_collection.insert_one(log_entry)

    def log_access(self, ip: str, endpoint: str, method: str, status_code: int):
        """Логировать доступ"""
        log_entry = {
            "type": "access",
            "ip": ip,
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "timestamp": datetime.utcnow(),
        }
        self.logs_collection.insert_one(log_entry)

    def get_errors(self, since: Optional[datetime] = None):
        """Получить ошибки"""
        query = {"type": "error"}
        if since:
            query["timestamp"] = {"$gte": since}
        return list(self.logs_collection.find(query))

    def get_access_logs(self, since: Optional[datetime] = None):
        """Получить логи доступа"""
        query = {"type": "access"}
        if since:
            query["timestamp"] = {"$gte": since}
        return list(self.logs_collection.find(query))

    def save_log(self, log_data):
        """Сохранение лога в MongoDB"""
        # Добавление timestamp если его нет
        if "timestamp" not in log_data:
            log_data["timestamp"] = datetime.now()

        result = logs_collection.insert_one(log_data)
        return result.inserted_id

    def get_all_logs(self):
        """Получение всех логов"""
        return list(logs_collection.find())

    def get_logs_by_type(self, log_type):
        """Получение логов по типу"""
        logs = logs_collection.find({"type": log_type})
        return list(logs)

    def get_error_logs(self):
        """Получение всех ошибок"""
        logs = logs_collection.find({"type": "error"})
        return list(logs)

    def get_logs_status_code(self, log_status_code):
        """Получение логов по коду статуса"""
        logs = logs_collection.find({"status_code": log_status_code})
        return list(logs)

    def get_logs_by_date_range(self, start, end):
        """Получение логов по времени"""
        logs = logs_collection.find({"timestamp": {"$gte": start, "$lt": end}})
        return list(logs)

    def get_logs_by_ip(self, log_ip):
        """Получение логов по IP"""
        logs = logs_collection.find({"ip": log_ip})
        return list(logs)

    def count_logs_by_type(self):
        """Подсчет логов по типу"""
        logs = logs_collection.aggregate(
            [{"$group": {"_id": "$type", "count": {"$sum": 1}}}]
        )
        return list(logs)

    def count_logs_by_status_code(self):
        """Подсчет логов по коду статуса"""
        logs = logs_collection.aggregate(
            [{"$group": {"_id": "$status_code", "count": {"$sum": 1}}}]
        )
        return list(logs)

    def count_logs_by_day(self, start, end):
        """Подсчет логов по дням"""
        logs = logs_collection.aggregate(
            [
                {"$match": {"timestamp": {"$gte": start, "$lt": end}}},
                {
                    "$group": {
                        "_id": {
                            "$dateToString": {
                                "format": "%Y-%m-%d",
                                "date": "$timestamp",
                            }
                        },
                        "count": {"$sum": 1},
                    }
                },
            ]
        )
        return list(logs)


class LogService:
    """Сервис логирования для проекта SFMShop"""

    def __init__(self, log_file: str = "app.log"):
        """Инициализация сервиса логирования"""
        # Настройка логирования
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
        )

        self.logger = logging.getLogger(__name__)

    def info(self, message: str, **kwargs):
        """Логирование информационного сообщения"""
        self.logger.info(f"{message} | {kwargs}")

    def error(self, message: str, **kwargs):
        """Логирование ошибки"""
        self.logger.error(f"{message} | {kwargs}")

    def warning(self, message: str, **kwargs):
        """Логирование предупреждения"""
        self.logger.warning(f"{message} | {kwargs}")

    def critical(self, message: str, **kwargs):
        """Логирование критической ошибки"""
        self.logger.critical(f"{message} | {kwargs}")
        self.send_alert(message)

    def debug(self, message: str, **kwargs):
        """Логирование отладочного сообщения"""
        self.logger.debug(f"{message} | {kwargs}")

    # В реальном проекте здесь может быть интеграция с Sentry,
    # Telegram, Slack или Email для уведомления о критических ошибках.
    def send_alert(self, message: str):
        print(f"Alert: {message}")


# Глобальный экземпляр
log_service = LogService()
