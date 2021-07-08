import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from sqlalchemy.engine import reflection
import pandas as pd


engine = create_engine('sqlite:///tweet.sqlite3')

metadata = MetaData()
metadata.create_all(engine)
inspector = inspect(engine)

print(inspector.get_columns('id'))

with engine.connect() as con:
    rs = con.execute("SELECT * FROM tweets")
    
    for row in rs:
        print(row)
        
    # get table names
    insp = reflection.Inspector.from_engine(engine)
    print(insp.get_table_names())


df = pd.read_sql_query(""" SELECT * FROM tweets""",
                       con=engine.connect())
                       
print(df.head())
        
con.close()

