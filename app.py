from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

responses = []

@app.route("/")
def index():
    title = surveys.satisfaction_survey.title
    instructions = surveys.satisfaction_survey.instructions
    return render_template("index.html", title=title, instructions=instructions)

@app.route("/question/<int:id>")
def question(id):

    if id >= len(surveys.satisfaction_survey.questions):
        return redirect("/sucker")
    if id != len(responses):
        flash("stop")
        return redirect(f'/question/{len(responses)}')
    print(f"THE ID IS: {id}")
    question = surveys.satisfaction_survey.questions[id].question
    choices = surveys.satisfaction_survey.questions[id].choices
    
    return render_template("question.html", question=question, choices=choices, id=id)

@app.route("/answer", methods=["POST"])
def answer():
    answer = request.form
    id = int(request.form["id"]) + 1
    responses.append(answer["choice"])
    print(responses)

    return redirect(f"/question/{id}")


@app.route("/sucker")
def sucker():
    return render_template("answer.html")



#When you finish survey and go back to index to start survey, the responses are not set back to empty
#When you finish survey and refresh and go back to index, responses refreshes