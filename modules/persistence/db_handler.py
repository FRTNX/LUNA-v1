from annoyances import *
import configparser
import psycopg2.extras
import psycopg2.errors
import sqlite3
import codecs
import json
import time
import uuid
import os

config = configparser.ConfigParser()
config.read('modules/persistence/db.ini')

def _open(database = config['defaults']['db']):
    if database == 'sqlite':
        database = config['sqlite']['db']
        conn = sqlite3.connect(database) # read database path from config
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        return conn, cur
    else:
        conn = psycopg2.connect(
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PWD'),
            host = config['postgresql']['host'],
            port = config['postgresql']['port'],
            database = config['postgresql']['db']
        )
        
        conn.set_session(autocommit=True)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        return conn, cur 


def _close(connection, cursor):
    connection.close()
    cursor.close()


def list_titles_by_origin(origin='science'):
    conn, cur = _open()
    cur.execute(f"SELECT title FROM intelligence WHERE origin = '{origin}'")
    rows = cur.fetchall()
    _close(conn, cur)
    return list(map((lambda row: row[0]), rows))


def list_titles_by_tag(tag):
    conn, cur = _open()
    if tag == 'random':
        # cur.execute(f"SELECT title FROM intelligence WHERE 'kardeshev_scale' = ANY (tags) ORDER BY RANDOM() LIMIT 80")
        cur.execute(f"SELECT title FROM intelligence ORDER BY RANDOM() LIMIT 60")
    else:
        cur.execute(f"SELECT title FROM intelligence WHERE '{tag}' = ANY (tags)")
    rows = cur.fetchall()
    _close(conn, cur)
    return list(map((lambda row: row[0]), rows))


def fetch_title_suggestions():
    conn, cur = _open()
    cur.execute(f"SELECT title FROM intelligence ORDER BY RANDOM() LIMIT 100")
    rows = cur.fetchall()
    _close(conn, cur)
    return list(map((lambda row: row[0]), rows))

def fetch_archive_list():
    conn, cur = _open()
    cur.execute(f"SELECT title FROM archive")
    rows = cur.fetchall()
    _close(conn, cur)
    return list(map((lambda row: row[0]), rows))


def list_exploits():
    return 'not implemented'


def fetch_quote(database = config['defaults']['db']):
    conn, cur = _open(database)
    cur.execute("SELECT payload FROM texts WHERE document_type IN ('ETHOS', 'AI', 'MATH') ORDER BY RANDOM() LIMIT 1")
    rows = cur.fetchone()
    if (database == 'postgresql'):
        _close(conn, cur)
        return rows[0][0]
    else:
        return rows[0]


def insert_quote(quote):
    conn, cur = _open()

    data = {
        'document_id': str(uuid.uuid4()),
        'document_type': 'ETHOS',
        'title': 'default', # todo: extract quote source and use as title, 
        'database': 'texts',
        'payload': [quote]
    }
    
    try:
        cur.execute("INSERT INTO texts (document_id, document_type, title, origin, payload) VALUES (%s, %s, %s, %s, %s)",
            (data['document_id'], data['document_type'], data['title'], data['database'], data['payload']))
    except psycopg2.errors.UniqueViolation:
        raise ValueError('Entry already exists: %s' % quote)
    _close(conn, cur)
    return 'Inserted : %s' % data['payload'][0]


def clean_quotes():
    conn, cur = _open()

    stop_words = open('data/meta/stop_words.txt', 'r').read().split('\n')
    patterns = 'de puta madre'
    for word in stop_words:
        if len(word) > 0 and "'" not in word:
            patterns += f'|{word}'

    try:
        pre_count = count_quotes()
        cur.execute("DELETE FROM texts WHERE document_type = 'ETHOS' AND LOWER(payload[1]) ~ '(%s)'" % patterns)
        post_count = count_quotes()
        deleted = pre_count - post_count
        _close(conn, cur)
        return f'Database cleansing complete. Deleted {deleted} quotes ({pre_count} => {post_count}).'
    except Exception as e:
        _close(conn, cur)
        return 'Error while cleaning database: %s' % e


def count_quotes():
    conn, cur = _open()
    cur.execute("SELECT COUNT(*) FROM texts WHERE document_type = 'ETHOS'")
    row = cur.fetchone()
    _close(conn, cur)
    return row[0]


def fetch_koan():
    conn, cur = _open()
    cur.execute("SELECT payload FROM texts WHERE document_type = 'KOAN' ORDER BY RANDOM() LIMIT 1")
    row = cur.fetchone()
    _close(conn, cur)
    return row[0][0]


def clean(text):
    return text.replace('\\\\', '').replace('u2013', ' ')


def fetch_reading_list(database = config['defaults']['db']):
    conn, cur = _open(database)

    res = cur.execute(f"SELECT title FROM intelligence WHERE 'PIN_TO_START' = ANY (flags) ORDER BY RANDOM() LIMIT 5") \
        if database == 'postgresql' else cur.execute(f"SELECT title FROM pinned_intel ORDER BY RANDOM() LIMIT 5")

    pinned_rows = cur.fetchall()
    pinned_articles = list(map((lambda row: row[0]), pinned_rows)) if database == 'postgresql' \
        else list(map((lambda row: clean(row['title'])), pinned_rows))

    extraction_quota = 5 - len(pinned_articles)

    if extraction_quota > 0:
        cur.execute(f'SELECT title FROM intelligence ORDER BY RANDOM() LIMIT {extraction_quota}')
        rows = cur.fetchall()
        random_articles = list(map((lambda row: row[0]), rows)) if database == 'postgresql' \
            else list(map((lambda row: clean(row['title'])), rows))

        _close(conn, cur) if database == 'postgresql' else None
        return pinned_articles + random_articles
    else:
        _close(conn, cur)
        return pinned_articles


def fetch_distinct_tags():
    conn, cur = _open()
    cur.execute('SELECT DISTINCT unnest(tags) as unique_tags FROM intelligence')
    rows = cur.fetchall()
    _close(conn, cur)
    return list(map((lambda row: row[0]), rows))


def tag_count(tag):
    conn, cur = _open()
    cur.execute(f"SELECT COUNT(*) FROM intelligence WHERE '{tag}' = ANY (tags)")
    rows = cur.fetchall()
    _close(conn, cur)
    return list(map((lambda row: row[0]), rows))


def fetch_distinct_origins():
    conn, cur = _open()
    cur.execute(f'SELECT DISTINCT origin FROM intelligence')
    rows = cur.fetchall()
    _close(conn, cur)
    return list(map((lambda row: row[0]), rows))


def origin_count(origin):
    conn, cur = _open()
    cur.execute(f"SELECT COUNT(*) FROM intelligence WHERE origin = '{origin}'")
    rows = cur.fetchall()
    _close(conn, cur)
    return list(map((lambda row: row[0]), rows))


def merge_relation_by_tag(tag, destination_relation='intelligence'):
    conn, cur = _open()

    try:
        cur.execute(f"UPDATE intelligence SET tags = array_remove(tags, '{tag}') WHERE '{tag}' = ANY (tags)")
        _close(conn, cur)
        return f'Successfuly merged relation {tag} to {destination_relation}'
    except Exception as e:
        _close(conn, cur)
        return f'Error merging relation {tag}: {e}'


def merge_all_relations_by_tag():
    conn, cur = _open()

    protected_relations = ['science']

    try:
        # support array of protected relations
        cur.execute("UPDATE intelligence SET tags = '{\"intelligence\"}' WHERE NOT ('science' = ANY (tags))")
        cur.execute("UPDATE intelligence SET tags = '{\"science\"}' WHERE 'science' = ANY (tags)")
        _close(conn, cur)
        return 'Successfuly merged relations'
    except Exception as e:
        _close(conn, cur)
        return f'Error merging relations: {e}'


def merge_relation_by_origin(source_relation, destination_relation='intelligence'):
    conn, cur = _open()

    try:
        cur.execute(f"UPDATE intelligence SET origin = %s WHERE origin = %s", (destination_relation, source_relation))
        _close(conn, cur)
        return f'Successfuly merged relation {source_relation} to {destination_relation}'
    except Exception as e:
        _close(conn, cur)
        return f'Error merging relation {source_relation}: {e}'


def merge_all_relations_by_origin():
    conn, cur = _open()

    protected_relations = ['science']

    try:
        # support array of protected relations
        cur.execute("UPDATE intelligence SET origin = 'intelligence' WHERE origin != 'science'")
        _close(conn, cur)
        return 'Successfuly merged relations'
    except Exception as e:
        _close(conn, cur)
        return f'Error merging relations: {e}'


def get_document(database, title):
    conn, cur = _open()

    cur.execute(f'SELECT payload, flags FROM {database} WHERE SIMILARITY (title, LOWER(%s)) > 0.7', (title.lower(),))
    row = cur.fetchone()

    if not row:
        _close(conn, cur)
        raise TypeError('No record found.')

    if (len(row[1]) > 0 and 'PIN_TO_START' in row[1]):
        cur.execute(f"UPDATE {database} SET flags = array_remove(flags, 'PIN_TO_START') WHERE LOWER(title) = '{title.lower()}'")
        
    _close(conn, cur)
    return row[0][0]


def insert_document(database, title, body):
    valid_databases = ['intelligence', 'archive']
    if database not in valid_databases:
        raise TypeError('Invalid database')

    conn, cur = _open()

    data = {
        'document_id': str(uuid.uuid4()),
        'title': title,
        'database': database,
        'payload': [body]
    }

    try:
        cur.execute(f'INSERT INTO {database} (document_id, title, origin, payload) VALUES (%s, %s, %s, %s)',
            (data['document_id'], data['title'], data['database'], data['payload']))
    except psycopg2.errors.UniqueViolation:
        _close(conn, cur)
        raise ValueError('Entry already exists: %s' % title)
    except Exception as e:
        _close(conn, cur)
        return f'Error inserting {title}: {e}'
    _close(conn, cur)
    return f'Inserted {title} into {database}'


def delete_document(title):
    conn, cur = _open()

    data = { 'title': title, 'database': 'intelligence' }

    try:
        cur.execute("DELETE FROM %s WHERE title = '%s'" % (data['database'], data['title']))
        _close(conn, cur)
        return f'Deleted {title} from {data["database"]}'
    except Exception as e:
        _close(conn, cur)
        raise ValueError(f'Error while deleting {title}: {e}')


def find_occurances(search_term):
    conn, cur = _open()

    condition1 = f"LOWER(title) LIKE ' %{search_term.lower()}% '"
    condition2 = f"LOWER(title) LIKE '{search_term.lower()}%'"
    condition3 = f"LOWER(title) LIKE '%{search_term.lower()}'"
    condition4 = f"LOWER(title) LIKE '-%{search_term.lower()}'"
    condition5 = f"LOWER(title) LIKE '{search_term.lower()}%-'"
    condition6 = f"LOWER(title) LIKE '{search_term.lower()}%)'"
    condition7 = f"LOWER(title) LIKE '(%{search_term.lower()}'"

    cur.execute(f"SELECT title FROM intelligence WHERE {condition1} OR {condition2} OR {condition3} OR {condition4} OR {condition5} OR {condition6} OR {condition7}")
    rows = cur.fetchall()

    if not rows:
        _close(conn, cur)
        raise TypeError('No records found.')
        
    _close(conn, cur)
    return list(map((lambda row: row[0]), rows))


def get_db_count(database):
    conn, cur = _open()

    cur.execute(f'SELECT COUNT(*) FROM {database}')
    row = cur.fetchone()
    _close(conn, cur)
    return row[0]


def fetch_bot_predicates():
    conn, cur = _open()

    cur.execute("SELECT bot_predicates FROM nlu.bot_predicates LIMIT 1") # order by creation date
    row = cur.fetchone()
    _close(conn, cur)
    return row[0]


def insert_session_data(data):
    conn, cur = _open()

    data = {
        'id': str(uuid.uuid4()),
        'text': data
    }

    try:
        cur.execute("INSERT INTO session_data (id, text) VALUES (%s, %s)", (data['id'], data['text']))
        _close(conn, cur)
        return f'Inserted: {data}'
    except Exception as e:
        _close(conn, cur)
        return f'Error inserting session data: {e}'
                                    


def fetch_nlu_model():
    conn, cur = _open()

    cur.execute("SELECT model FROM nlu.trained_models LIMIT 1") # todo: order by creation date
    row = cur.fetchone()
    decoded = codecs.decode(row[0][0].encode(), 'utf-8-sig')
    _close(conn, cur)
    return json.loads(decoded)


def save_nlu_model(model_path):
    model = open(model_path, 'r').read()
    if not model:
        raise ValueError('No model found')

    conn, cur = _open()

    database = 'nlu.trained_models'

    data = {
        'model_id': str(uuid.uuid4()),
        'model': [model]
    }

    try:
        cur.execute(f'INSERT INTO {database} (model_id, model) VALUES (%s, %s)',
                    (data['model_id'], data['model']))
        _close(conn, cur)
        return f'Inserted model: {data["model_id"]}'
    except Exception as e:
        _close(conn, cur)
        return f'Error storing new model: {e}'


def update_doc_flags(database, title, flag):
    conn, cur = _open()
    response = ''

    try:
        cur.execute(f"UPDATE {database} SET flags = array_append(flags, '{flag}') WHERE LOWER(title) = '{title.lower()}'")
        response = f'Successfully flagged {title}'
    except Exception as e:
        _close(conn, cur)
        response = f'Error flagging {title}: {e}'
    finally:
        _close(conn, cur)
        return response    


def clear_all_pins():
    conn, cur = _open()

    flag = 'PIN_TO_START'
    response = ''

    try:
        cur.execute(f"UPDATE intelligence SET flags = array_remove(flags, '{flag}') WHERE '{flag}' = ANY (flags)")
        response = 'Successfully removed all pinned documents'
    except Exception as e:
        response = f'Error clearing pins: {e}'
    finally:
        _close(conn, cur)
        return response       


def insert_note(note):
    return 'not implemented'


def get_note(keyword):
    return 'not implemented'


def list_all_notes():
    return 'not implemented'


def fetch_coords():
    conn, cur = _open()

    cur.execute("SELECT lat_long FROM weather_location_default")
    row = cur.fetchone()
    coords = json.loads(row[0])
    _close(conn, cur)
    return coords


def insert_coords(coords):
    conn, cur = _open()

    data = {
        'location_id': str(uuid.uuid4()), 
        'lat_long': json.dumps(coords)
    }

    try:
        cur.execute('INSERT INTO weather_location_default (location_id, lat_long) VALUES (%s, %s)',
                    (data['location_id'], data['lat_long']))
        _close(conn, cur)
        return f'Inserted : {data}'
    except Exception as e:
        _close(conn, cur)
        return f'Could not save coordinates: {e}'


def clear_recent_locations():
    conn, cur = _open()

    try:
        cur.execute("DELETE FROM weather_location_default")
        _close(conn, cur)
        return 'Cleared recent locations'
    except Exception as e:
        _close(conn, cur)
        return  'Error deleting recent locations: %s' % e


def insert_weather_data(data):
    return 'not implemented'


def fetch_weather_data():
    return 'not implemented'


def get_known_users():
    conn, cur = _open()

    cur.execute("SELECT user_name FROM users")
    rows = cur.fetchall()
    _close(conn, cur)
    return list(map((lambda row: row[0].lower()), rows))


def insert_new_user(user):
    conn, cur = _open()

    data = {
        'user_id': str(uuid.uuid4()),
        'user_name': user
    }

    try:
        cur.execute("INSERT INTO users (user_id, user_name) VALUES (%s, %s)", (data['user_id'], data['user_name']))
        _close(conn, cur)
        return f'Inserted : {data}'
    except Exception as e:
        _close(conn, cur)
        return f'Error inserting new user: {e}'


def delete_user():
    return 'not implemented'
