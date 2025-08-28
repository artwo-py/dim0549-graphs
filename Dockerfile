FROM python:3.12-slim

WORKDIR /app

COPY . /app

ENTRYPOINT ["python", "1-unidade/1-1/"]
CMD ["q1.py"]
