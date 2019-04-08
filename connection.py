"""import csv

DATA_HEADER_QUESTION = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
DATA_HEADER_ANSWER = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
DATA_HEADER_NUMBER = ["number"]


def get_data_from_file(filename):
    with open(filename, "r") as file:
        result = []
        if filename == "sample_data/question.csv":
            stories = csv.DictReader(file, fieldnames=DATA_HEADER_QUESTION)
        elif filename == "sample_data/answer.csv":
            stories = csv.DictReader(file, fieldnames=DATA_HEADER_ANSWER)
        elif filename == "sample_data/question_number.csv":
            stories = csv.DictReader(file, fieldnames=DATA_HEADER_NUMBER)
        elif filename == "sample_data/answer_number.csv":
            stories = csv.DictReader(file, fieldnames=DATA_HEADER_NUMBER)
        for row in stories:
            result.append(dict(row))
        return result


def write_data_to_file(filename, list_of_dicts):
    with open(filename, "w") as file:
        if filename == "sample_data/question.csv":
            stories = csv.DictWriter(file, fieldnames=DATA_HEADER_QUESTION)
        elif filename == "sample_data/answer.csv":
            stories = csv.DictWriter(file, fieldnames=DATA_HEADER_ANSWER)
        elif filename == "sample_data/question_number.csv":
            stories = csv.DictWriter(file, fieldnames=DATA_HEADER_NUMBER)
        elif filename == "sample_data/answer_number.csv":
            stories = csv.DictWriter(file, fieldnames=DATA_HEADER_NUMBER)
        stories.writeheader()
        for row in list_of_dicts:
            stories.writerow(row)
"""

# Creates a decorator to handle the database connection/cursor opening/closing.
# Creates the cursor with RealDictCursor, thus it returns real dictionaries, where the column names are the keys.
import os
import psycopg2
import psycopg2.extras


def get_connection_string():
    # setup connection string
    # to do this, please define these environment variables first
    user_name = os.environ.get('PSQL_USER_NAME')
    password = os.environ.get('PSQL_PASSWORD')
    host = os.environ.get('PSQL_HOST')
    database_name = os.environ.get('PSQL_DB_NAME')

    env_variables_defined = user_name and password and host and database_name

    if env_variables_defined:
        # this string describes all info for psycopg2 to connect to the database
        return 'postgresql://{user_name}:{password}@{host}/{database_name}'.format(
            user_name=user_name,
            password=password,
            host=host,
            database_name=database_name
        )
    else:
        raise KeyError('Some necessary environment variable(s) are not defined')


def open_database():
    try:
        connection_string = get_connection_string()
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception
    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        # we set the cursor_factory parameter to return with a RealDictCursor cursor (cursor which provide dictionaries)
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value

    return wrapper
