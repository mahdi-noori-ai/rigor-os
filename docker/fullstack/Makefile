# Easy local commands (copy Makefile to project root if useful)

.PHONY: up down logs bootstrap

up:
	docker compose -f rigor-os/docker/fullstack/compose.yml --env-file .env up --build

down:
	docker compose -f rigor-os/docker/fullstack/compose.yml down

logs:
	docker compose -f rigor-os/docker/fullstack/compose.yml logs -f

bootstrap:
	python rigor-os/tools/bootstrap.py
