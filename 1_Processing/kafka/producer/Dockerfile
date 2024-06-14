FROM --platform=amd64 python:3.11-alpine

RUN pip install --no-cache-dir kafka-python numpy python-dotenv 

ENV ACTION produce

ENV BOOTSTRAP_SERVERS "broker-1:29091,broker-2:29092,broker-3:29093"

COPY . /src

# ADD ./run.sh /src/run.sh

