from flask import Flask, render_template

app = Flask(__name__)

import data_manager

@app.route('/')
@app.route("/list")
def list_of_questions():
    list_of_questions = data_manager.get_data_from_file("sample_data/question.csv")
    return render_template("list.html",list_of_questions=list_of_questions)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
