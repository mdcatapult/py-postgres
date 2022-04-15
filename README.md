# Py-Env-Aware Postgres

Simple module to allow connection to postgres

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
