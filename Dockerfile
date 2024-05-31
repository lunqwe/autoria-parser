FROM python:3.9-slim

# Установка зависимостей для Selenium и Firefox
RUN apt-get update && apt-get install -y \
    wget \
    firefox-esr \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Установка GeckoDriver
RUN wget -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz \
    && tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin \
    && rm /tmp/geckodriver.tar.gz \
    && chmod +x /usr/local/bin/geckodriver

# Создание директории приложения
WORKDIR /app

# Копирование файлов проекта в контейнер
COPY . .

# Установка зависимостей Python
RUN pip install --no-cache-dir -r req.txt

# Команда для запуска приложения
CMD ["python", "run.py"]