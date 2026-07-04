import os
import psycopg2
from psycopg2.pool import SimpleConnectionPool

_pool = None

from shared_libs.core.config import ConfigService

def get_pool():
    global _pool
    if _pool is None:
        _pool = SimpleConnectionPool(
            1, 10,
            host=ConfigService.get_postgres_host(),
            port=ConfigService.get_postgres_port(),
            dbname=ConfigService.get_postgres_db(),
            user=ConfigService.get_postgres_user(),
            password=ConfigService.get_postgres_password()
        )
    return _pool

def get_connection():
    return get_pool().getconn()

def release_connection(conn):
    get_pool().putconn(conn)
