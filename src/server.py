from flask import Flask
from flask import render_template, redirect, url_for
from flask import request, Response, make_response

from functools import wraps

from crowdtruth.CrowdTruthAPI import CrowdTruthAPI
from data.DIVERepository import DIVERepository

import simplejson

app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.debug = True


"""------------------------------------------------------------------------------
GLOBAL FUNCTIONS
------------------------------------------------------------------------------"""

def getErrorMessage(msg):
	return simplejson.dumps({'error' : msg})

def getSuccessMessage(msg, data):
	return simplejson.dumps({'success' : msg, 'data' : data})

"""------------------------------------------------------------------------------
AUTHENTICATION
------------------------------------------------------------------------------"""

def check_auth(username, password):
	return username == app.config['USER'] and password == app.config['PASSWORD']

def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def isLoggedIn(request):
	if request.authorization:
		return True
	return False

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def getAuthenticatedUser(request):
    if request.authorization:
        return request.authorization.username
    return None

"""------------------------------------------------------------------------------
REGULAR ROUTING (STATIC CONTENT)
------------------------------------------------------------------------------"""

@app.route('/')
def home():
	return render_template('index.html', loggedIn=isLoggedIn(request), user=getAuthenticatedUser(request))

@app.route('/about')
def about():
    return render_template('about.html', loggedIn=isLoggedIn(request), user=getAuthenticatedUser(request))

@app.route('/contact')
def contact():
    return render_template('contact.html', loggedIn=isLoggedIn(request), user=getAuthenticatedUser(request))

@app.route('/collection')
@requires_auth
def collections():
    collection = request.args.get('c', None)
    dr = DIVERepository(app.config)
    stats = dr.getCollectionStats(collection)
    return render_template(
        'collection.html',
        stats=stats,
        collection=collection,
        loggedIn=isLoggedIn(request),
        user=getAuthenticatedUser(request)
    )

@app.route('/crowd-tasks')
@requires_auth
def tasks():
    collection = request.args.get('c', None)
    page = request.args.get('p', 0)
    api = CrowdTruthAPI(app.config)
    jobs = api.getJobsOfCollection(collection, page)
    return render_template(
        'crowd-tasks.html',
        jobs=jobs,
        collection=collection,
        loggedIn=isLoggedIn(request),
        user=getAuthenticatedUser(request)
    )

@app.route('/alignments')
@requires_auth
def alignments():
    collection = request.args.get('c', None)
    return render_template(
        'alignments.html',
        collection=collection,
        loggedIn=isLoggedIn(request),
        user=getAuthenticatedUser(request))


if __name__ == '__main__':
	app.run(port=app.config['API_PORT'], host=app.config['API_HOST'])