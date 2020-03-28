"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

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


@app.route('/')
def hello():
    """Renders a Home page."""
    pageObject = render_template('home.html')

    return pageObject


# Since we have to use a full webpage to execute this python script, the user can do webpage/background_process_test to run this webpage
@app.route('/background_process_test')
def background_process_test():
    print("\nsee, we called a method without change the webpage\n")
    return ('nothing')


@app.route('/newPage')
def newPage():
    return render_template('newPage.html')


# Main Run Code
if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
