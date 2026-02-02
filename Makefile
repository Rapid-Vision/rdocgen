.PHONY: all docs

all: docs

docs:
	uv run rdocgen -c src --project-name "rdocgen" -o vitepress/docs/api --format md-plain --clean