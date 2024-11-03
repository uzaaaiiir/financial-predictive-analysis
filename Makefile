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

# Docker Commands 
# Build docker image: make build
docker-build:
	docker build -t qinvst-app .

# Run docker container: make run
docker-run:
	docker run -d -p 8000:8000 qinvst-app

# Stop docker container: make stop
docker-stop:
	docker stop $(shell docker ps -a -q --filter ancestor=qinvst-app)

# Remove docker container: make rm
docker-rm:
	docker rm $(shell docker ps -a -q --filter ancestor=qinvst-app)