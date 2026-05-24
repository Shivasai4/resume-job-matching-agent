import logging
import sys
from pythonjsonlogger import jsonlogger
from app.config import settings


def setup_logging():
    logHandler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    logHandler.setFormatter(formatter)
    root = logging.getLogger()
    root.addHandler(logHandler)
    root.setLevel(logging.getLevelName(settings.log_level))
    # reduce noisy loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)