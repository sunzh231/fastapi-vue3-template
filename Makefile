# Makefile

.PHONY: init dev

init:
	@pdm install
	@bun install
dev-frontend:
	@bun dev

dev:
	@nf start

build-frontend:
	@yarn build

deploy: build-frontend
	@git push -f dokku master
