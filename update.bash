#!/bin/bash

# Получаем последние изменения из репозитория
git pull origin main

# Останавливаем и удаляем сервисы
docker-compose down

# Пересобираем и запускаем
docker-compose build --no-cache
docker-compose up -d