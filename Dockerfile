FROM python:3.9.7

RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /code/

COPY ./app ./app
COPY ./alembic ./alembic
COPY ./alembic.ini ./
COPY ./pyproject.toml ./

EXPOSE 8000

RUN useradd --shell /bin/sh --no-log-init --system -u 999 api
USER api
CMD uvicorn --host 0.0.0.0 --port $PORT --reload app.main:app --root-path /api