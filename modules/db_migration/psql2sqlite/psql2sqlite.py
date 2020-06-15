from pymongo import MongoClient
import pymongo
import datetime
import sqlite3
import codecs
import json
import time
import uuid
import os

sqlitedb = 'luna.db'

client = MongoClient()
db = client.in_vivo_veritas
users = db.users
files = db.files
intel = db.intelligence
sci = db.science
research = db.research
arch = db.arcs
logs = db.logs
unread = db.unread
read = db.read
mv = db.mindvalley
sessions = db.sessions
hades = db.exploits
rec_loc = db.recent_location
config = db.configurations
hades.create_index([('title',pymongo.ASCENDING)], unique=True)
intel.create_index([('title',pymongo.ASCENDING)], unique=True)
files.create_index([('payload',pymongo.ASCENDING)], unique=True)
files.create_index([('date',pymongo.ASCENDING)], unique=True)
arch.create_index([('date',pymongo.ASCENDING)], unique=True)


epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return int((dt - epoch).total_seconds() * 1000.0)

def migrate_files():
    
    # FILES
    conn = sqlite3.connect(sqlitedb)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS texts;')

    # text arrays now become json-stringified array. Persistence functions should handle normalization.
    # timestamp becomes date string
    cur.execute(
    """
    CREATE TABLE texts (
        document_id VARCHAR (200) NOT NULL PRIMARY KEY,
        document_type VARCHAR (100) NOT NULL,                                                   
        title VARCHAR NOT NULL,
        origin VARCHAR (100) NOT NULL,
        payload VARCHAR NOT NULL UNIQUE,
        creation_time VARCHAR (100) NOT NULL,
        updated_time VARCHAR (100) NOT NULL,
        flags VARCHAR
    );
    """)
    print("Created table texts")

    cur.execute("SELECT COUNT(*) FROM texts")
    row = cur.fetchone()
    print("Initialising migration with row count:", row)
    time.sleep(2)
    
    for file in files.find():
        try:
            database = json.dumps('texts')
            # print('Got Mongofile:', file)
            if file['payload'] == ['note']:
                payload = json.dumps(file['code_name'][0])
                document_id = json.dumps(str(uuid.uuid4()))
                title = json.dumps('default')
                document_type = json.dumps(file['payload'].upper())
            else:
                payload = json.dumps(file['payload'][0])
                document_id = json.dumps(str(uuid.uuid4()))
                title = json.dumps('default')
                document_type = json.dumps(file['code_name'].upper())

            print('Created data object: ', document_id)
            creation_time = json.dumps(str(datetime.datetime.now()))
            cur.execute("INSERT INTO texts (document_id, document_type, title, origin, payload, creation_time, updated_time) VALUES ({}, {}, {},{}, {}, {}, {})".\
                        format(document_id, document_type, title, database, payload, creation_time, creation_time))
            print("Inserted : ", title)
                                                                                
            cur.execute("SELECT COUNT(*) FROM texts")
            row = cur.fetchone()
            print("Number of rows:", row)
            cur.execute("SELECT * FROM texts LIMIT 1")
            row = cur.fetchone()
            print('data:', row)
        except Exception as e:
            print('CustomInsertError:', e)
        finally:
            print('--------------------------------------------------------------------------------')
            print('--------------------------------------------------------------------------------')
    conn.commit()
    conn.close()

def create_pinned_intel():
    conn = sqlite3.connect(sqlitedb)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS pinned_intel;')
    cur.execute(
    """
    CREATE TABLE core_intel (
        document_id TEXT (200) NOT NULL PRIMARY KEY,
        title TEXT NOT NULL,
        origin TEXT NOT NULL,
        payload TEXT NOT NULL UNIQUE,
        creation_time INTEGER NOT NULL,
        updated_time INTEGER NOT NULL,
        flags TEXT,
        tags TEXT
    );
    """)
    print("Created table pinned_intel")

    cur.execute("SELECT COUNT(*) FROM pinned_intel")
    row = cur.fetchone()
    print("Test query to pinned_intel resolved:", row)
    conn.commit()
    conn.close()

def create_core_intel():
    conn = sqlite3.connect(sqlitedb)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS core_intel;')
    cur.execute(
    """
    CREATE TABLE core_intel (
        document_id TEXT (200) NOT NULL PRIMARY KEY,
        title TEXT NOT NULL,
        origin TEXT NOT NULL,
        payload TEXT NOT NULL UNIQUE,
        creation_time INTEGER NOT NULL,
        updated_time INTEGER NOT NULL,
        flags TEXT,
        tags TEXT
    );
    """)
    print("Created table core_intel")

    cur.execute("SELECT COUNT(*) FROM core_intel")
    row = cur.fetchone()
    print("Test query to core_intel resolved:", row)
    conn.commit()
    conn.close()


def create_science():
    conn = sqlite3.connect(sqlitedb)
    cur = conn.cursor()
    print("Created table science")
    
    for file in intel.find():
        try:
            database = json.dumps('science')
            # print('Got Mongofile:', file['payload'])
            document_id = json.dumps(str(uuid.uuid4()))
            payload = json.dumps(file['payload'][0])
            title = json.dumps(file['title']),
            creation_time = unix_time_millis(datetime.datetime.now())
            print('Created data object: ', title[0])
            sql = "INSERT INTO core_intel (document_id, title, payload, origin, creation_time, updated_time) VALUES ({}, {}, {},{}, {}, {})".\
                        format(document_id, title[0], payload, database, creation_time, creation_time)
            # print('Inserting query:', sql)
            # time.sleep(2)
            cur.execute(sql)
            print("Inserted : ", title)
                                                                                
            cur.execute("SELECT COUNT(*) FROM core_intel")
            row = cur.fetchone()
            print("Number of rows:", row)
            cur.execute("SELECT * FROM core_intel ORDER BY RANDOM() LIMIT 1")
            row = cur.fetchone()
            print('data:', row)
        except Exception as e:
            print('CustomInsertError:', e)
        except KeyboardInterrupt:
            print('Process terminated by user. Committing')
            conn.commit()
            conn.close()
        finally:
            print('--------------------------------------------------------------------------------')
            print('--------------------------------------------------------------------------------')

    cur.execute("SELECT COUNT(*) FROM core_intel")
    row = cur.fetchone()
    print("Number of rows in core_intel:", row)                 
    conn.commit()
    conn.close()

def create_tag_tables(tag_name, skip_insert = False):
    conn = sqlite3.connect(sqlitedb)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(f'DROP TABLE IF EXISTS {tag_name};')
    cur.execute(
    f"""
    CREATE TABLE {tag_name} (
        document_id TEXT (200) NOT NULL PRIMARY KEY,
        title TEXT NOT NULL,
        creation_time INTEGER NOT NULL,
        updated_time INTEGER NOT NULL,
        CONSTRAINT fk_column FOREIGN KEY (document_id) REFERENCES core_intel (document_id)
    );
    """)

    if not skip_insert:
        cur.execute("SELECT document_id, title FROM core_intel;")
        rows = cur.fetchall()
        for row in rows:
            document_id = json.dumps(row['document_id'])
            title = json.dumps(row['title'])
            creation_time = unix_time_millis(datetime.datetime.now())
            sql = "INSERT INTO {} (document_id, title, creation_time, updated_time) VALUES ({}, {}, {}, {})".\
                        format(tag_name, document_id, title, creation_time, creation_time)
            # print('sending query:', sql)
            cur.execute(sql)
            print("{tag_name} tagged: ", title)
            cur.execute(f"SELECT COUNT(*) FROM {tag_name}")
            row = cur.fetchone()
            print("Number of rows:", row['COUNT(*)'])

    print(f"Created tag {tag_name}")
    conn.commit()
    conn.close()


# populate intelligence with science table rows; create intelligence and science tag for each entry

# def create_initial_tables():
    # create_intelligence()
    # create_science()
    # create_users()
    # create_archive()
    # create_weather_data()
    # create_bot_predicates()
    # create_session_data()


# command to get table names, for use later
# res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
# for name in res:
#     print name[0]