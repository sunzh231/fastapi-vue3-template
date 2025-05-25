# Makefile

.PHONY: init dev

init:
	@uv sync
	@bun install

dev:
	@echo "正在清理Overmind资源..."
	@pkill -f overmind || true
	@rm -f ./.overmind.sock
	@echo "清理完成，启动新的Overmind实例..."
	@sleep 1
	@overmind start -f Procfile.dev

deploy:
	@git push -f dokku master
