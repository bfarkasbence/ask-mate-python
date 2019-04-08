import connection
import time
import datetime


def get_submission_time():
    time_stamp_in_seconds = time.time()
    whole_seconds = int(time_stamp_in_seconds)

    submission_time = (datetime.datetime.utcfromtimestamp(int(str(whole_seconds))).strftime('%Y-%m-%d %H:%M:%S'))
    return submission_time


@connection.connection_handler
def get_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question;
                   """,)
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def get_question_data_by_id(cursor, id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(id)s;
                   """,
                   {'id': id})
    question = cursor.fetchall()
    return question


@connection.connection_handler
def get_list_of_answers(cursor, id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id = %(id)s;
                   """,
                   {'id': id})
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def complement_new_question_data(cursor, title, message, image):
    submission_time = get_submission_time()
    cursor.execute("""
                    INSERT INTO question ("submission_time", "vote_number", "view_number", "title", "message", "image")
                    VALUES (%(submission_time)s, 0, 0, %(title)s, %(message)s, %(image)s); """,
                   {"submission_time": submission_time, "title": title, "message": message, "image": image})


@connection.connection_handler
def complement_new_answer_data(cursor, message, image, question_id):
    submission_time = get_submission_time()
    cursor.execute("""
                    INSERT INTO answer ("submission_time", "vote_number", "question_id", "message", "image")
                    VALUES  (%(submission_time)s, 0, %(question_id)s, %(message)s, %(image)s); """,
                   {"submission_time": submission_time, "question_id": question_id, "message": message, "image": image})
