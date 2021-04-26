testdb:
	psql -c "CREATE USER test with PASSWORD 'test' CREATEDB SUPERUSER;" -U postgres
	psql -c "CREATE DATABASE test;" -U postgres
	psql -c "CREATE EXTENSION postgis;" -U postgres -d test

test:
	pipenv run ./run-tests.sh
	pipenv run flake8

.PHONY: testdb test
