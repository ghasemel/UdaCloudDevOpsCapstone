
setup:
	# Create python virtualenv & source it
	python3 -m venv ~/.venv

	# source it
	. ~/.venv/bin/activate

refresh_requirements:
	# to create/update the file
	python -m pip freeze > requirements.txt

install:
	# This should be run from inside a virtualenv
	pip install --upgrade pip &&\
		pip install -r requirements.txt

db_migration_init:
	# database initialization
	python migration.py db init

test_db_migration:
	# running the migrate command
	python migration.py test migrate
	python migration.py test upgrade

db_migration:
	# running the migrate command
	python migration.py prod upgrade

test:
	# tests go here
	python -m pytest

lint-docker:
	# See local hadolint install instructions:   https://github.com/hadolint/hadolint
	# This is linter for Dockerfiles
	hadolint Dockerfile

lint:
	# This is a linter for Python source code linter: https://www.pylint.org/
	# This should be run from inside a virtualenv
	# W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
	# W0611: unused-import
	# W0703: Catching too general exception Exception (broad-except)
	pylint --disable=R,C,W1203,W0611,W0703 --load-plugins=pylint_flask_sqlalchemy *.py

all: install lint test
