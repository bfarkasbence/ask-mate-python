from flask import Flask, render_template, request, redirect, url_for
import data_manager
import connection

app = Flask(__name__)


@app.route('/')
@app.route("/list")
def route_list_of_questions():
    questions = data_manager.get_questions()
    return render_template("list.html", list_of_questions=questions)


@app.route("/questions/<question_id>")
def route_question(question_id):
    question_data = data_manager.get_question_data_by_id(question_id)
    answers_data = data_manager.get_list_of_answers(question_id)
    return render_template("question.html", question_data=question_data, answers_data=answers_data,
                           question_id=question_id)


@app.route("/add-question", methods=['GET'])
def route_add_question_form():
    return render_template("add-question.html")


@app.route("/add-question", methods=['POST'])
def route_add_question():
    data_manager.complement_new_question_data(request.form['title'], request.form['message'], request.form['image'])
    return redirect('/')


@app.route("/questions/<question_id>/new-answer", methods=['GET', 'POST'])
def route_add_answer(question_id):
    new_answer_data = {}
    if request.method == 'POST':
        new_answer_data['message'] = request.form['message']
        new_answer_data['image'] = request.form['image']
        data_manager.save_answer(new_answer_data, question_id)

        return redirect(url_for("route_question", question_id=question_id))
    return render_template("add-answer.html", question_id=question_id)


@app.route("/questions/<question_id>/delete", methods=['GET', 'POST'])
def delete_question(question_id):
    if request.method == 'POST':
        delete_question = request.form['delete_question']

    return render_template("delete-question.html", question_id=question_id)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
