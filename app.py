from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.secret_key = 'SECRETTTSECRETTTS'
app.config["SECRET_KEY"] = "SECRET"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.route("/")
def index():
    '''Displays the survey title and instruction. After clicking form submit, redirects
    page to /session decorator'''
    title = 'PICK A SURVEY'
    instructions = 'CHOOSE THE SURVEY THAT BEST SUITS YOU'
    lst_of_surveys = surveys.surveys
    return render_template("index.html", title=title, instructions=instructions, surveys=lst_of_surveys)


@app.route('/session', methods=["POST"]) 
def session_creator(): 
    '''Initializes the session['responses'], holding our questions, and redirects
    to our first question'''
    session['responses'] = []
    session['chosen_title'] = request.form.get('survey_choice', 'satisfaction')
    print(session['chosen_title'])
    responses_length = len(session['responses'])
    return redirect(f'/question/{responses_length}')


@app.route("/question/<int:id>")
def question(id):
    '''Question page that shows each individual question, using the length of our current 
    session['responses'] length as our id'''
    responses_length = len(session['responses'])
    #ends our survey and also stops people from accessing questions higher than the limit
    print(surveys.surveys['satisfaction'].questions)
    if id >= len(surveys.surveys[session['chosen_title']].questions): 
        return redirect('/endpage')
    #if someone tinkers with our id, we make sure to spam them with a flash saying 'stop' and deny access
    if id != responses_length:
        flash("stop")
        return redirect(f'/question/{responses_length}')
    question = surveys.surveys[session['chosen_title']].questions[id].question
    choices = surveys.surveys[session['chosen_title']].questions[id].choices

    return render_template("question.html", question=question, choices=choices)


@app.route("/answer", methods=["POST"])
def answer():
    '''saves our answers in the session response and redirects us to the next question'''
    answer = request.form
    sesh = session['responses']
    sesh.append(answer["choice"])
    session['responses'] = sesh
    id = len(session['responses'])
    return redirect(f"/question/{id}")


@app.route('/endpage')
def endpage():
    '''our end-page'''
    return render_template("answer.html")



#When you finish survey and go back to index to start survey, the responses are not set back to empty
#When you finish survey and refresh and go back to index, responses refreshes