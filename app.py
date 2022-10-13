from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.get('/')
def root_route():
  """
    render a page that shows the user the title of the survey, the instructions,
    and a button to start the survey
  """

  survey_title = survey.title
  survey_instructions = survey.instructions

  return render_template("survey_start.html", survey_title=survey_title, 
    survey_instructions=survey_instructions
  )

@app.post('/begin')
def begin():
  """ 
    redirect to the question
  """
  return redirect("/questions/0")


@app.get('/questions/<int:id>')
def get_question(id):
  """
    display the question
  """
  question = survey.questions[id]

  return render_template("question.html", question=question)

@app.post("/answer")
def get_answer():
  """
    handles the answer
  """
  answer = request.form["answer"]

  # append to responses

  responses.append(answer)

