# copyright 2022 Medicines Discovery Catapult
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-

import argparse
import logging

import psycopg2
from psycopg2.extras import LoggingConnection
from klein_config import get_config

parser = argparse.ArgumentParser()
parser.add_argument("--debug", help="enable debug", action="store_true")


def params(**kwargs):
    """
    generate a dict of connection based on those provided by klein_config
    :param config: config imported from klein_config
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

    for key, value in kwargs.items():
        p[key] = value

    return p


class PostgresConnection:

    def __init__(self):
        self.connection = None
        args, _ = parser.parse_known_args()
        self.debug = args

    def refresh(self, **kwargs):
        """
        refresh the connection
        :param config: dict of parameters to refresh the connection with (optional)
        :return psycopg.connection
        """
        if self.connection:
            self.connection.close()
        return self.connect(**kwargs)

    def connect(self, **kwargs):
        """
        connect to database
        :param config: dict of parameters to refresh the connection with (optional)
        :return psycopg.connection
        """

        if not kwargs:
            kwargs = {}

        p = params(**kwargs)

        if not p:
            return None

        if self.debug:
            logging.basicConfig(level=logging.DEBUG)
            logger = logging.getLogger(__name__)
            p["connection_factory"] = LoggingConnection
            conn = psycopg2.connect(**p)
            conn.initialize(logger)
        else:
            conn = psycopg2.connect(**p)

        return conn


