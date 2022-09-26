import psycopg2
from config import config

#conn = psycopg2.connect("dbname=testwifilogs user=postgres password=XXXXXX")

def connect():
    """Connect to the PostgreSQL database server"""
    conn = None
    try:
        #read connection parameters
        params = config()

        #connect to the PostgreSQL server
        print('Connection to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement