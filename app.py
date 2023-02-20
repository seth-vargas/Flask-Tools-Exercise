from flask import Flask, request, render_template, flash, redirect, jsonify
from flask import session
from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "2001"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False # makes it so that the debugger will automatically redirect the user to the proper page

debug = DebugToolbarExtension(app)

# responses = [] # As people answer questions, you should store answers in this list. 
"""
NOTE
responses does not reset until the server stops. You may need to stop the server if you run into any bugs, as the legnth of this list tells the app to end once it exceeds the length of avaliable questions.
"""

@app.route('/')
def show_survey():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template("index.html", title=title, instructions=instructions)


@app.route('/start-test', methods=["POST"])
def start_test():
    # cannot submit multiple forms
    if not session.get('responses'): # treat like a dictionary, use .get instead of obj[key] notation
        session['responses'] = []
        return redirect('questions/0')
    flash("You have already completed the test, thank you!")
    return redirect('/complete')


@app.route('/questions/<int:question_number>')
def show_question(question_number):
    current_question = satisfaction_survey.questions[question_number].question
    choices = satisfaction_survey.questions[question_number].choices

    if question_number > len(session['responses']):
        flash("Invalid number entered in URL")
        return redirect(f"/questions/{len(session['responses'])}")

    if len(satisfaction_survey.questions) == len(session['responses']):
        return redirect('/complete')

    return render_template("questions.html", question=current_question, number=question_number, choices=choices)


@app.route('/answer', methods=["POST"])
def store_answers():
    # append to responses list
    ans = request.form['choices']

    answers_list = session['responses']
    answers_list.append(ans)
    session['responses'] = answers_list

    # survey is over, thank the user
    if len(session['responses']) == len(satisfaction_survey.questions):
        return redirect("/complete")
    # redirect them to the next question
    next_question = len(session['responses'])
    return redirect(f'/questions/{next_question}')


@app.route('/complete')
def thank_user():
    return render_template("thanks.html")