#!/usr/bin/env python3
import json
import time
import os
import logging
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField,IntegerType,FloatType,StringType
from pyspark.sql.functions import from_json, col, udf, size, split
import uuid


list_topics = os.getenv("TOPICS").split(",")
bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS", "localhost:9091,localhost:9092,localhost:9093")


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s:%(funcName)s:%(levelname)s:%(message)s"
)


spark = SparkSession \
    .builder \
    .appName("Spark Kafka Streaming Data Pipeline") \
    .master("local[*]") \
    .config("spark.executor.memory", "4g")\
    .config("spark.driver.memory", "4g")\
    .config("spark.cores.max", "2")\
    .config("spark.cassandra.connection.host","cassandra") \
    .config("spark.cassandra.connection.port","9042") \
    .config("spark.cassandra.auth.username","cassandra") \
    .config("spark.cassandra.auth.password","cassandra") \
    .config("spark.driver.host", "localhost")\
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR") 



class BatchStream(object):
    def __init__(self, topic):
        self.topic = topic

    def save_to_cassandra(self, df, epoch_id):
        """
        Save data to Cassandra database.
        Args:
            df : The DataFrame to be written to the table.
            epoch_id : id.
        Returns:
            None
        Raises:
            Exception: If an error occurs while writing the DataFrame to the table.
        """
        try:
            print("Printing epoch_id: ")
            print(epoch_id)  
            df.write \
                .format("org.apache.spark.sql.cassandra")\
                .mode('append')\
                .options(table=f"{self.topic}_table", keyspace=f"{self.topic}_ks")\
                .save()  
            logging.info(f"{epoch_id} saved to Cassandra table: {self.topic}")
        except Exception as e:
            logging.error(f"Failed to save to cassandra table: {self.topic}")

    def save_to_postgres(self, df, epoch_id):
        """
        Save data to PosrgreSQL database.
        Args:
            df : The DataFrame to be written to the table.
            epoch_id : id.
        Returns:
            None
        Raises:
            Exception: If an error occurs while writing the DataFrame to the table.
        """
        try:
            db_credentials = {
                "user": "user",
                "password": "secret",
                "driver" : "org.postgresql.Driver"
            }

            print("Printing epoch_id: ")
            print(epoch_id)
            
            df.write \
                .jdbc(
                url="jdbc:postgresql://postgres:5432/dvd_rentals_lake_db",
                table=f"schema_dvd_rentals.{self.topic}",
                mode="append",
                properties=db_credentials
                )  
            logging.info(f"{epoch_id} saved to Postgres table: {self.topic}")
        except Exception as e:
            logging.error(f"Failed to save to postgres table: {self.topic}")

    def save_to_mysql(self, df, epoch_id):
        """
        Save data to MySQL database.
        Args:
            df : The DataFrame to be written to the table.
            epoch_id : id.
        Returns:
            None
        Raises:
            Exception: If an error occurs while writing the DataFrame to the table.
        """
        db_credentials = {
            "user": "user",
            "password": "passwd",
            "driver" : "com.mysql.jdbc.Driver" 
            }
        try:
            print("Printing epoch_id: ")
            print(epoch_id)    
            df.write \
                        .jdbc(
                        url="jdbc:mysql://mysql:3306/dvd_rentals_lake_db",
                        table=f"{self.topic}",
                        mode="append",
                        properties=db_credentials
                        )  
            logging.info(f"{epoch_id} saved to MySQL table: {self.topic}")
        except Exception as e:
            logging.error(f"Failed to save to mysql table: {self.topic}")


def stream_to_dataframe(topic):
    """
    Spark Read stream data realtime from kafka.
    Args:
        topic (str): name of table.
    Returns:
        Dataframe:
    Raises:
        Exception: If an error occurs while reading the DataFrame.
    """
    # .option("subscribe", f"{topic}") \
    # .option("subscribe", "actor,category,film,film_actor,film_category,inventory,rental") \
    try:
        input_df = spark \
                    .readStream \
                    .format("kafka") \
                    .option("kafka.bootstrap.servers", bootstrap_servers) \
                    .option("subscribe", f"{topic}") \
                    .option("startingOffsets", "earliest") \
                    .load() 

        input_df.printSchema()     

        logging.info(f"Read {topic} stream successfully.")
        #logging.info(f"Read stream completed successfully.")
        return input_df
    except Exception as e:
        logging.error(f"Failed to read message of topic: {topic}")
        #logging.error(f"Failed to read message")
        return "Faild."



def query_to_cassandra(df, bs, topic, schema):
    """
    Write processed stream data to Cassandra.
    Args:
        df : The DataFrame to be written to the table.
        epoch_id : id.
        topic (str): name of table.
    Returns:
        None
    Raises:
        Exception: If an error occurs while writing the DataFrame to the table.
    """
    try:
        expanded_df = df \
                        .selectExpr("CAST(value AS STRING)") \
                        .select(from_json(col("value"),schema).alias(f"{topic}")) \
                        .select(f"{topic}.*")
        uuid_udf = udf(lambda: str(uuid.uuid4()), StringType()).asNondeterministic()
        expanded_df = expanded_df.withColumn("uuid", uuid_udf())
        expanded_df = expanded_df.select([expanded_df.columns[-1]] + expanded_df.columns[:-1])

        # # Output to Console
        # expanded_df.writeStream \
        #   .outputMode("append") \
        #   .format("console") \
        #   .option("truncate", False) \
        #   .start()             
        
        query = expanded_df.writeStream \
        .trigger(processingTime="15 seconds") \
        .foreachBatch(bs.save_to_cassandra) \
        .outputMode("update") \
        .start()
        query.awaitTermination()
        logging.info(f"Write {topic} stream to cassandra successfully.")
    except Exception as e:
        logging.error(f"Failed to write message to cassandra table: {topic}")


def query_to_mysql(df, bs, topic, schema):
    """
    Write processed stream data to MySQL.
    Args:
        df : The DataFrame to be written to the table.
        epoch_id : id.
        topic (str): name of table.
    Returns:
        None
    Raises:
        Exception: If an error occurs while writing the DataFrame to the table.
    """
    try:
        expanded_df = df \
                        .selectExpr("CAST(value AS STRING)") \
                        .select(from_json(col("value"),schema).alias(f"{topic}")) \
                        .select(f"{topic}.*")         

        # expanded_df.printSchema()

        # Output to Console
        expanded_df.writeStream \
          .outputMode("append") \
          .format("console") \
          .option("truncate", False) \
          .start()  

        query = expanded_df.writeStream \
        .trigger(processingTime="15 seconds") \
        .outputMode("update") \
        .foreachBatch(bs.save_to_mysql) \
        .start()
        query.awaitTermination()
        logging.info(f"Write {topic} stream to mysql successfully.")        
    except Exception as e:
        logging.error(f"Failed to write message to mysql table: {topic}")


def query_to_postgres(df, bs, topic, schema):
    """
    Write processed stream data to PostgreSQL.
    Args:
        df : The DataFrame to be written to the table.
        epoch_id : id.
        topic (str): name of table.
    Returns:
        None
    Raises:
        Exception: If an error occurs while writing the DataFrame to the table.
    """
    try:
        expanded_df = df \
                        .selectExpr("CAST(value AS STRING)") \
                        .select(from_json(col("value"),schema).alias(f"{topic}")) \
                        .select(f"{topic}.*")         

        # expanded_df.printSchema()

        # Output to Console
        expanded_df.writeStream \
          .outputMode("append") \
          .format("console") \
          .option("truncate", False) \
          .start()  

        query = expanded_df.writeStream \
                    .trigger(processingTime="15 seconds") \
                    .outputMode("update") \
                    .foreachBatch(bs.save_to_postgres) \
                    .start()
        query.awaitTermination()
        logging.info(f"Write {topic} stream to postgres successfully.")        
    except Exception as e:
        logging.error(f"Failed to write message to postgres table: {topic}")

def create_schema(topic):
    '''
    Write schema of tables.
    Args:
        topic (str): name of table.
    Returns:
        None
    '''
    try:
        if topic=='actor':
            schema = StructType([
                StructField("actor_id", StringType()),
                StructField("first_name", StringType()),
                StructField("last_name", StringType()),
                StructField("last_update", StringType()),
            ])
        elif topic=='category':
            schema = StructType([
                StructField("category_id", StringType()),
                StructField("first_name", StringType()),
                StructField("last_update", StringType()),
            ])
        elif topic=='film':
            schema = StructType([
                StructField("film_id", IntegerType()),
                StructField("title", StringType()),
                StructField("description", StringType()),
                StructField("release_year", StringType()),
                StructField("language_id", IntegerType()),
                StructField("original_language_id", IntegerType()),
                StructField("rental_duration", StringType()),
                StructField("rental_rate", IntegerType()),
                StructField("length", IntegerType()),
                StructField("replacement_cost", IntegerType()),
                StructField("rating", StringType()),
                StructField("last_update", StringType()),
                StructField("special_features", StringType()),
                StructField("fulltext", StringType())
            ])
        elif topic=='film_actor':
            schema = StructType([
                StructField("actor_id", IntegerType()),
                StructField("film_id", IntegerType()),
                StructField("last_update", StringType())
            ])
        elif topic=='film_category':
            schema = StructType([
                StructField("film_id", IntegerType()),
                StructField("category_id", IntegerType()),
                StructField("last_update", StringType())
            ])
        elif topic=='inventory':
            schema = StructType([
                StructField("inventory_id", IntegerType()),
                StructField("film_id", IntegerType()),
                StructField("store_id", IntegerType()),
                StructField("last_update", StringType())
            ])
        elif topic=='rental':
            schema = StructType([
                StructField("rental_id", IntegerType()),
                StructField("rental_date", IntegerType()),
                StructField("inventory_id", IntegerType()),
                StructField("customer_id", IntegerType()),
                StructField("return_date", StringType()),
                StructField("staff_id", IntegerType()),
                StructField("last_update", StringType())
            ])   

        logging.info(f"schema {topic} created successfully.")
        return schema
    except Exception as e:
        logging.error(f"Failed to create schema for {topic} table.")
        return "Schema not found."


if __name__ == "__main__": 
    # df = stream_to_dataframe() 
    for i, topic in enumerate(list_topics):
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(topic)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        df = stream_to_dataframe(topic)
        bs = BatchStream(topic)
        schema = create_schema(topic)
        # query_to_cassandra(df, bs, topic, schema)
        query_to_postgres(df, bs, topic, schema)
        # query_to_mysql(df, bs, topic, schema)

