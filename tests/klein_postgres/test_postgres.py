import argparse
import logging
import os
import unittest

from mock import mock

host = os.environ.get('POSTGRES_HOST')
if host is None:
    host = 'localhost'

dummyConfig = {
    'POSTGRES_HOST': host,
    'POSTGRES_PORT': '5432', 
    'POSTGRES_DATABASE': 'test',
    'POSTGRES_USERNAME': 'postgres',
    'POSTGRES_PASSWORD': 'postgres',
    'READWRITE_HOST': host,
    'READWRITE_PORT': '5432',
    'READWRITE_DATABASE': 'test',
    'READWRITE_USERNAME': 'postgres',
    'READWRITE_PASSWORD': 'postgres',
    'READWRITE_READONLY': '0',
}


@mock.patch.dict(os.environ, dummyConfig)
class TestPostgres(object):

    def test_params(self):
        from src.klein_postgres.connect import params
        p = params()
        assert p == dict(
            database="test",
            user="postgres",
            password="postgres",
            host=host,
            port=5432,
            readonly=True,
            autocommit=True,
        )

    def test_params_with_readonly_set(self):
        from src.klein_postgres.connect import params
        p = params('readwrite')
        assert p == dict(
            database="test",
            user="postgres",
            password="postgres",
            host=host,
            port=5432,
            readonly=False,
            autocommit=False,
        )


    def test_params_with_custom_values(self):
        from src.klein_postgres.connect import params
        tmp_params = dict(
            database="tmp_db",
            user="tmp_username",
            password="tmp_password",
            host="tmp_host",
            port="tmp_port",
            readonly=True,
            autocommit=True,
        )
        p = params(**tmp_params)
        assert p == tmp_params

    def test_connect_with_no_params(self):
        from src.klein_postgres.postgres import connect
        connect()

    def test_connect_with_custom_params(self):
        from src.klein_postgres.postgres import connect
        connect(database="postgres")

    @mock.patch('argparse.ArgumentParser.parse_known_args',return_value=(argparse.Namespace(debug=True, config=None, common=None), argparse.Namespace()))
    def test_connect_with_logging_connection(self, args, caplog):
        caplog.set_level(logging.DEBUG)
        from src.klein_postgres.postgres import connect
        conn = connect('readwrite')
        query = b"CREATE TABLE loggingTest (id serial primary key);"
        conn.cursor().execute(query)
        msg = caplog.records[0].msg
        assert (query == msg)

    @mock.patch('argparse.ArgumentParser.parse_known_args',return_value=(argparse.Namespace(debug=True, config=None, common=None), argparse.Namespace()))
    def test_readonly_connect_with_write_queries(self, args, caplog):
        caplog.set_level(logging.DEBUG)
        from src.klein_postgres.postgres import connect
        conn = connect()
        query = b"CREATE TABLE loggingTest (id serial primary key);"
        try:
            conn.cursor().execute(query)
            conn.commit()
            # an exception should have been raised for attempting a write operation
            assert False
        except Exception:
            pass
