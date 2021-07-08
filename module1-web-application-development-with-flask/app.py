from flask import Flask, render_template
import sqlite3
import json
from twitter import *


db_name = "tweet.sqlite3"
ACCESS_TOKEN = ''
ACCESS_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

t = Twitter(auth=OAuth(CONSUMER_KEY,
            CONSUMER_SECRET,
            ACCESS_TOKEN,
            ACCESS_SECRET))

def create_db(db_name):
    # connect to the db
    conn = sqlite3.connect(db_name)
    curs = conn.cursor()

    #query_table_exist = '''SELECT name FROM sqlite_master WHERE type='table' AND name='{demo}';'''

    # first drop the table if exists to make life easier
    drop_table = '''DROP TABLE IF EXISTS tweets'''
    curs.execute(drop_table)

    # creating demo table
    create_demo_table = '''
        CREATE TABLE tweets (
            created_at VARCHAR(1),
            id INT,
            id_str VARCHAR(100),
            text VARCHAR(500),
            truncated VARCHAR(5000),
            entities VARCHAR(5000),
            source VARCHAR(500),
            in_reply_to_status_id INT,
            in_reply_to_status_id_str VARCHAR(500),
            in_reply_to_user_id INT,
            in_reply_to_user_id_str VARCHAR(500),
            in_reply_to_screen_name VARCHAR(100),
            user VARCHAR(100), 
            geo VARCHAR(100), 
            coordinates VARCHAR(100),
            place VARCHAR(100),
            contributors VARCHAR(100),
            retweeted_status VARCHAR(100),
            is_quote_status BIT, 
            quoted_status VARCHAR(100),
            quoted_status_id INT,
            quoted_status_id_str VARCHAR(100),
            retweet_count INT,
            retweet_status VARCHAR(100),
            extended_entities VARCHAR(100),
            favorite_count INT,
            favorited BIT,
            retweeted BIT,
            possibly_sensitive BIT,
            possibly_sensitive_appealable BIT,
            lang VARCHAR(2)
        )
        '''
    curs.execute(create_demo_table)
    conn.commit()
    curs.close()
    conn.close()

def insert_records(db_name, records):
    conn = sqlite3.connect(db_name)
    curs = conn.cursor()

    query_table_exist = '''SELECT name FROM sqlite_master WHERE type='table' AND name='tweets';'''
    
    #print(curs.execute(query_table_exist).fetchall())

    for r in records:
        header = f"INSERT INTO tweets ( "
        keys = ', '.join(list(r.keys()))
        #print(keys)
        inter = ") VALUES ( "
        #print(inter)
        values = ', '.join("'"+str(v).replace("'", "''")+"'" for v in r.values())
        #print(values)
        end = ")"
        insert_record = header + keys + inter + values + end
        #print(insert_record)
        curs.execute(insert_record)

    conn.commit()
    curs.close()
    conn.close()    

if __name__ == "__main__":
    
    create_db(db_name)
    results = t.statuses.home_timeline(count=6)
    #print(','.join([list(r.values()) for r in results]))
    #for result in results:
    #    print(', '.join(list(result.keys())))
    #    print(', '.join(str(v) for v in result.values()))
    
    insert_records(db_name, results)