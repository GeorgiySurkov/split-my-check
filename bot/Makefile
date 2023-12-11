migrate:
	alembic upgrade heads

downgrade:
	alembic downgrade -1

revision:
	alembic revision --autogenerate -m "$(M)"

install_dev:
	pip-sync requirements.txt dev-requirements.txt

install:
	pip-sync requirements.txt
