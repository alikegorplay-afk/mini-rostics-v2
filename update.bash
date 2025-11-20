#!/bin/bash

# Останавливаем и удаляем только наш контейнер
docker stop my-app 2>/dev/null || true
docker rm my-app 2>/dev/null || true

git pull origin main

docker build -t app .
docker run -d -p 8000:8000 --name my-app -v app-data:/app/data app