FROM python:3.10
WORKDIR /src
COPY ./requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt
COPY . /src

#RUN python -V
#ENV DATABASE_URL=postgresql+asyncpg://user:password@db:5432/database

#RUN apt install alembic
#RUN alembic revision --autogenerate -m 'create database'

#RUN alembic upgrade head