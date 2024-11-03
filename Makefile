# Run dev server: make start_dev
start_dev:
	fastapi dev app/main.py

# Run tests: make test
test:
	PYTHONPATH=. python -m pytest tests/

# Install dependencies: make install
install:
	pip install -r requirements.txt

# Save requirements: make freeze
freeze:
	pip freeze > requirements.txt

# Run linter: make lint
lint:
	flake8 app/ --count --exit-zero --max-complexity=10 --statistics  --ignore E501