FROM python:3.9-alpine3.16

COPY requirements.txt /temp/requirements.txt
# пакеты для подключения к pg
RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user

# слева локальное, справа контейнерное
COPY service /service
WORKDIR /service
EXPOSE 8000


USER service-user