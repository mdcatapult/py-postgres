import argparse
import logging
from typing import Dict

import psycopg2
from psycopg2.extras import LoggingConnection
from klein_config import get_config

parser = argparse.ArgumentParser()
parser.add_argument("--debug", help="enable debug", action="store_true")


def params(config_path: str = 'postgres', **kwargs) -> Dict:
    """
    generate a dict of connection based on those provided by klein_config
    :param config_path: the path to the postgres config in the config
    :param kwargs: expanded keyword arguments to build a connection with
    :return dict
    """
    config = get_config()
    p = {}

    if config.has('postgres.username'):
        p["user"] = config.get('postgres.username')

    if config.has('postgres.password'):
        p["password"] = config.get('postgres.password')

    if config.has('postgres.database'):
        p["database"] = config.get('postgres.database')

    if config.has('postgres.host'):
        p["host"] = config.get('postgres.host', "127.0.0.1")

    if config.has('postgres.port'):
        p["port"] = config.get('postgres.port', "5432")

    p.update(kwargs)
    return p


class PostgresConnection:

    def __init__(self):
        self.connection = None
        args, _ = parser.parse_known_args()
        self.debug = args

    def refresh(self, config_path: str = 'postgres', **kwargs):
        """
        refresh the connection
        :param config_path: the path to the postgres config in the config
        :param **kwargs: parameters to refresh the connection with (optional)
        :return psycopg.connection
        """
        if self.connection:
            self.connection.close()
        return self.connect(config_path, **kwargs)

    def connect(self, config_path: str = 'postgres', **kwargs):
        """
        connect to database
        :param config_path: the path to the postgres config in the config
        :param **kwargs: parameters to refresh the connection with (optional)
        :return psycopg.connection
        """

        p = params(**kwargs)

        if not p:
            return None

        readonly = p.pop('readonly', True)
        autocommit = p.pop('autocommit', readonly)

        if self.debug:
            logging.basicConfig(level=logging.DEBUG)
            logger = logging.getLogger(__name__)
            p["connection_factory"] = LoggingConnection
            conn = psycopg2.connect(**p)
            conn.initialize(logger)
        else:
            conn = psycopg2.connect(**p)

        conn.set_session(readonly=readonly,
                         autocommit=autocommit)

        return conn


