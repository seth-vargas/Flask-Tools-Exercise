from flask import Flask, request, render_template, flash, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "2001"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False # makes it so that the debugger will automatically redirect the user to the proper page

debug = DebugToolbarExtension(app)

responses = [] # As people answer questions, you should store answers in this list. 
"""
NOTE
responses does not reset until the server stops. You may need to stop the server if you run into any bugs, as the legnth of this list tells the app to end once it exceeds the length of avaliable questions.
"""

@app.route('/')
def show_survey():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template("index.html", title=title, instructions=instructions)


@app.route('/questions/<int:question_number>')
def show_question(question_number):
    current_question = satisfaction_survey.questions[question_number].question
    choices = [c for c in satisfaction_survey.questions[question_number].choices]

    if question_number > len(responses):
        flash("Invalid number entered in URL")
        return redirect(f'/questions/{len(responses)}')

    if len(satisfaction_survey.questions) == len(responses):
        return redirect('/complete')

    return render_template("questions.html", question=current_question, number=question_number, choices=choices)


@app.route('/answer', methods=["POST"])
def store_answers():
    # append to responses list
    ans = request.form['choices']
    responses.append(ans)
    next_question = len(responses)
    # survey is over, thank the user
    if next_question == len(satisfaction_survey.questions):
        return redirect("/complete")
    # redirect them to the next question
    return redirect(f'/questions/{next_question}')


@app.route('/complete')
def thank_user():
    return render_template("thanks.html")