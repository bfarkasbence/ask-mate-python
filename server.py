from flask import Flask, render_template

app = Flask(__name__)

import data_manager

@app.route('/')
@app.route("/list")
def list_of_questions():
    list_of_questions = data_manager.get_list_of_questions()
    return render_template("list.html",list_of_questions=list_of_questions)


@app.route("/questions/<question_id>")
def questions_id(question_id):
    question_data = data_manager.get_question_data_by_ID(question_id)
    answers_data = data_manager.get_list_of_answers(question_id)
    return render_template("question.html", question_data=question_data,answers_data=answers_data)

@app.route("/add-question")
def add_question():
    return render_template("add-question.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
