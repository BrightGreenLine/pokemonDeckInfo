# syntax=docker/dockerfile:1

FROM python:3.11.4-slim
WORKDIR /app

# install psycopg2 dependencies
RUN apt-get update 
RUN apt-get -y install gcc libpq-dev 

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 80/TCP 

COPY . .

CMD ["flask","run"]