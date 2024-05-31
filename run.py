import os
import logging
import schedule
import time
import subprocess
from sqlalchemy.exc import OperationalError
from database import models
from database.config import engine, Base, get_session, create_tables
from database.models import Card
from scrapper import main as scrapper

def setup_logger():
    # Создаем логгер
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Создаем обработчик для записи логов в файл
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.DEBUG)

    # Создаем обработчик для вывода логов в консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Создаем форматтер для логов
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Добавляем обработчики к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def run_daily(logger):
    try:
        # Запускаем приложение
        subprocess.call(["python", "run.py"])
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

def main():
    scrapper.run()

if __name__ == "__main__":
    main()