import connection
import time
import datetime


def get_submission_time():
    time_stamp_in_seconds = time.time()
    whole_seconds = int(time_stamp_in_seconds)

    submission_time = (datetime.datetime.utcfromtimestamp(int(str(whole_seconds))).strftime('%Y-%m-%d %H:%M:%S'))
    return submission_time


@connection.connection_handler
def get_questions(cursor, criteria, direction, number_of_questions=None):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY 
                      CASE WHEN %(criteria)s='submission_time' AND %(direction)s='DESC' THEN submission_time END DESC,
                      CASE WHEN %(criteria)s='submission_time' AND %(direction)s='ASC' THEN submission_time END ASC,                  
                      CASE WHEN %(criteria)s='vote_number' AND %(direction)s='DESC' THEN vote_number END DESC,
                      CASE WHEN %(criteria)s='vote_number' AND %(direction)s='ASC' THEN vote_number END ASC,
                      CASE WHEN %(criteria)s='view_number' AND %(direction)s='DESC' THEN view_number END DESC,
                      CASE WHEN %(criteria)s='view_number' AND %(direction)s='ASC' THEN view_number END ASC                        
                   LIMIT %(number_of_questions)s;
                   """,
                   {'number_of_questions': number_of_questions, 'criteria': criteria, 'direction': direction})
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def get_answer_message(cursor,answer_id):
    cursor.execute("""
                    SELECT message FROM answer
                    WHERE id = %(answer_id)s;
                   """, {'answer_id': int(answer_id)})
    return cursor.fetchone()


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
def get_list_of_answers(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE question_id = %(question_id)s;
                   """,
                   {'question_id': question_id})
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


@connection.connection_handler
def edit_existing_answer_data(cursor,new_message,answer_id):
    cursor.execute("""
                        UPDATE answer set message = %(new_message)s
                        WHERE id = %(answer_id)s;
                        """,
                   {"new_message": new_message,"answer_id":answer_id })
