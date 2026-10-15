# Easy local commands — copy to your project root.
COMPOSE := docker compose -f rigor-os/docker/fullstack/compose.yml --env-file .env

.PHONY: up down logs ps bootstrap gates seo

up:
	$(COMPOSE) up --build -d

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f

ps:
	$(COMPOSE) ps

bootstrap:
	python3 rigor-os/tools/bootstrap.py

gates:
	bash rigor-os/tools/validate-gates.sh

seo:
	python3 rigor-os/tools/seo_context.py
