# Klein Postgres

Simple module to allow connection to postgres

## Example

config.yaml

``` yaml
postgres:
    username: postgres_username
    password: postgres_password
    database: database_name
    host: 127.0.0.1
    port: 5432
    readonly: True  # Default to True, set to False if write operation is required
    autocommit: True  # Default to be the same as readonly. If set to false, you are expected to commit after the queries manually.
```

python

``` python
from klein_postgres.connect import connect

connection = connect()  # or
connection = connect('postgres')  # same as in the config. You may specify multiple postgres db in the config
```


## Development


Utilises python 3.7

### Ubuntu

```
sudo apt install python3.7
```

## Virtualenv

```
virtualenv -p python3.7 venv
source venv/bin/activate
echo -e "[global]\nindex = https://nexus.mdcatapult.io/repository/pypi-all/pypi\nindex-url = https://nexus.mdcatapult.io/repository/pypi-all/simple" > venv/pip.conf
pip install -r requirements.txt
```

### Testing
```bash
docker-compose up
python -m pytest
```
For test coverage you can run:
```bash
docker-compose up
python -m pytest --cov-report term --cov src/ tests/
```
