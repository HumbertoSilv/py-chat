import inspect
import logging
import sys

from loguru import logger as loguru_logger

from py_chat.core.config import Settings

settings = Settings()


class InterceptHandler(logging.Handler):
    @staticmethod
    def emit(record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        try:
            level: str | int = loguru_logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame:
            filename = frame.f_code.co_filename
            is_logging = filename == logging.__file__
            is_frozen = 'importlib' in filename and '_bootstrap' in filename
            if depth > 0 and not (is_logging or is_frozen):
                break
            frame = frame.f_back
            depth += 1

        loguru_logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logger():
    log_level = settings.LOG_LEVEL
    log_format = (
        '<green>{time:YYYY-MM-DD HH:mm:ss}</green> | '
        '<level>{level: <8}</level> | '
        '<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - '
        '<level>{message}</level>'
    )
    loguru_logger.remove()

    loguru_logger.level('DEBUG', color='<white>')
    loguru_logger.level('INFO', color='<white>')
    loguru_logger.level('SUCCESS', color='<green>')
    loguru_logger.level('WARNING', color='<yellow>')
    loguru_logger.level('ERROR', color='<red>')
    loguru_logger.level('CRITICAL', color='<RED><bold>')

    loguru_logger.add(
        sys.stdout,
        level=log_level,
        format=log_format,
    )

    # Intercepta logs do logging padrão
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # Redireciona loggers específicos para o Loguru
    for name in ('uvicorn', 'uvicorn.error', 'uvicorn.access', 'fastapi'):
        logging.getLogger(name).handlers = [InterceptHandler()]
        logging.getLogger(name).propagate = False

    return loguru_logger


logger = setup_logger()
