from .models import *


def create_DB_records(df):
    """Pull Los Angeles data from OpenAq & create db records"""
    for index, row in df.iterrows():
        rec = Record(datetime=row['date.utc'], value=row['value'])
        DB.session.add(rec)
    DB.session.commit()

