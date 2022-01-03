from sqlalchemy import create_engine

TOKEN = 'secret'

DB_USER = 'secret'
DB_PASS = 'secret'
DB_NAME = 'customers'
DB_HOST = 'localhost'
DB_DRIVER = 'psycopg2'
DB = 'postgresql'


engine = create_engine(
    f'{DB}+{DB_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}')

