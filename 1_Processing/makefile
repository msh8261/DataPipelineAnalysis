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
