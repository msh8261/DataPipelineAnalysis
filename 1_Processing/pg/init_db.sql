-- CREATE DATABASE dvd_rentals_lake_db;
CREATE SCHEMA IF NOT EXISTS schema_dvd_rentals;


GRANT CONNECT ON DATABASE dvd_rentals_lake_db TO user;
GRANT ALL PRIVILEGES ON SCHEMA schema_dvd_rentals TO user;

-- \c dvd_rentals_lake_db;

CREATE TABLE IF NOT EXISTS actor(
    actor_id int SERIAL primary key,
    first_name varchar(100),
    last_name varchar(100),
    last_update varchar(100)
);

CREATE TABLE IF NOT EXISTS category(
    category_id int SERIAL primary key,
    last_name varchar(100),
    last_update varchar(100)
);

CREATE TABLE IF NOT EXISTS film(
    film_id int SERIAL primary key, 
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
    actor_id int SERIAL primary key,
    film_id int,
    last_update VARCHAR (100)
    );

CREATE TABLE IF NOT EXISTS film_category(
    film_id int SERIAL primary key, 
    category_id int, 
    last_update VARCHAR (100)
    );

CREATE TABLE IF NOT EXISTS inventory(
    inventory_id int SERIAL primary key, 
    film_id int, 
    store_id int, 
    last_update VARCHAR (1000)
    );

CREATE TABLE IF NOT EXISTS rental(
    rental_id int SERIAL primary key, 
    rental_date VARCHAR (100), 
    inventory_id int, 
    customer_id int, 
    return_date VARCHAR (100), 
    staff_id int, 
    last_update VARCHAR (100)
    );


GRANT CREATE ON SCHEMA schema_dvd_rentals TO user;
GRANT USAGE ON SCHEMA schema_dvd_rentals TO user;

GRANT INSERT ON TABLE schema_dvd_rentals.actor TO user;
GRANT SELECT ON TABLE schema_dvd_rentals.actor TO user;

GRANT INSERT ON TABLE schema_dvd_rentals.category TO user;
GRANT SELECT ON TABLE schema_dvd_rentals.category TO user;

GRANT INSERT ON TABLE schema_dvd_rentals.film TO user;
GRANT SELECT ON TABLE schema_dvd_rentals.film TO user;

GRANT INSERT ON TABLE schema_dvd_rentals.film_actor TO user;
GRANT SELECT ON TABLE schema_dvd_rentals.film_actor TO user;

GRANT INSERT ON TABLE schema_dvd_rentals.film_category TO user;
GRANT SELECT ON TABLE schema_dvd_rentals.film_category TO user;

GRANT INSERT ON TABLE schema_dvd_rentals.inventory TO user;
GRANT SELECT ON TABLE schema_dvd_rentals.inventory TO user;

GRANT INSERT ON TABLE schema_dvd_rentals.rental TO user;
GRANT SELECT ON TABLE schema_dvd_rentals.rental TO user;
