from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY']="secret"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

responses = []

@app.route("/")
def home_page():
    title = survey.title
    instructions = survey.instructions
    return render_template("home_page.html", title=title, instructions=instructions)

@app.route("/begin", methods=["POST"])
def begin_survey():
    session["responses"] = []
    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def answer_handler():
    response = request.form['response']

    responses = session["responses"]
    responses.append(response)
    session["responses"] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/completed")

    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/questions/<int:id>")
def question_series(id):
    responses = session.get("responses")

    if (responses is None):
        return redirect("/")
    
    if (len(responses) == len(survey.questions)):
        return redirect("/completed")

    if (len(responses) != id):
        flash(f"Invalid question id: {id}.")
        return redirect(f"/questions/{len(responses)}")

    questions = survey.questions[id]
    return render_template("questions.html", responses=responses, question_num=id, question=questions)

@app.route("/completed")
def completed():
    return render_template("completed.html")