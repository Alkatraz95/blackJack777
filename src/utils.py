# src/utils.py
from .logger_config import get_module_logger

# Создаем логгер с именем "utils"
logger = get_module_logger("utils")

def some_utility_function():
    logger.info("Работает функция из utils.py")
