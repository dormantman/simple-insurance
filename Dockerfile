FROM python:3.8

EXPOSE 8080

ENV PYTHONUNBUFFERED=1

RUN mkdir /app/
WORKDIR /app/

COPY ./requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY ./app/ /app/
WORKDIR /app/
