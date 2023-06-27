# syntax=docker/dockerfile:1

FROM python:3.11.4-slim
WORKDIR /app

# install psycopg2 dependencies
RUN apt-get update 
RUN apt-get -y install gcc libpq-dev 

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 6969/TCP 

COPY . .

RUN export DOCKER_HOST_IP=$(route -n | awk '/UG[ \t]/{print $2}')
CMD ["flask","run", "--host=0.0.0.0", "--port=6969"]