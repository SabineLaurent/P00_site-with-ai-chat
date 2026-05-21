.PHONY: up down logs build clean test

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

build:
	docker compose build

clean:
	docker compose down -v

test:
	docker compose run --rm backend pytest

restart:
	$(MAKE) down
	$(MAKE) up
