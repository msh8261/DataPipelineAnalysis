#!/usr/bin/env bash

until printf "" 2>>/dev/null >>/dev/tcp/cassandra/9042; do
    sleep 5;
    echo "Waiting for cassandra...";
done

echo "Creating keyspace and table..."

cqlsh cassandra -u cassandra -p cassandra -e "CREATE KEYSPACE IF NOT EXISTS actor_ks WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};"
cqlsh cassandra -u cassandra -p cassandra -e "CREATE TABLE IF NOT EXISTS actor_ks.actor_table(uuid uuid primary key, actor_id int, first_name text, last_name text, last_update text);"

cqlsh cassandra -u cassandra -p cassandra -e "CREATE KEYSPACE IF NOT EXISTS category_ks WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};"
cqlsh cassandra -u cassandra -p cassandra -e "CREATE TABLE IF NOT EXISTS category_ks.category_table(uuid uuid primary key, category_id int, last_name text, last_update text);"

cqlsh cassandra -u cassandra -p cassandra -e "CREATE KEYSPACE IF NOT EXISTS film_ks WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};"
cqlsh cassandra -u cassandra -p cassandra -e "CREATE TABLE IF NOT EXISTS film_ks.film_table(uuid uuid primary key, film_id int, title text, description text, release_year text, language_id int, rental_duration text, rental_rate int, length int, replacement_cost int, rating text, last_update text, special_features text, fulltext text);"

cqlsh cassandra -u cassandra -p cassandra -e "CREATE KEYSPACE IF NOT EXISTS film_actor_ks WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};"
cqlsh cassandra -u cassandra -p cassandra -e "CREATE TABLE IF NOT EXISTS film_actor_ks.film_actor_table(uuid uuid primary key, actor_id int, film_id int, last_update text);"

cqlsh cassandra -u cassandra -p cassandra -e "CREATE KEYSPACE IF NOT EXISTS film_category_ks WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};"
cqlsh cassandra -u cassandra -p cassandra -e "CREATE TABLE IF NOT EXISTS film_category_ks.film_category_table(uuid uuid primary key, film_id int, category_id int, last_update text);"

cqlsh cassandra -u cassandra -p cassandra -e "CREATE KEYSPACE IF NOT EXISTS inventory_ks WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};"
cqlsh cassandra -u cassandra -p cassandra -e "CREATE TABLE IF NOT EXISTS inventory_ks.inventory_table(uuid uuid primary key, inventory_id int, film_id int, store_id int, last_update text);"

cqlsh cassandra -u cassandra -p cassandra -e "CREATE KEYSPACE IF NOT EXISTS rental_ks WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};"
cqlsh cassandra -u cassandra -p cassandra -e "CREATE TABLE IF NOT EXISTS rental_ks.rental_table(uuid uuid primary key, rental_id int, rental_date text, inventory_id int, customer_id int, return_date text, staff_id int, last_update text);"




