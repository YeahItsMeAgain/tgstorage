FROM tiangolo/uvicorn-gunicorn:latest
COPY ./pyproject.toml ./poetry.lock* ./
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-root --no-interaction --no-ansi
COPY ./app /app/app
COPY .env prestart.sh main.py uvicorn_proxy_worker.py /app/

# For the prestart.sh script.
RUN apt update && apt install -y netcat