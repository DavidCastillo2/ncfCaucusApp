"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

###########################################################################################################################################
#                                                                                                                                         #
#                                                           Importing                                                                     #
#                                                                                                                                         #
###########################################################################################################################################

from flask import *
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
@app.route('/')
def home():
    """Renders a Home page."""
    pageObject = render_template('home.html')

    return pageObject


# Since we have to use a full webpage to execute this python script, the user can do webpage/background_process_test to run this webpage
@app.route('/background_process_test')
def background_process_test():
    print("\nsee, we called a method without change the webpage\n")
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

@app.route('/wireframe')
def wireframe():
    global Candidates
    Candidates = []
    for i in range(1, 8):
        imageURL = url_for('static', filename=('people/person' + str(i)) + ".jpg")
        tempPerson = Candidate(("Dave"+ str(i)), rand.randint(0,100), imageURL)
        tempPerson.id = i-1
        Candidates.append(tempPerson)
    return render_template('wireframe.html', Candidates=Candidates)

###########################################################################################################################################
#                                                                                                                                         #
#                                                           Create Flask Host                                                             #
#                                                                                                                                         #
###########################################################################################################################################

if __name__ == '__main__':
    # app.run(debug=True)
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
