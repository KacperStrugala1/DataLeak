from loguru import logger

logger.add(
    "debug.log",
    rotation="10 MB",
    retention="10 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} - {level} - {file}:{line} - {message}"
)