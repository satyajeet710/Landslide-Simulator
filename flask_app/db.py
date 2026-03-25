import mysql.connector
from mysql.connector import pooling

_pool = None

def init_db_pool(config):
    global _pool, _config
    _config = config  # store config, don't connect yet

def get_conn():
    global _pool, _config
    if _pool is None:
        try:
            _pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="mypool",
                pool_size=5,
                **_config
            )
        except Exception as e:
            raise RuntimeError(f'DB connection failed: {e}')
    return _pool.get_connection()
