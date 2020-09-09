import os
import sys
import getopt
import random
import time
import uuid
import json
import wikipedia
import psycopg2.extras
import psycopg2.errors
from colorama import Fore
from func_timeout.StoppableThread import StoppableThread
from requests.exceptions import ConnectionError


# todo: read db connection details from env vars or protected config file
PROTECTED_TABLES = ['science', 'intelligence', 'texts', 'archive', 'session_data', 'users', 'weather_location_default', 'random']
READ_ONLY_TABLES = ['texts', 'archive', 'session_data', 'users', 'weather_location_default']

state = []
extracted = []
extraction_queue = [{ }]

def load_state():
    global state
    state = list_titles('intelligence')


def connect():
    return psycopg2.connect(user = os.getenv('DB_USER'), password = os.getenv('DB_PWD'), host = '127.0.0.1', port = '5432', database = 'luna')


def extract_and_insert_initial(database, topic):
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    try:
        res = wikipedia.page(topic)
        content = res.content
        insert_document(database, topic, content)
        print('[+] Root document found.')
    except ConnectionError:
        print('[+] Offline. Searching for root document locally.')
        extract_document(database, topic)
        if (extraction_count(database) > 0):
            print('[+] Root document found.')
        else:
            # todo: remove target from extraction list where this error is caught, continue with other targets
            raise IndexError('Root document not found locally. This extraction requires internet.')

    conn.close()
    cur.close()


def extract_document(database, title):
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    cur.execute(f"""INSERT INTO {database} SELECT * FROM intelligence WHERE LOWER(title) = '{title.lower()}' ON CONFLICT (title) DO NOTHING;""")
    conn.close()
    cur.close()    


def extract_and_insert_relations(database):
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    print(f'[+] Got extraction queue: {extraction_queue}')
    random.shuffle(extraction_queue)
    for topic in extraction_queue[0][database]:
        if topic.lower() not in list_titles(database) + state:
            try:
                res = wikipedia.page(topic)
                content = res.content
                insert_document(database, topic, content)
                extraction_queue[0][database].remove(topic)
                extracted.append(topic)
            except ConnectionError as e:
                print(f'[-] Offline. Skipped {topic}')
            except Exception as e:
                print(f'[-] Error extracting {topic}: {e}')
        else:
            print(f'[-] {topic} already exists. Creating relation.')
            update_tag(topic, database)
            extracted.append(topic)
            
    conn.close()
    cur.close()


def extraction_count(database):
    try:
        conn = connect()
        conn.set_session(autocommit=True)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(f"SELECT COUNT(*) FROM {database.replace(' ', '_').replace('-', '_')}")
        rows = cur.fetchall()
        conn.close()
        cur.close()
        return rows[0][0]
    except Exception as e:
        print(f'[-] Error counting extracted items: {e}')
        return 0


def update_tag(title, relation):
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    cur.execute(f"""UPDATE intelligence SET tags = array_append(tags, '{relation}') WHERE LOWER(title) = '{title.lower()}' AND NOT ('{relation}' = ANY (tags));""")
    print(f'[+] --------------------- Updated {title}')
    cur.execute(f"""INSERT INTO {relation} SELECT * FROM intelligence WHERE LOWER(title) = '{title.lower()}' ON CONFLICT (title) DO NOTHING;""")
    conn.close()
    cur.close()


def update_origin(title, origin):
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    cur.execute(f"""UPDATE intelligence SET origin = '{origin}' WHERE LOWER(title) = '{title.lower()}';""")
    print(f'[+] --------------------- Updated {title}')
    cur.execute(f"""INSERT INTO {origin} SELECT * FROM intelligence WHERE LOWER(title) = '{title.lower()}' ON CONFLICT (title) DO NOTHING;""")
    conn.close()
    cur.close()


def origin_count(origin):
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f"SELECT COUNT(*) FROM intelligence WHERE origin = '{origin}'")
    rows = cur.fetchall()
    conn.close()
    cur.close()
    return list(map((lambda row: row[0]), rows))


def create_database(database_name):
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    if (database_name not in PROTECTED_TABLES):
        cur.execute(f'DROP TABLE IF EXISTS {database_name} CASCADE;')

        cur.execute(
        f"""CREATE TABLE IF NOT EXISTS {database_name} (
            document_id uuid NOT NULL UNIQUE,                                                      
            title varchar NOT NULL UNIQUE,
            origin varchar(100) NOT NULL,
            payload text[] NOT NULL,
            creation_at TIMESTAMP WITH TIME ZONE NOT NULL default current_timestamp,
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL default current_timestamp,
            flags text[] default null,
            tags text[] default null
        );""")
        print(f'[+] Created table: {database_name}')
        
        conn.close()
        cur.close()
    else:
        raise TypeError('[-] Cannot update protected database.')


def insert_document(database, title, body):
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    data = {
        'document_id': str(uuid.uuid4()),
        'title': title,
        'database': database,
        'payload': [body]
    }

    try:
        cur.execute(f'INSERT INTO {database} (document_id, title, origin, payload, tags) VALUES (%s, %s, %s, %s, %s)',
            (data['document_id'], data['title'], data['database'], data['payload'], '{"' + database + '"}'))
        print('[+] ' + Fore.BLUE + f'{database}: {get_db_count(database)} ' + Fore.RESET + f'- Inserted {title} into {database}')
    except psycopg2.errors.UniqueViolation:
        print('[-] Entry already exists: %s' % title)
    
    conn.close()
    cur.close()


def list_titles(database):
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f'SELECT title FROM {database}')
    rows = cur.fetchall()
    # print(f'[+] Got titles: {list(map((lambda row: row[0].lower()), rows))}')
    return list(map((lambda row: row[0].lower()), rows))
    conn.close()
    cur.close()


def get_db_count(database):
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(f'SELECT COUNT(*) FROM {database}')
    row = cur.fetchone()
    return row[0]
    conn.close()
    cur.close()


def prepare_listing(database):
    global extraction_queue
    conn = connect()
    conn.set_session(autocommit=True)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    count = 0
    extraction_queue[0][database] = []
    extracted = list_titles(database)
    random.shuffle(extracted)
    for title in extracted:
        cursor.execute('SELECT payload FROM ' + database + ' WHERE LOWER(title) = %s', (title.lower(),))
        idx = cursor.fetchall()
        index = idx[0][0][0]
        try:
            start = index.lower().find('see also ==') # or See alsoEdit ==
            segment_start = index[start:]
            segment_end = segment_start[:segment_start.find('\n\n\n')]
            relations = segment_end.split('\n')
            if relations != [''] and relations != ['See also ==']:
                for relation in relations:
                    if 'also ==' not in relation.lower() and relation != '':
                        if relation.lower() not in list_titles(database):
                            print(f'[+] Queueing: {relation}')
                            # print(f'ExtractionQ for {database}:' + str(extraction_queue[0][database]))
                            extraction_queue[0][database].append(relation)
                            count += 1
        except Exception as e:
            print(f'[-] {e}')
            pass

    conn.close()
    cursor.close()
    print(f'[+] {len(extracted)} file(s) gave us {count} relations.')
    time.sleep(2)
    return count, len(extracted)


def t1(database):
    try:
        extract_and_insert_relations(database)
    except Exception as e:
        print(f'[-] Error in thread: {e}')
        pass


def setup_thread(database):
    thread = StoppableThread(name='t1', target=t1, args=(database,))
    thread.daemon = True
    return thread


# multiple threads currently have little effect
def parallel_extraction(database):
    max_threads = 1
    for i in range(max_threads):
        setup_thread(database).start();print(f'[+] STARTING ENGINE {i}')


def consolidate_dbs(interests):
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    try:
        for interest in interests:
            table = interest.lower().replace(' ', '_').replace('-', '_')
            cur.execute(f"INSERT INTO intelligence SELECT * FROM {table} ON CONFLICT (title) DO UPDATE SET tags = array_append(intelligence.tags, %s) WHERE NOT (%s = ANY (intelligence.tags));", (table, table))
            print(f'[+] Merged {table} into intelligence')
    except psycopg2.errors.UndefinedTable:
        pass

    conn.close()
    cur.close()


def cleanup(interests):
    conn = connect()
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    for interest in interests:
        table = interest.lower().replace(' ', '_').replace('-', '_')
        if (interest not in PROTECTED_TABLES):
            cur.execute(f'DROP TABLE IF EXISTS {table} CASCADE;')
            print(f'[+] Deleted temp table: {table}')
        else:
            print(f'[+] {table} table is protected. Table left intact.')

    conn.close()
    cur.close()


# move to utilities file
def color(text, color):
    # todo: create color mapper (one giant switch case, which returns the result of a statement as below)
    return Fore.LIGHTBLACK_EX + u"\u25CF " + Fore.RESET
