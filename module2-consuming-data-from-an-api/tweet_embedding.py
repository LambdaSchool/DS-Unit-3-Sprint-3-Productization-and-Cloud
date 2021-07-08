import sqlite3
import json
import basilica

BAS_KEY = ""
DB_FILE = "tweet.sqlite3"
TABLE_NAME = "tweets"


def create_col(table, col_name):
    sqlite_conn = sqlite3.connect(DB_FILE)
    curs = sqlite_conn.cursor()

    # we need to check if the column we want to create exists 
    # before creating it    
    cols = curs.execute(f"PRAGMA table_info('{table}')").fetchall()
    col_names = [col[1] for col in cols]
    #print(table)
    #print(col_names)
    
    # insert new column only if it does not exist.
    if col_name not in col_names:   
        try:
            curs.execute(f'ALTER TABLE {table} ADD COLUMN {col_name} VARCHAR(10000);')
        except:
            print("ERROR: Column Insertion Error")
        
    # commit and close the dB
    sqlite_conn.commit()
    curs.close()
    sqlite_conn.close()

def insert_embeddings(bas_conn, table, col):    
    sqlite_conn = sqlite3.connect(DB_FILE)
    curs = sqlite_conn.cursor()
    #embedding = bas_conn.embed_sentence('hey this is a cool tweet', model='twitter')

    rows = curs.execute(f'SELECT text FROM {TABLE_NAME}').fetchall()

    # adding embeddings to col row by row, assuming col is empty
    # absolutely wont work if it is not...
    for r in rows:
        print(f'Adding embeddings for {r[0]}...')
        with bas_conn as c:
            embeddings = c.embed_sentence(r[0])
            insert = f'INSERT INTO {table} ({col}) VALUES ("{str(list(embeddings))}");'
            curs.execute(insert)
    
    # commit and close
    sqlite_conn.commit()
    curs.close()
    sqlite_conn.close()    
        
if __name__ == "__main__":
    col_name = "embeddings"
    bas_conn = basilica.Connection(BAS_KEY)
    
    print("Inserting new column to dB...")
    create_col(TABLE_NAME, col_name)
    print("Adding embeddings...")
    insert_embeddings(bas_conn, TABLE_NAME, col_name)
    print("Embeddings added..."