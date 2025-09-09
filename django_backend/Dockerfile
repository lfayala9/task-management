FROM python:3.12-slim

WORKDIR /app

RUN pip install --upgrade pip

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY requirements.txt  /app/

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest pytest-django

COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]