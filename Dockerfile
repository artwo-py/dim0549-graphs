FROM python:3.12-alpine

WORKDIR /app

RUN apk update && apk add --no-cache graphviz

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "main.py"]