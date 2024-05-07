from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


RESPONSES_KEY = "responses"


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def show_survey_start():
    return render_template("survey_start.html", survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")


@app.route("/answer", methods=["POST"])
def handle_question():
    # response choice
    choice = request.form['answer']

    # add response to session
    responses = session[RESPONSES_KEY]
    responses.append (choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        # thanks for answer all questions
        return redirect("/complete")
    
    else: 
        return redirect(f"/questions/{len(responses)}")
    

@app.route("/questions/<int:qid>")
def show_question(qid):
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # acess questions page too soon
        return redirect("/")
    
    if(len(responses) == len(survey.questions)):
        # All questions answered 
        return redirect("/complete")
    
    if(len(responses) != qid):
        # Questions out if order
        flash(f"Invalid question id: {qid}.")
        return redirect (f"/questions/{len(responses)}")
    



    @app.route("/complete")
    def complete():
        return render_template("completion.html")
