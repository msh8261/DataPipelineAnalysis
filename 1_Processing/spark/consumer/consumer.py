#!/usr/bin/env python3
import json
import os
import logging
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField,IntegerType,FloatType,StringType
from pyspark.sql.functions import from_json, col, udf


list_topics = os.getenv("TOPICS").split(",")
bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS", 'localhost:9091,localhost:9092,localhost:9093').split(',')

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s:%(funcName)s:%(levelname)s:%(message)s"
)


spark = SparkSession \
    .builder \
    .appName("Spark Kafka Streaming Data Pipeline") \
    .master("local[*]") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR") 



def stream_to_dataframe():
    return 1

def spark_dataframe():
    return 1


def process_message():
    pass


def write_data():
    pass





if __name__ == "__main__":
    print()

