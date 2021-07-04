import sqlite3

conn = sqlite3.connect("twitoff.sqlite3")
curs = conn.cursor()


# SQL to create table
def user_table_schema():
    create_table = """
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY,
            username VARCHAR(25)
        );
    """
    curs.execute(create_table)


# SQL to create table
def twit_table_schema():
    create_table = """
        CREATE TABLE tweets (
            twit_id INTEGER PRIMARY KEY,
            tweet VARCHAR(280)
        );
    """

    curs.execute(create_table)


# SQL to insert data from list of tuples
def insert_data(tablename, schema, data):
    for datum in data:
        insert = (
            """
            INSERT INTO """
            + tablename
            + " "
            + schema
            + """ VALUES """
            + str(datum[0:])
            + ";"
        )
        print(insert)
        curs.execute(insert)


# custom user data
user_table_data = [(1, "user_1"), (2, "user_2")]


# custom tweet data
twit_table_data = [
    (1, "The Cowboys win! What a excellent game of football!"),
    (2, "Check out my new single: Beyond Me. Out in Stores Jan 1st"),
]

# Calling functions to create tables and insert data
user_table_schema()
twit_table_schema()
insert_data(tablename="users", schema="(user_id, username)", data=user_table_data)
insert_data(tablename="tweets", schema="(twit_id, tweet)", data=twit_table_data)
curs.close()
conn.commit()
