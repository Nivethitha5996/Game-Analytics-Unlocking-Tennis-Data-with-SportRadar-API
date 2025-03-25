# db_operations.py
from sqlalchemy import create_engine
import pandas as pd

def execute_query(query):
    DATABASE_URI = 'mysql+pymysql://username:password@localhost/tennis_analytics'
    engine = create_engine(DATABASE_URI)
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result