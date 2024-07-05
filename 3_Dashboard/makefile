down:
	docker system prune && docker volume prune && docker compose down

up:
	make down && docker compose up --build -d 


# Postgres:
#	- winpty docker container exec -it postgres psql -U postgres -d dvd_rentals
# 	- select * from category_recommendations_ranked;


# netstat -ano | findstr :3306
# taskkill /PID typeyourPIDhere /F

Superset:
	- winpty docker exec -it superset bash
	- superset db upgrade

dashboard:
	- winpty docker exec -it superset-create-dashboard python scripts/create_dashboard.py 

# access the dashboard on localhost:8088 