import connection
import time


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
    cursor.execute("""
                    INSERT INTO question ("title", "message", "image")
                    VALUES (%(title)s, %(message)s, %(image)s); """,
                   {"title": title, "message": message, "image": image})


def complement_new_answer_data(data_from_file, basic_data, question_id):
    new_data = {"id": get_number_of_all_questions("sample_data/answer_number.csv"), "submission_time": time.time(),
                "vote_number": '0', "question_id": question_id, "message": basic_data['message'],
                "image": basic_data['image']}
    data_to_file = []
    data_to_file.append(new_data)
    data_to_file = data_to_file + data_from_file[1:]
    return data_to_file


def save_answer(new_answer_data, question_id):
    list_of_questions = complement_new_answer_data(
        connection.get_data_from_file('sample_data/answer.csv'), new_answer_data,question_id)
    connection.write_data_to_file('sample_data/answer.csv', list_of_questions)
