
setup:
	# Create python virtualenv & source it
	python3 -m venv .venv
	source .venv/bin/activate

install:
	# to create/update the file
	# python -m pip freeze > requirements.txt

	# This should be run from inside a virtualenv
	pip install --upgrade pip &&\
		pip install -r requirements.txt

migration_init:
	# database initialization
	python migration.py db init


migration:
	# running the migrate command
	python migration.py db migrate
	python migration.py db upgrade

test:
	# Additional, optional, tests could go here
	#python -m pytest -vv --cov=myrepolib tests/*.py
	#python -m pytest --nbval notebook.ipynb

lint:
	# See local hadolint install instructions:   https://github.com/hadolint/hadolint
	# This is linter for Dockerfiles
	#hadolint Dockerfile
	# This is a linter for Python source code linter: https://www.pylint.org/
	# This should be run from inside a virtualenv
	pylint --disable=R,C,W1203,W1309 goods.py

all: install lint test
