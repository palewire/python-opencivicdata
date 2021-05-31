testdb:
	psql -c "CREATE USER test with PASSWORD 'test' CREATEDB SUPERUSER;" -U postgres
	psql -c "CREATE DATABASE test;" -U postgres
	psql -c "CREATE EXTENSION postgis;" -U postgres -d test

test:
	pipenv run ./run-tests.sh
	pipenv run flake8

ship:
	rm -rf build/
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/* --skip-existing

.PHONY: testdb test ship
