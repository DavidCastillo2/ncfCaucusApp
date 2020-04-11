"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

###########################################################################################################################################
#                                                                                                                                         #
#                                                           App Setup                                                                     #
#                                                                                                                                         #
###########################################################################################################################################
import sqlite3
import click
from flask import Flask, url_for, render_template, g

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

# jinja2 setup
import jinja2 as ninja
import os
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja2_env = ninja.Environment(loader=ninja.FileSystemLoader(template_dir))

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

# SQLite database setup
app.config.from_mapping(
    SECRET_KEY="dev",
    DATABASE=os.path.join(app.instance_path, "myData.sqlite"),
)
from db import init_app, get_db
init_app(app)

# Local Files/Dependancies
from classFile import *
import random as rand

###########################################################################################################################################
#                                                                                                                                         #
#                                                        Objects inserted into HTML                                                       #
#                                                                                                                                         #
###########################################################################################################################################

Candidates = []
for i in range(1, 8):
    imageURL = "people/person" + str(i)
    tempPerson = Candidate(("Dave"+ str(i)), i+80, imageURL)

###########################################################################################################################################
#                                                                                                                                         #
#                                                           Flask Routing                                                                 #
#                                                                                                                                         #
###########################################################################################################################################
from flask import Flask, redirect, request, g

@app.route('/')
def home():
    """Renders a Home page."""
    pageObject = render_template('home.html')

    return pageObject


# Since we have to use a full webpage to execute this python script, the user can do webpage/background_process_test to run this webpage
@app.route('/background_process_test')
def background_process_test():
    return ('nothing')


@app.route('/Candidates')
def Candidates():
    global Candidates
    Candidates = []
    for i in range(1, 8):
        imageURL = url_for('static', filename=('people/person' + str(i)) + ".jpg")
        tempPerson = Candidate(("Dave"+ str(i)), rand.randint(0,100), imageURL)
        tempPerson.id = i-1
        Candidates.append(tempPerson)
    return render_template('Candidates.html', Candidates=Candidates, title="Candidates List")


@app.route('/Candidates/<candidate>')
def viewCandidate(candidate):
    global Candidates
    for i in range(0, len(Candidates)):
        if (Candidates[i].name == candidate):
            can = Candidates[i]
            break
        else:
            can = Candidates[i]
    return render_template('Candidates.html', Candidates=can, title = can.name)


@app.route('/startCount')
def StartCount():
    global Candidates
    Candidates = []
    for i in range(1, 8):
        imageURL = url_for('static', filename=('people/person' + str(i)) + ".jpg")
        tempPerson = Candidate(("Dave"+ str(i)), rand.randint(0,100), imageURL)
        tempPerson.id = i-1
        Candidates.append(tempPerson)
    return render_template('chooseCandidate.html', Candidates=Candidates, title = "Select Your Candidate")

@app.route('/Count/<candidate>')
def count(candidate):
    for i in range(0, len(Candidates)):
        if (Candidates[i].name == candidate):
            can = Candidates[i]
            break
        else:
            can = Candidates[i]
    return render_template('count.html', Candidates=can, title = can.name)

@app.route('/wireframe', methods=("GET", "POST"))
def wireframe():
    if request.method == "POST":
        name = request.form["name"]
        bio = request.form["bio"]
        issues = request.form["issues"]
        error = None

        if not name:
            error = "Missing Information"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute (
                "INSERT INTO candidates (name, bio, issues) VALUES (?, ?, ?)", (name, bio, issues),    
            )
            db.commit()
            db.commit()
            return redirect(url_for('wireframe'))

    global Candidates
    Candidates = []
    for i in range(1, 8):
        imageURL = url_for('static', filename=('people/person' + str(i)) + ".jpg")
        tempPerson = Candidate(("Dave"+ str(i)), rand.randint(0,100), imageURL)
        tempPerson.id = i-1
        Candidates.append(tempPerson)
    return render_template('wireframe.html', Candidates=Candidates)

@app.route('/addie', methods=("GET","POST"))
def addie():
    if request.method == "POST":
        name = request.form["cName"]
        bio = request.form["cInfo"]
        image = request.form["cImage"]
        error = None

        if not name:
            error = "Missing Information"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute (
                "INSERT INTO addie (name, bio, img) VALUES (?, ?, ?)", (name, bio, image),    
            )
            db.commit()
            db.commit()
            return redirect(url_for('addie'))
    return render_template('addie.html')

###########################################################################################################################################
#                                                                                                                                         #
#                                                           Create Flask Host                                                             #
#                                                                                                                                         #
###########################################################################################################################################

if __name__ == '__main__':
    app.run(debug=True)
    '''
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
    '''