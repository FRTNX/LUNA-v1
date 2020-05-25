from pymongo import MongoClient
import pymongo
import psycopg2
import psycopg2.errors
import psycopg2.extras
import codecs
import json
import uuid
import time
import os

def connect():
    #todo: read from config
    return psycopg2.connect(
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PWD'),
        host = '127.0.0.1',
        port = '5432',
        database = 'luna'
    )

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

def migrate_intel():
    # INTEL
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS intelligence;')

    cur.execute(
    """
    CREATE TABLE intelligence (
        document_id uuid NOT NULL UNIQUE,                                                      
        title varchar NOT NULL UNIQUE,
        origin varchar(100) NOT NULL,
        payload text[] NOT NULL,
        creation_at TIMESTAMP WITH TIME ZONE NOT NULL default current_timestamp,
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL default current_timestamp,
        flags text[] default '{}'
    );
    """)
    print("Created table intelligence")

    for file in intel.find():
        try:
            database = 'intelligence'
            # print('Got Mongofile:', file['payload'])
            data = {
                'payload': file['payload'],
                'title': file['title'],
                'document_id': str(uuid.uuid4())
            }
            print('Created data object: ', data['title'])
            cur.execute("INSERT INTO intelligence (document_id, title, origin, payload) VALUES (%s, %s, %s, %s)",
                        (data['document_id'], data['title'], database, data['payload']))
            print("Inserted : ", data['title'])
                                                                                
            cur.execute("SELECT COUNT(*) FROM intelligence")
            row = cur.fetchone()
            print("Number of rows:", row)
        except psycopg2.errors.UniqueViolation:
            print('Entry already exists.')
        finally:
            print('--------------------------------------------------------------------------------')
            print('--------------------------------------------------------------------------------')

    cur.execute("SELECT COUNT(*) FROM intelligence")
    row = cur.fetchone()
    print("Number of rows in intelligence:", row)                 
    cur.close()
    conn.close()

def migrate_science():
    # SCIENCE
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    # cur.execute('DROP TABLE IF EXISTS science;')

    # cur.execute(
    # """
    # CREATE TABLE science (
    #     document_id uuid NOT NULL UNIQUE,                                                      
    #     title varchar NOT NULL UNIQUE,
    #     origin varchar(100) NOT NULL,
    #     payload text[] NOT NULL,
    #     creation_at TIMESTAMP WITH TIME ZONE NOT NULL default current_timestamp,
    #     updated_at TIMESTAMP WITH TIME ZONE NOT NULL default current_timestamp,
    #     flags text[] default '{}',
    #     tags text[] default '{}'
    # );
    # """)
    # print("Created table science")

    for file in sci.find():
        try:
            database = 'science'
            # print('Got Mongofile:', file['payload'])
            data = {
                'payload': file['payload'],
                'title': file['title'],
                'document_id': str(uuid.uuid4())
            }
            print('Created data object: ', data['title'])
            cur.execute("INSERT INTO intelligence (document_id, title, origin, payload, tags) VALUES (%s, %s, %s, %s, %s)",
                        (data['document_id'], data['title'], database, data['payload'], '{database}'))
            print("Inserted : ", data['title'])
                                                                                
            cur.execute(f"SELECT COUNT(*) FROM intelligence WHERE '{database}' = ANY (tags)")
            row = cur.fetchone()
            print("Number of rows:", row)
        except psycopg2.errors.UniqueViolation:
            print('Entry already exists. Updating.')
            title = data['title']
            cur.execute("UPDATE intelligence SET tags = array_append(tags, %s) WHERE LOWER(title) = %s", (database, title.lower(),))
            cur.execute(f"SELECT COUNT(*) FROM intelligence WHERE '{database}' = ANY (tags)")
            row = cur.fetchone()
            print("Number of rows:", row)
            print(f'Updated {file["title"]}')
        except Exception as e:
            print(f'[-] Error updating {file["title"]}: {e}')
        finally:
            print('--------------------------------------------------------------------------------')
            print('--------------------------------------------------------------------------------')


    cur.execute("SELECT COUNT(*) FROM science")
    row = cur.fetchone()
    print("Number of rows in science:", row)                     
    cur.close()
    conn.close()


def migrate_files():
    # FILES
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS texts;')

    cur.execute(
    """
    CREATE TABLE texts (
        document_id uuid NOT NULL UNIQUE,
        document_type varchar(100) NOT NULL,                                                   
        title varchar NOT NULL,
        origin varchar(100) NOT NULL,
        payload text[] NOT NULL UNIQUE,
        creation_at TIMESTAMP WITH TIME ZONE NOT NULL default current_timestamp,
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL default current_timestamp,
        flags text[] default '{}'
    );
    """)
    print("Created table texts")

    
    for file in files.find():
        try:
            database = 'texts'
            # print('Got Mongofile:', file)
            if file['payload'] == ['note']:
                data = {
                    'payload': [file['code_name']],
                    'title': 'default',
                    'document_id': str(uuid.uuid4()),
                    'document_type': file['payload'][0].upper()
                }
            else:
                data = {
                    'payload': file['payload'],
                    'title': 'default',
                    'document_id': str(uuid.uuid4()),
                    'document_type': file['code_name'].upper()
                }
            print('Created data object: ', data['payload'])
            cur.execute("INSERT INTO texts (document_id, document_type, title, origin, payload) VALUES (%s, %s, %s, %s, %s)",
                        (data['document_id'], data['document_type'], data['title'], database, data['payload']))
            print("Inserted : ", data['title'])
                                                                                
            cur.execute("SELECT COUNT(*) FROM texts")
            row = cur.fetchone()
            print("Number of rows:", row)
        except psycopg2.errors.UniqueViolation:
            print('Entry already exists.')
        finally:
            print('--------------------------------------------------------------------------------')
            print('--------------------------------------------------------------------------------')


def migrate_users():
    print('Migrating users')
    # FILES
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS users;')

    cur.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        user_id UUID NOT NULL UNIQUE,
        user_name varchar NOT NULL,
        user_details jsonb default '{}',
        creation_at TIMESTAMP WITH TIME ZONE NOT NULL default current_timestamp,
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL default current_timestamp,
        flags text[] default '{}'
    );
    """)
    print("Created table users")

    
    for file in ['FRTNX', 'Basket', 'Andile', 'NOAA', 'ThatiLove']:
        try:
            database = 'users'
            print('Got Mongofile:', file)
 
            data = {
                'user_id': str(uuid.uuid4()),
                'user_name': file,
            }
            print('Created data object: ', data)
            cur.execute("INSERT INTO users (user_id, user_name) VALUES (%s, %s)", (data['user_id'], data['user_name']))
            print("Inserted : ", data)
                                                                                
            cur.execute("SELECT COUNT(*) FROM users")
            row = cur.fetchone()
            print("Number of rows:", row)
        except psycopg2.errors.UniqueViolation:
            print('Entry already exists.')
        finally:
            print('--------------------------------------------------------------------------------')
            print('--------------------------------------------------------------------------------')

    cur.close()
    conn.close()


# todo
def migrate_exploits():
    print('Migrating users')
    # FILES
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS users;')

    cur.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        user_id UUID NOT NULL UNIQUE,
        user_name varchar NOT NULL,
        user_details jsonb default '{}',
        creation_at TIMESTAMP WITH TIME ZONE NOT NULL default current_timestamp,
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL default current_timestamp,
        flags text[] default '{}'
    );
    """)
    print("Created table users")

    
    for file in ['FRTNX', 'Basket', 'Andile', 'NOAA', 'ThatiLove']:
        try:
            database = 'users'
            print('Got Mongofile:', file)
 
            data = {
                'user_id': str(uuid.uuid4()),
                'user_name': file,
            }
            print('Created data object: ', data)
            cur.execute("INSERT INTO users (user_id, user_name) VALUES (%s, %s)", (data['user_id'], data['user_name']))
            print("Inserted : ", data)
                                                                                
            cur.execute("SELECT COUNT(*) FROM users")
            row = cur.fetchone()
            print("Number of rows:", row)
        except psycopg2.errors.UniqueViolation:
            print('Entry already exists.')
        finally:
            print('--------------------------------------------------------------------------------')
            print('--------------------------------------------------------------------------------')
            
    cur.close()
    conn.close()


def migrate_nlu_data():
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    cur.execute('CREATE SCHEMA IF NOT EXISTS nlu;')

    cur.execute(
    """
    CREATE TABLE IF NOT EXISTS nlu.trained_models (
        model_id uuid NOT NULL UNIQUE,
        model text[] NOT NULL,
        creation_at TIMESTAMP WITH TIME ZONE NOT NULL default current_timestamp,
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL default current_timestamp,
        flags text[] default '{}'
    );
    """)
    print("Created table nlu.trained_models")

    try:
        file = config.find_one({'name': 'nlu_model'})
        database = 'nlu.trained_models'
        print('Got Mongofile:', file)

        data = {
            'model_id': str(uuid.uuid4()),
            'model': [file['payload']]
        }

        print('Created data object: ', data['model'])
        cur.execute(f'INSERT INTO {database} (model_id, model) VALUES (%s, %s)',
                    (data['model_id'], data['model']))
        print("Inserted : ", data['model_id'])
                                                                            
        cur.execute("SELECT COUNT(*) FROM nlu.trained_models")
        row = cur.fetchone()
        print("Number of rows:", row)
    except psycopg2.errors.UniqueViolation:
        print('Entry already exists.')
    finally:
        print('--------------------------------------------------------------------------------')
        print('--------------------------------------------------------------------------------')


def migrate_bot_predicates():
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    cur.execute('CREATE SCHEMA IF NOT EXISTS nlu;')

    cur.execute(
    """
    CREATE TABLE IF NOT EXISTS nlu.bot_predicates (
        predicate_id uuid NOT NULL UNIQUE,
        bot_predicates JSON NOT NULL,
        creation_at TIMESTAMP WITH TIME ZONE NOT NULL default current_timestamp,
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL default current_timestamp,
        flags text[] default '{}'
    );
    """)
    print("Created table nlu.bot_predicates")

    try:
        file = config.find_one({'name': 'luna_predicates'})
        database = 'nlu.bot_predicates'
        print('Got Mongofile:', json.dumps(file))

        data = {
            'predicate_id': str(uuid.uuid4()),
            'bot_predicates': json.dumps(file['bot_predicates'])
        }

        cur.execute('INSERT INTO nlu.bot_predicates (predicate_id, bot_predicates) VALUES (%s, %s)',
                    (data['predicate_id'], data['bot_predicates']))
        print("Inserted : ", data)
                                                                            
        cur.execute("SELECT COUNT(*) FROM nlu.bot_predicates")
        row = cur.fetchone()
        print("Number of rows:", row)
    except psycopg2.errors.UniqueViolation:
        print('Entry already exists.')
    finally:
        print('--------------------------------------------------------------------------------')
        print('--------------------------------------------------------------------------------')

def fetch_nlu_model():
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("SELECT model FROM nlu.trained_models LIMIT 1")
    row = cur.fetchone()
    decoded = codecs.decode(row[0][0].encode(), 'utf-8-sig')
    return json.loads(decoded)


def create_archive():
    # ARCHIVE
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS archive;')

    cur.execute(
    """
    CREATE TABLE archive (
        document_id uuid NOT NULL UNIQUE,                                                  
        title varchar NOT NULL,
        origin varchar(100) NOT NULL,
        payload text[] NOT NULL,
        creation_at TIMESTAMP WITH TIME ZONE NOT NULL default current_timestamp,
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL default current_timestamp,
        flags text[] default '{}'
    );
    """)
    print("Created table archive")


def migrate_rec_loc():
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS weather_location_default;')

    cur.execute(
    """
    CREATE TABLE IF NOT EXISTS weather_location_default (
        location_id UUID NOT NULL UNIQUE,
        lat_long text NOT NULL,
        creation_at TIMESTAMP WITH TIME ZONE NOT NULL default current_timestamp,
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL default current_timestamp,
        flags text[] default '{}'
    );
    """)
    print("Created table weather_location_default")

    # cur.execute("""
    #     CREATE OR REPLACE FUNCTION check_number_of_row
    #     RETURNS TRIGGER AS
    #     $body$
    #     BEGIN
    #         -- replace 100 by the number of rows you want
    #         IF (SELECT count(*) FROM your_table) > 1
    #         THEN 
    #             RAISE EXCEPTION 'INSERT statement exceeding maximum number of rows for this table' 
    #         END IF;
    #     END;
    #     $body$
    #     LANGUAGE plpgsql;

    #     CREATE TRIGGER tr_check_number_of_row 
    #     BEFORE INSERT ON weather_location_default
    #     FOR EACH ROW EXECUTE PROCEDURE check_number_of_row();

    #     );
    # """)
    # print('Created trigger for weather_location_default table')

    try:
        file = rec_loc.find_one({'delta': 1})
        database = 'weather_location_default'
        print('Got Mongofile:', json.dumps(file))

        data = {
            'location_id': str(uuid.uuid4()), 
            'lat_long': json.dumps(file['loc'])
        }
 
        print('Created data object:', data)
        cur.execute('INSERT INTO weather_location_default (location_id, lat_long) VALUES (%s, %s)',
                    (data['location_id'], data['lat_long']))
        print("Inserted : ", data)
                                                                            
        cur.execute("SELECT COUNT(*) FROM weather_location_default")
        row = cur.fetchone()
        print("Number of rows:", row)
    except psycopg2.errors.UniqueViolation:
        print('Entry already exists.')
    finally:
        print('--------------------------------------------------------------------------------')
        print('--------------------------------------------------------------------------------')

def fetch_coords():
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("SELECT lat_long FROM weather_location_default")
    row = cur.fetchone()
    print("Number of rows in files:", json.loads(row[0]))


def migrate_session_data():
    print('Migrating session_data')
    # SESSIONS
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS session_data;')

    cur.execute(
    """
    CREATE TABLE IF NOT EXISTS session_data (
        id UUID NOT NULL UNIQUE,
        text varchar NOT NULL,
        details jsonb default '{}',
        creation_at TIMESTAMP WITH TIME ZONE NOT NULL default current_timestamp,
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL default current_timestamp,
        flags text[] default '{}'
    );
    """)
    print("Created table session_data")

    
    for file in sessions.find():
        try:
            database = 'session_data'
            print('Got Mongofile:', file)
 
            data = {
                'id': str(uuid.uuid4()),
                'text': file['text']
            }
            print('Created data object: ', data)
            cur.execute("INSERT INTO session_data (id, text) VALUES (%s, %s)", (data['id'], data['text']))
            print("Inserted : ", data)
                                                                                
            cur.execute("SELECT COUNT(*) FROM session_data")
            row = cur.fetchone()
            print("Number of rows:", row)
        except psycopg2.errors.UniqueViolation:
            print('Entry already exists.')
        finally:
            print('--------------------------------------------------------------------------------')
            print('--------------------------------------------------------------------------------')

def count():
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT COUNT(*) FROM texts")
    row = cur.fetchone()
    print("Number of rows in files:", row)
    cur.execute("SELECT COUNT(*) FROM science")
    row = cur.fetchone()
    print("Number of rows in science:", row)
    cur.execute("SELECT COUNT(*) FROM intelligence")
    row = cur.fetchone()
    print("Number of rows in intelligence:", row)
    cur.execute("SELECT COUNT(*) FROM archive")
    row = cur.fetchone()
    print("Number of rows in archives:", row)
    cur.execute("SELECT COUNT(*) FROM nlu.trained_models")
    row = cur.fetchone()
    print("Number of rows in nlu.trained_models:", row)
    cur.execute("SELECT COUNT(*) FROM nlu.bot_predicates")
    row = cur.fetchone()
    print("Number of rows in nlu.bot_predicates:", row)
    cur.execute("SELECT COUNT(*) FROM weather_location_default")
    row = cur.fetchone()
    print("Number of rows in weather_location_default:", row)
    cur.execute("SELECT * FROM intelligence WHERE title = 'Botany'")
    row = cur.fetchone()
    print("Result:", row['creation_at'])
    cur.close()
    conn.close()

def get_quotes():
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("SELECT title, count(title) FROM texts ")
    rows = cur.fetchall()
    results = list(map((lambda row: row[0][0]), rows))
    for result in results:
        print(result)

migrate_science()