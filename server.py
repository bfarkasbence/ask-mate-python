from flask import Flask, render_template, request, redirect

app = Flask(__name__)

new_question_data = {}

import data_manager
import connection


@app.route('/')
@app.route("/list")
def route_list_of_questions():
    list_of_questions = data_manager.get_list_of_anything("title")
    list_of_ids = data_manager.get_list_of_anything("id")
    return render_template("list.html", list_of_questions=list_of_questions, list_of_ids=list_of_ids)


@app.route("/questions/<question_id>")
def route_questions_id(question_id):
    question_data = data_manager.get_question_data_by_ID(question_id)
    answers_data = data_manager.get_list_of_answers(question_id)
    return render_template("question.html", question_data=question_data,answers_data=answers_data)


@app.route("/add-question", methods=['GET', 'POST'])
def route_add_question():
    if request.method == 'POST':
        new_question_data['title'] = request.form['title']
        new_question_data['message'] = request.form['message']
        new_question_data['image'] = request.form['image']
        list_of_questions = data_manager.complement_new_question_data(connection.get_data_from_file('sample_data/question.csv'), new_question_data)
        connection.write_data_to_file('sample_data/question.csv', list_of_questions)
        return redirect('/')

    return render_template("add-question.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
