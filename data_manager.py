import csv

DATA_HEADER = ["id","submission_time","view_number","vote_number","title","message","image"]


def get_data_from_file(filename):
    with open(filename,"r") as file:
        result = []
        stories = csv.DictReader(file,fieldnames=DATA_HEADER)
        for row in stories:
            result.append(dict(row))
        return result

print(get_data_from_file("sample_data/question.csv"))