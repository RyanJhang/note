
import datetime
import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

import structlog


def create_std_logger(folder_path):
    def log_handler():
        server_num = os.environ.get("SERVER_NUM", "dev")
        log_filename = datetime.datetime.now().strftime(
            f"api_server_{server_num}.%Y-%m-%d.log")
        handler = TimedRotatingFileHandler(
            os.path.join(folder_path, log_filename), when="D", interval=1, backupCount=15, encoding="UTF-8", delay=False, utc=True)
        handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")
        handler.setFormatter(formatter)
        return handler

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.DEBUG,
    )

    root_logger = logging.getLogger("root")
    root_logger.addHandler(log_handler())
    root_logger.debug("Root logger created")
    return root_logger


def create_json_logger(folder_path):
    def json_handler():
        server_num = os.environ.get("SERVER_NUM", "dev")
        log_filename = datetime.datetime.now().strftime(
            f"api_server_{server_num}.%Y-%m-%d.json")

        handler = TimedRotatingFileHandler(

            os.path.join(folder_path, log_filename), when="D", interval=1, backupCount=15, encoding="UTF-8", delay=False, utc=True)
        handler.setLevel(logging.DEBUG)
        return handler

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    json_logger = structlog.get_logger("json")
    json_logger.addHandler(json_handler())
    json_logger.debug("Json logger created")
    return json_logger
