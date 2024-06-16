test:
	pytest tests/

check:
	isort .
	black .
	flake8 .
	pylint --recursive=y .

down:
	docker system prune && docker volume prune && docker compose down

up:
	make down && docker compose up --build -d 

log:
	docker logs -f producer

# cassandra:
# 	- winpty docker exec -it cassandra cqlsh -u cassandra -p cassandra localhost 9042
# 	Get tables info:
# 	- SELECT * FROM system_schema.keyspaces;
# 	Get table info:
# 	- select * from actor_ks.actor_table;
# 	- select * from category_ks.category_table;
#   - select * from film_ks.film_table;
# 	- ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'new_password';


# MySQL:
# 	- winpty docker exec -it mysql mysql -u user -p
# 	- select * from information_schema.tables;
# 	- select * from dvd_rentals_lake_db.actor;
# 	- select count(*) from dvd_rentals_lake_db.actor;
# 	- DELETE FROM dvd_rentals_lake_db.actor;


# Postgres:
#	- winpty docker container exec -it postgres psql -U user -d dvd_rentals_lake_db
# 	- select * from schema_dvd_rentals.actor;
# 	- select count(*) from schema_dvd_rentals.actor;
# 	- select * from schema_dvd_rentals.category;
# 	- select count(*) from schema_dvd_rentals.category;
# 	- select * from schema_dvd_rentals.film;
# 	- select count(*) from schema_dvd_rentals.film;



# netstat -ano | findstr :3306
# taskkill /PID typeyourPIDhere /F
