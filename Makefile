.PHONY: format lint typecheck test quality system-check ci

format:
	uv run black app tests

lint:
	uv run flake8 app tests

typecheck:
	uv run mypy app

test:
	uv run pytest -q

system-check:
	uv run flask --app wsgi:app system-check

quality:
	uv run black --check app tests
	uv run flake8 app tests
	uv run mypy app

ci: quality test system-check
