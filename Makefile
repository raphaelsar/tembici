clean:
	@echo "Execute cleaning ..."
	rm -f *.pyc
	rm -f coverage.xml
	rm -rf app/__pycache__


pep8:
	@find . -type f -not -path "*./.venv/*" -not -path "*tests/__init__.py*" -name "*.py"|xargs flake8 --max-line-length=120 --ignore=E402 --max-complexity=6

build-image: clean
	docker-compose up --build -d

run: clean
	python index.py