CREATE DATABASE IF NOT EXISTS dvd_rentals_lake_db;

USE dvd_rentals_lake_db;

CREATE TABLE IF NOT EXISTS actor(
    actor_id int primary key AUTO_INCREMENT,
    first_name varchar(100),
    last_name varchar(100),
    last_update varchar(100)
);

CREATE TABLE IF NOT EXISTS category(
    category_id int primary key AUTO_INCREMENT,
    last_name varchar(100),
    last_update varchar(100)
);

CREATE TABLE IF NOT EXISTS film(
    film_id int primary key AUTO_INCREMENT, 
    title VARCHAR (100), 
    description VARCHAR (1000), 
    release_year VARCHAR (100), 
    language_id int, 
    original_language_id int, 
    rental_duration VARCHAR (100), 
    rental_rate int, 
    length int, 
    replacement_cost int, 
    rating VARCHAR (100), 
    last_update VARCHAR (100), 
    special_features VARCHAR (100), 
    fulltext VARCHAR (1000)
    );

CREATE TABLE IF NOT EXISTS film_actor(
    actor_id int primary key AUTO_INCREMENT,
    film_id int,
    last_update VARCHAR (100)
    );

CREATE TABLE IF NOT EXISTS film_category(
    film_id int primary key AUTO_INCREMENT, 
    category_id int, 
    last_update VARCHAR (100)
    );

CREATE TABLE IF NOT EXISTS inventory(
    inventory_id int primary key AUTO_INCREMENT, 
    film_id int, 
    store_id int, 
    last_update VARCHAR (1000)
    );

CREATE TABLE IF NOT EXISTS rental(
    rental_id int primary key AUTO_INCREMENT, 
    rental_date VARCHAR (100), 
    inventory_id int, 
    customer_id int, 
    return_date VARCHAR (100), 
    staff_id int, 
    last_update VARCHAR (100)
    );


