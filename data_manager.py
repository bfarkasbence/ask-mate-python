import connection
import time

def get_list_of_questions():
    list_of_dic = connection.get_data_from_file("sample_data/question.csv")
    result= []
    for item in list_of_dic[1:]:
        result.append(item.get("title"))
    return result


def get_question_data_by_ID(Id):
    list_of_dic = connection.get_data_from_file("sample_data/question.csv")
    result = []
    for item in list_of_dic[1:]:
        if item["id"] == str(Id):
            for value in item.values():
                result.append(value)
    return result


def get_list_of_answers(question_id):
    list_of_dic = connection.get_data_from_file("sample_data/answer.csv")
    result = []
    for item in list_of_dic[1:]:
        if question_id == item['question_id']:
            result.append(item)
    return result


def get_number_of_all_questions():
    number = connection.get_data_from_file("sample_data/number.csv")
    number[1]['number'] = int(number[1]['number']) + 1
    connection.write_data_to_file("sample_data/number.csv", number[1:])
    return number[1]["number"]


def complement_new_question_data(data_from_file, basic_data):
    new_data = {"id": get_number_of_all_questions(), "submission_time": time.time(), "view_number": '0', "vote_number": '0', "title": basic_data['title'], "message": basic_data['message'], "image": basic_data['image']}
    data_to_file = []
    data_to_file.append(new_data)
    data_to_file = data_to_file + data_from_file[1:]
    return data_to_file

