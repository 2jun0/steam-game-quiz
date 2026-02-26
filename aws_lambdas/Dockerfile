FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY database_lambda ./database_lambda
COPY daily_quiz ./daily_quiz
COPY game_updater ./game_updater
COPY lambda_job_runner.py ./lambda_job_runner.py

CMD ["python", "lambda_job_runner.py"]
