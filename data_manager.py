import connection

def get_list_of_questions():
    list_of_dic = connection.get_data_from_file_question("sample_data/question.csv")
    result= []
    for item in list_of_dic[1:]:
        result.append(item.get("title"))
    return result


def get_question_data_by_ID(Id):
    list_of_dic = connection.get_data_from_file_question("sample_data/question.csv")
    result = []
    for item in list_of_dic[1:]:
        if item["id"] == str(Id):
            for value in item.values():
                result.append(value)
    return result

def get_list_of_answers(question_id):
    list_of_dic = connection.get_data_from_file_answer("sample_data/answer.csv")
    result = []
    for item in list_of_dic[1:]:
        if question_id == item['question_id']:
            result.append(item)
    return result


print(get_list_of_answers("0"))
