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
def get_answer_message_and_question_id(cursor,answer_id):
    cursor.execute("""
                    SELECT message,question_id FROM answer
                    WHERE id = %(answer_id)s;
                   """, {'answer_id': int(answer_id)})
    return cursor.fetchone()


@connection.connection_handler
def get_question_data_by_id(cursor, question_id):
    cursor.execute("""
                    SELECT question.*, users.username FROM question LEFT JOIN users ON question.user_id = users.id
                    WHERE question.id = %(id)s;
                   """,
                   {'id': question_id})
    question = cursor.fetchall()
    return question


@connection.connection_handler
def get_list_of_answers(cursor, question_id):
    cursor.execute("""
                    SELECT answer.*, users.username FROM answer LEFT JOIN users ON answer.user_id = users.id
                    WHERE answer.question_id = %(question_id)s
                    ORDER BY vote_number DESC;
                   """,
                   {'question_id': question_id})
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def complement_new_question_data(cursor, title, message, image, user_id):
    submission_time = get_submission_time()
    cursor.execute("""
                    INSERT INTO question ("submission_time", "vote_number", "view_number", "title", "message", "image", "user_id")
                    VALUES (%(submission_time)s, 0, 0, %(title)s, %(message)s, %(image)s, %(user_id)s); """,
                   {"submission_time": submission_time, "title": title, "message": message, "image": image, "user_id": user_id})


@connection.connection_handler
def complement_new_answer_data(cursor, message, image, question_id, user_id):
    submission_time = get_submission_time()
    cursor.execute("""
                    INSERT INTO answer ("submission_time", "vote_number", "question_id", "message", "image","user_id")
                    VALUES  (%(submission_time)s, 0, %(question_id)s, %(message)s, %(image)s, %(user_id)s); """,
                   {"submission_time": submission_time, "question_id": question_id, "message": message, "image": image, "user_id":user_id})


@connection.connection_handler
def edit_existing_answer_data(cursor,new_message,answer_id):
    cursor.execute("""
                        UPDATE answer set message = %(new_message)s
                        WHERE id = %(answer_id)s;
                        """,
                   {"new_message": new_message, "answer_id": answer_id})


@connection.connection_handler
def searching_data(cursor,phrase):
    cursor.execute("""
                        SELECT DISTINCT question.* FROM answer
                        FULL JOIN question ON  answer.question_id = question.id
                        WHERE answer.message ILIKE %(phrase)s 
                            OR question.title ILIKE %(phrase)s
                            OR question.message ILIKE %(phrase)s;
                        """,
                   {"phrase": phrase})
    return cursor.fetchall()


@connection.connection_handler
def delete_answer_by_question_id(cursor, question_id):
    cursor.execute("""
                    DELETE FROM answer
                    WHERE question_id = %(question_id)s;
                    """, {"question_id": question_id})


@connection.connection_handler
def delete_answer_by_id(cursor, answer_id):
    cursor.execute("""
                    DELETE FROM answer
                    WHERE id = %(answer_id)s;
                    """, {"answer_id": answer_id})


@connection.connection_handler
def delete_question_by_quesion_id(cursor, question_id):
    cursor.execute("""
                    DELETE FROM question
                    WHERE id = %(question_id)s;
                    """, {"question_id": question_id})


@connection.connection_handler
def vote_up(cursor, question_id, answer_id=None):
    if answer_id is None:
        cursor.execute("""
                        UPDATE question set vote_number = vote_number +1
                        WHERE id = %(question_id)s;                    
                        """, {"question_id": question_id})
    else:
        cursor.execute("""
                        UPDATE answer set vote_number = vote_number +1
                        WHERE id = %(answer_id)s;                    
                        """, {"answer_id": answer_id})


@connection.connection_handler
def vote_down(cursor, question_id, answer_id=None):
    if answer_id is None:
        cursor.execute("""
                        UPDATE question set vote_number = vote_number -1
                        WHERE id = %(question_id)s;                    
                        """, {"question_id": question_id})
    else:
        cursor.execute("""
                        UPDATE answer set vote_number = vote_number -1
                        WHERE id = %(answer_id)s;                    
                        """, {"answer_id": answer_id})


@connection.connection_handler
def raise_view_number(cursor, question_id):
    cursor.execute("""
                    UPDATE question set view_number = view_number +1
                    WHERE id = %(question_id)s;
                    """, {"question_id": question_id})


@connection.connection_handler
def complement_new_comment_of_question(cursor, message, question_id, user_id):
    submission_time = get_submission_time()
    cursor.execute("""
                    INSERT INTO comment ("question_id", "answer_id" , "message" ,"submission_time", "edited_count", "user_id")
                    VALUES (%(question_id)s, %(none)s, %(message)s, %(submission_time)s, %(none)s, %(user_id)s); """,
                   {"question_id": question_id,  "submission_time": submission_time, "message": message, "none": None, "user_id": user_id })


@connection.connection_handler
def complement_new_comment_of_answer(cursor, message, answer_id, user_id):
    submission_time = get_submission_time()
    cursor.execute("""
                    INSERT INTO comment ("question_id", "answer_id" , "message" ,"submission_time", "edited_count", "user_id")
                    VALUES (%(none)s,%(answer_id)s, %(message)s, %(submission_time)s, %(none)s, %(user_id)s); """,
                   {"answer_id": answer_id, "submission_time": submission_time, "message": message, "none": None, "user_id":user_id })


@connection.connection_handler
def get_comment_data(cursor, question_id):
    cursor.execute("""
                    SELECT comment.id, comment.question_id, comment.answer_id, comment.message, comment.submission_time,
                    comment.edited_count, comment.user_id, users.username FROM comment
                    LEFT JOIN users ON comment.user_id = users.id
                    FULL JOIN answer ON comment.answer_id = answer.id
                    WHERE comment.question_id = %(question_id)s OR answer.question_id = %(question_id)s; """,
                   {"question_id": question_id})
    comments = cursor.fetchall()
    return comments


@connection.connection_handler
def delete_comment_by_quesion_id(cursor, question_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE question_id = %(question_id)s;
                    """, {"question_id": question_id})


@connection.connection_handler
def delete_answers_comments_by_question_id(cursor, question_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE answer_id IN (SELECT id FROM answer WHERE answer.question_id = %(question_id)s);
                    """, {"question_id": question_id})


@connection.connection_handler
def delete_comment_by_answer_id(cursor, answer_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE answer_id = %(answer_id)s; 
                    """, {"answer_id": answer_id})


@connection.connection_handler
def delete_comment_by_comment_id(cursor, comment_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE id = %(comment_id)s;
                    """, {"comment_id": comment_id})


@connection.connection_handler
def edit_existing_comment_data(cursor, new_message, comment_id):
    submission_time = get_submission_time()
    cursor.execute("""
                        UPDATE comment set message = %(new_message)s, submission_time = %(submission_time)s, edited_count = edited_count + 1
                        WHERE id = %(comment_id)s;
                        """,
                   {"new_message": new_message, "comment_id": comment_id, "submission_time": submission_time })


@connection.connection_handler
def get_comment_message_and_question_id(cursor, comment_id):
    cursor.execute("""
                    SELECT message, question_id FROM comment
                    WHERE id = %(comment_id)s;
                   """, {'comment_id': int(comment_id)})
    return cursor.fetchone()


@connection.connection_handler
def register_new_user(cursor, username, hashed_password, email):
    registration_time = get_submission_time()
    cursor.execute("""
                    INSERT INTO users (username, password, email, registration_time)
                    VALUES (%(username)s, %(hashed_password)s, %(email)s, %(registration_time)s)
                    """, {'username': username, 'hashed_password': hashed_password, 'email': email, 'registration_time':registration_time})


@connection.connection_handler
def get_users(cursor):
    cursor.execute("""
                    SELECT username FROM users
                    """)
    return cursor.fetchall()


@connection.connection_handler
def check_username_or_email(cursor,username,email):
    cursor.execute("""
                    SELECT * FROM users 
                    WHERE username = %(username)s OR email = %(email)s
                    """,{'username':username, 'email':email})
    return cursor.fetchall()


@connection.connection_handler
def user_login(cursor, username):
    cursor.execute("""SELECT password, id FROM users
                     WHERE username LIKE %(username)s;""",
                   {'username': username})
    return cursor.fetchone()


