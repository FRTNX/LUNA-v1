import mock
import pytest
from pytest_mock import mocker
import psycopg2.errors
from unittest.mock import Mock
from index import *


# todo: test error handling

def test_list_titles_by_origin():
    test_titles = list_titles_by_origin()
    assert type(test_titles) == list
    assert len(test_titles) > 0
    return

def test_list_titles_by_tag():
    test_titles = list_titles_by_tag('intelligence')
    assert type(test_titles) == list
    assert len(test_titles) > 0
    return

def test_list_exploits():
    assert list_exploits() == ''
    return

def test_fetch_quote():
    assert type(fetch_quote()) == str
    assert len(fetch_quote()) > 0
    return

def test_clean_quotes():
    return

def test_insert_quote():
    return

def test_count_quotes():
    quote_count = count_quotes()
    assert type(quote_count) == int
    assert quote_count > 0
    return

def test_fetch_koan():
    test_koan = fetch_koan()
    assert type(test_koan) == str
    assert len(test_koan) > 0
    return

def test_fetch_reading_list():
    reading_list = fetch_reading_list()
    assert type(reading_list) == list
    assert len(reading_list) == 5
    return

def test_fetch_distinct_tags():
    test_tags = fetch_distinct_tags()
    assert type(test_tags) == list
    assert len(test_tags) > 0
    return

def test_tag_count():
    test_count = tag_count('intelligence')
    assert type(test_count) == list
    assert type(test_count[0]) == int
    assert test_count[0] > 0 
    return

def test_fetch_distinct_origins():
    test_origins = fetch_distinct_origins()
    assert type(test_origins) == list
    assert len(test_origins) > 0
    return

def test_origin_count():
    test_count = origin_count('intelligence')
    assert type(test_count) == list
    assert type(test_count[0]) == int
    assert test_count[0] > 0
    return


def test_merge_relation_by_tag():
    with mock.patch('psycopg2.connect') as mock_connect:
        mock_connect.cursor.return_value.execute.return_value = []
        test_op = merge_relation_by_tag('test_tag')
        assert test_op == 'Successfuly merged relation test_tag to intelligence'
    return

def test_merge_all_relations_by_tag():
    with mock.patch('psycopg2.connect') as mock_connect:
        mock_connect.cursor.return_value.execute.return_value = []
        test_op = merge_all_relations_by_tag()
        assert test_op == 'Successfuly merged relations'
    return

def test_merge_relation_by_origin():
    with mock.patch('psycopg2.connect') as mock_connect:
        mock_connect.cursor.return_value.execute.return_value = []
        test_op = merge_relation_by_origin('test_origin')
        assert test_op == 'Successfuly merged relation test_origin to intelligence'
    return

def test_merge_all_relations_by_origin():
    with mock.patch('psycopg2.connect') as mock_connect:
        mock_connect.cursor.return_value.execute.return_value = []
        test_op = merge_all_relations_by_origin()
        assert test_op == 'Successfuly merged relations'
    return

def test_get_document():
    test_doc = get_document('intelligence', 'science')
    assert type(test_doc) == str
    assert len(test_doc) > 0
    return

def test_insert_document():
    test_insertion = insert_document('intelligence', 'Test', 'test')
    assert test_insertion == 'Inserted Test into intelligence'
    return

def test_delete_document():
    test_deletion = delete_document('Test')
    assert test_deletion == 'Deleted Test from intelligence'
    return

def test_get_db_count():
    test_count = get_db_count('intelligence')
    assert type(test_count) == int
    assert test_count > 0
    return

def test_fetch_bot_predicates():
    test_predicates = fetch_bot_predicates()
    expected_keys = [
        'name', 'botmaster', 'city', 'master', 'language', 'birthplace', 'birthday', 'phylum', 'state',
        'email', 'mother', 'nationality', 'species', 'location', 'gender', 'order', 'favoriteband',
        'kindmusic', 'favoritemovie', 'favoriteactress', 'bestfriend', 'dislikes', 'father',
        'favoritecheese', 'favoritecolor', 'favoritefood', 'favoritemovie', 'favoritesinger',
        'favoritesong', 'firstname', 'friend', 'nickname', 'pet', 'religion', 'likes'
    ]
    assert type(test_predicates) == list
    assert len(test_predicates) == 35
    for predicate in test_predicates:
        assert type(predicate) == dict
        assert len(list(predicate.keys())) > 0 and list(predicate.keys())[0] in expected_keys 
    return

def test_insert_session_data():
    with mock.patch('psycopg2.connect') as mock_connect:
        mock_connect.cursor.return_value.execute.return_value = []
        test_op = insert_session_data('Test')
        assert test_op.startswith('Inserted:')
    return

def test_fetch_nlu_model():
    test_model = fetch_nlu_model()
    assert type(test_model) == dict
    assert list(test_model.keys()) == ['rasa_nlu_data']
    return

def test_save_nlu_model():
    with mock.patch('psycopg2.connect') as mock_connect:
        mock_connect.cursor.return_value.execute.return_value = []
        test_op = save_nlu_model('../data/nlu/nlu.json')
        assert test_op.startswith('Inserted model: ')
    return

def test_update_doc_flags():
    with mock.patch('psycopg2.connect') as mock_connect:
        mock_connect.cursor.return_value.execute.return_value = []
        test_op = update_doc_flags('intelligence', 'Test', 'test')
        assert test_op == 'Successfully flagged Test'
    return

def test_clear_all_pins():
    with mock.patch('psycopg2.connect') as mock_connect:
        mock_connect.cursor.return_value.execute.return_value = []
        test_op = clear_all_pins()
        assert test_op == 'Successfully removed all pinned documents'
    return

def test_insert_note():
    assert insert_note('dummy') == 'not implemented'
    return

def test_get_note():
    assert get_note('dummy') == 'not implemented'
    return

def test_list_all_notes():
    assert list_all_notes() == 'not implemented'
    return

def test_fetch_coords():
    test_coords = fetch_coords()
    assert type(test_coords) == list
    assert len(test_coords) == 2
    for coord in test_coords:
        assert type(coord) == float
    return

def test_insert_coords():
    with mock.patch('psycopg2.connect') as mock_connect:
        mock_connect.cursor.return_value.execute.return_value = []
        test_op = insert_coords([37.234332396, -115.80666344])
        assert test_op.startswith('Inserted : ')
    return

def test_clear_recent_locations():
    with mock.patch('psycopg2.connect') as mock_connect:
        mock_connect.cursor.return_value.execute.return_value = []
        test_op = clear_recent_locations()
        assert test_op == 'Cleared recent locations'
    return

def test_insert_weather_data():
    assert insert_weather_data('dummy') == 'not implemented'
    return

def test_fetch_weather_data():
    assert fetch_weather_data() == 'not implemented'
    return

def test_get_known_users():
    test_users = get_known_users()
    assert type(test_users) == list
    return 

def test_insert_new_user():
    with mock.patch('psycopg2.connect') as mock_connect:
        mock_connect.cursor.return_value.execute.return_value = []
        test_op = insert_new_user('Test')
        assert test_op.startswith('Inserted : ')
    return

def test_delete_user():
    return
