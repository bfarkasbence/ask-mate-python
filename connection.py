import csv

DATA_HEADER_QUESTION = ["id","submission_time","view_number","vote_number","title","message","image"]
DATA_HEADER_ANSWER = ["id","submission_time","vote_number","question_id","message","image"]


def get_data_from_file_question(filename):
    with open(filename,"r") as file:
        result = []
        stories = csv.DictReader(file,fieldnames=DATA_HEADER_QUESTION)
        for row in stories:
            result.append(dict(row))
        return result

def get_data_from_file_answer(filename):
    with open(filename,"r") as file:
        result = []
        stories = csv.DictReader(file,fieldnames=DATA_HEADER_ANSWER)

        for row in stories:
            result.append(dict(row))
        return result
