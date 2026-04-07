.PHONY: all docs test

all: docs

docs:
	uv run rdocgen -c src --project-name "rdocgen" -o docs_vp/docs/api --clean

test:
	uv run pytest
