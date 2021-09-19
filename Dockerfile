FROM python:3.9.7

RUN useradd --create-home --shell /bin/bash --no-log-init --system -u 999 api
USER api

RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /code/

COPY --chown=api:api ./app ./app
COPY --chown=api:api ./alembic ./alembic
COPY --chown=api:api ./alembic.ini ./

EXPOSE 8000

ENV PATH="/home/api/.local/bin:${PATH}"

CMD ["uvicorn", "--host", "0.0.0.0", "--reload", "app.main:app" ]