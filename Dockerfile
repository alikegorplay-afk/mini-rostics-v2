FROM python:3.13.9-slim

WORKDIR /app

RUN mkdir -p /app/data
RUN mkdir -p /app/data/database
RUN mkdir -p /app/data/img

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME ["/app/data"]

CMD ["python", "main.py"]