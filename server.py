from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)


@app.route("/list")
def route_sorted_list_of_questions():
    criteria = request.args.get('criteria', 'submission_time')
    direction = request.args.get('direction', 'DESC')
    questions = data_manager.get_questions(criteria, direction, None)
    return render_template("list.html", list_of_questions=questions)


@app.route('/')
def route_list_of_latest_questions():
    questions = data_manager.get_questions('submission_time', 'DESC', 5)
    return render_template("home.html", list_of_questions=questions)


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
    return redirect('/list')


@app.route("/questions/<question_id>/new-answer", methods=['GET'])
def route_add_answer_form(question_id):
    return render_template("add-answer.html", question_id=question_id)


@app.route("/questions/<question_id>/new-answer", methods=['POST'])
def route_add_answer(question_id):
    data_manager.complement_new_answer_data(request.form['message'], request.form['image'], question_id)
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/questions/<question_id>/delete")
def delete_question(question_id):
    delete_question_confirm = request.args.get('confirm', False)
    if delete_question_confirm == "True":
        data_manager.delete_answer_by_question_id(question_id)
        data_manager.delete_question_by_quesion_id(question_id)
        return redirect('/list')
    return render_template("delete-question.html", question_id=question_id)


@app.route("/answer/<answer_id>/edit", methods=['GET', 'POST'])
def editing_answers(answer_id):
    answer = data_manager.get_answer_message_and_question_id(answer_id)
    question_id = answer["question_id"]
    if request.method=='POST':
        data_manager.edit_existing_answer_data(request.form['message'], answer_id)
        return render_template('/question/<question_id>.html', question_id=question_id)
    return render_template("edit-answer.html",answer=answer,answer_id=answer_id)


@app.route("/search")
def searching_data():
    search_phrase = "%" + request.args.get('search_box') + "%"
    searching = data_manager.searching_data(search_phrase)
    return render_template("search.html", searching=searching)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
