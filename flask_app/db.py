import mysql.connector
from mysql.connector import pooling
from flask import current_app

_pool = None

def init_db_pool(config):
    global _pool
    if _pool is None:
        _pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=5,
            **config
        )

def get_conn():
    global _pool
    if _pool is None:
        raise RuntimeError('DB pool not initialized')
    return _pool.get_connection()
