import csv

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
