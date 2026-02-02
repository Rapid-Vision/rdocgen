.PHONY: all docs

all: docs

docs:
	uv run rdocgen -c src -o vitepress/docs/api --format md-plain --clean