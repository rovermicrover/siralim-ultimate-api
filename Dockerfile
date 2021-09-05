FROM python:3.9.6

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /code/

COPY ./app ./app
COPY ./alembic ./alembic
COPY ./alembic.ini ./
COPY ./import.py ./

EXPOSE 8000

CMD [ "uvicorn", "--host", "0.0.0.0", "--reload", "app.main:app" ]