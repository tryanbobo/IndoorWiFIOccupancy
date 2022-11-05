import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# create engine instance
alchemyEngine = create_engine('postgresql://postgres:Bike7866six@localhost:5433/alkekOccupancy')

# connect to PostgreSQL server
#dbConnection = alchemyEngine.connect():
a = pd.read_sql_query("select * from testwifilogs", con=alchemyEngine)
#a['_date'] = pd.to_datetime(a['date'])
a.resample("3T").sum()

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(a)