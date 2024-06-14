FROM bitnami/spark:3.5.0

RUN pip install --no-cache-dir kafka-python numpy python-dotenv delta-spark minio

ENV ACTION consumer

ENV BOOTSTRAP_SERVERS "broker-1:29091,broker-2:29092,broker-3:29093"

ADD . /src

# ADD spark-setup.sh /src/spark-setup.sh

