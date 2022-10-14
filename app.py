from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# up to step five
#responses = []


@app.get('/')
def root_route():
    """
      render a page that shows the user the title of the survey, the instructions,
      and a button to start the survey
    """

    session["responses"] = []
    session["questions_answered"] = []
    survey_title = survey.title
    survey_instructions = survey.instructions

    return render_template(
        "survey_start.html",
        survey_title=survey_title,
        survey_instructions=survey_instructions
    )

# start button. shows up in network tab


@app.post('/begin')
def begin():
    """ 
      redirect to the question
    """
    return redirect("/questions/0")


@app.get('/questions/<int:id>')
def get_question(id):
    """
      displays the question
    """

    """ protecting questions """
    answered = session["questions_answered"]
    print(answered, "answered here")
    """ if truthy and if last index of answered is not equal to the current id"""
    if answered and answered[-1] != id-1:
        flash("Woah buddy. Calm down")
        return redirect(f"/questions/{answered[-1]+1}")

    if id >= len(survey.questions):
        responses = session["responses"]
        """ Creating tuples with question and answers """
        results = [(survey.questions[i].question, responses[i])
                   for i in range(0, len(survey.questions))
                   ]
        return render_template("completion.html", results=results)

    question = survey.questions[id]

    return render_template("question.html", question=question, id=id)


@app.post("/answer")
def get_answer():
    """
      handles the answer
    """
    answer = request.form["answer"]
    id = int(request.form["id"])

    # append to responses (old code up to step five)
    # responses.append(answer)
    responses = session["responses"]
    #print(responses, "response 72")
    responses.append(answer)
    session["responses"] = responses
    #print(session["responses"], "session is 75")

    answered = session["questions_answered"]
    answered.append(id)
    session["questions_answered"] = answered

    next_url = f"/questions/{id + 1}"

    return redirect(next_url)
