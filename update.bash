docker stop $(docker ps -aq) 2>/dev/null || true
docker rm $(docker ps -aq) 2>/dev/null || true

git pull origin main

docker build -t app .
docker run -d -p 8000:8000 --name my-app app