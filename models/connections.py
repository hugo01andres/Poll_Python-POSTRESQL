import os
from psycopg2 import connect
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv
from contextlib import contextmanager


DATABASE_PROMPT = "Enter the DATABASE_URI value or leave empty to load from .env file: "
def create_connection():
        load_dotenv()
        conn_string = "host={0} dbname={1} user={2} password={3} port={4}".format(
        os.environ["DB_HOST"],
        os.environ["DB_NAME"],
        os.environ["DB_USER"],
        os.environ["DB_PASSWORD"],
        os.environ["DB_PORT"]
    )
        return conn_string

pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn=create_connection())

@contextmanager
def get_connection():
    connection = pool.getconn()

    try:
        yield connection
    finally:
        pool.putconn(connection)