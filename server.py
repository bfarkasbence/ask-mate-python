from flask import Flask, render_template, request, redirect, url_for, flash, session
import data_manager
import bcrypt

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/list")
def route_sorted_list_of_questions():
    criteria = request.args.get('criteria', 'submission_time')
    direction = request.args.get('direction', 'DESC')
    questions = data_manager.get_questions(criteria, direction, None)
    return render_template("list.html", list_of_questions=questions)


@app.route('/')
def route_list_of_latest_questions():
    questions = data_manager.get_questions('submission_time', 'DESC', 5)
    print(session.get('logged_in'))
    if not session.get('logged_in'):
        return render_template('login.html')
    return render_template("home.html", list_of_questions=questions)


@app.route("/questions/<question_id>")
def route_question(question_id):
    question_data = data_manager.get_question_data_by_id(question_id)
    answers_data = data_manager.get_list_of_answers(question_id)
    comment_data = data_manager.get_comment_data(question_id)
    return render_template("question.html", question_data=question_data, answers_data=answers_data,
                           question_id=question_id, comment_data=comment_data)


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
        data_manager.delete_answers_comments_by_question_id(question_id)
        data_manager.delete_answer_by_question_id(question_id)
        data_manager.delete_comment_by_quesion_id(question_id)
        data_manager.delete_question_by_quesion_id(question_id)
        return redirect('/list')
    return render_template("delete-question.html", question_id=question_id)


@app.route("/answer/<question_id>/<answer_id>/delete")
def delete_answer(question_id, answer_id):
    delete_answer_confirm = request.args.get('confirm', False)
    if delete_answer_confirm == "True":
        data_manager.delete_comment_by_answer_id(answer_id)
        data_manager.delete_answer_by_id(answer_id)
        return redirect(url_for("route_question", question_id=question_id))
    return render_template("delete-answer.html", question_id=question_id, answer_id=answer_id)


@app.route("/answer/<answer_id>/edit", methods=['GET'])
def editing_answers(answer_id):
    answer = data_manager.get_answer_message_and_question_id(answer_id)
    return render_template("edit-answer.html", answer=answer, answer_id=answer_id)


@app.route("/answer/<answer_id>/edit", methods=['POST'])
def save_edited_answers(answer_id):
    answer = data_manager.get_answer_message_and_question_id(answer_id)
    question_id = answer["question_id"]
    data_manager.edit_existing_answer_data(request.form['message'], answer_id)
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/search")
def searching_data():
    search_phrase = "%" + request.args.get('search_box') + "%"
    searching = data_manager.searching_data(search_phrase)
    return render_template("search.html", searching=searching)


@app.route("/answer/<question_id>/<answer_id>/like")
def vote_up_answer(answer_id, question_id):
    data_manager.vote_up(question_id, answer_id)
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/answer/<question_id>/<answer_id>/dislike")
def vote_down_answer(question_id, answer_id):
    data_manager.vote_down(question_id, answer_id)
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/questions/<question_id>/like")
def vote_up_question(question_id):
    data_manager.vote_up(question_id)
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/questions/<question_id>/dislike")
def vote_down_question(question_id):
    data_manager.vote_down(question_id)
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/questions/<question_id>/view_number")
def raise_view_number(question_id):
    data_manager.raise_view_number(question_id)
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/question/<question_id>/new-comment", methods=['GET'])
def new_questions_comment(question_id):
    return render_template("add-comment.html", question_id=question_id)


@app.route("/question/<question_id>/new-comment", methods=['POST'])
def questions_comment(question_id):
    data_manager.complement_new_comment_of_question(request.form['message'], question_id)
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/answer/<question_id>/<answer_id>/new-comment", methods=['GET'])
def new_answers_comment(question_id, answer_id):
    return render_template("add-comment.html", question_id=question_id)


@app.route("/answer/<question_id>/<answer_id>/new-comment", methods=['POST'])
def answers_comment(question_id, answer_id):
    data_manager.complement_new_comment_of_answer(request.form['message'], answer_id)
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/comment/<question_id>/<comment_id>/delete")
def delete_comment_by_id(comment_id, question_id):
    delete_comment_confirm = request.args.get('confirm', False)
    if delete_comment_confirm == "True":
        data_manager.delete_comment_by_comment_id(comment_id)
        return redirect(url_for("route_question", question_id=question_id))
    return render_template("delete-comment.html", question_id=question_id, comment_id=comment_id)


@app.route("/comment/<question_id>/<comment_id>/edit", methods=['GET'])
def editing_comments(question_id, comment_id):
    comment = data_manager.get_comment_message_and_question_id(comment_id)
    return render_template("edit-comment.html", comment=comment, comment_id=comment_id, question_id=question_id)


@app.route("/comment/<question_id>/<comment_id>/edit", methods=['POST'])
def save_edited_comments(comment_id, question_id):
    data_manager.edit_existing_comment_data(request.form['message'], comment_id)
    return redirect(url_for("route_question", question_id=question_id))


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)



@app.route("/registration", methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        hashed_password = hash_password(request.form['password'])
        if check_username_or_mail_in_db(request.form['username'], request.form['password']):
            data_manager.register_new_user(request.form['username'], hashed_password, request.form['email'])
            return redirect(url_for('route_list_of_latest_questions'))
        else:
            flash("Username or email already in use...")
            return redirect(url_for('register',))


def check_username_or_mail_in_db(username, password):
    return len(data_manager.check_username_or_email(username, password)) == 0


@app.route("/user-list")
def route_users_list():
    users = data_manager.get_users()
    return render_template("users-list.html", users=users)


@app.route('/login', methods=["GET"])
def login():
    return render_template('login.html')


@app.route('/login', methods=["POST"])
def get_login():
    if verify_password(request.form["password"], data_manager.user_login(request.form["username"]).get('password')):
        session["username"] = request.form["username"]
        session['logged_in'] = True
        print(session)
    return redirect('/list')


@app.route('/logout',methods=["GET"])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
