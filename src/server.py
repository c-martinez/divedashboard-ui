from flask import Flask
from flask import render_template, redirect, url_for
from flask import request, Response, make_response

from functools import wraps

from crowdtruth.CrowdTruthAPI import CrowdTruthAPI
from data.triplestore.DIVERepository import DIVERepository

import simplejson

app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.debug = True


_repository = DIVERepository(app.config)
_crowdTruth = CrowdTruthAPI(app.config)

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
    user = getAuthenticatedUser(request)

    stats = _repository.getCollectionTestResults(collection)
    collections = _repository.getCollections(user)
    return render_template(
        'collection.html',
        stats=stats,
        collection=collection,
        collections=collections,
        loggedIn=isLoggedIn(request),
        user=user
    )

@app.route('/crowd-tasks')
@requires_auth
def tasks():
    collection = request.args.get('c', None)
    user = getAuthenticatedUser(request)
    page = request.args.get('p', 0)

    jobs = _crowdTruth.getJobsOfCollection(collection, page)
    collections = _repository.getCollections(user)
    return render_template(
        'crowd-tasks.html',
        jobs=jobs,
        collection=collection,
        collections=collections,
        loggedIn=isLoggedIn(request),
        user=user
    )

@app.route('/alignments')
@requires_auth
def alignments():
    collection = request.args.get('c', None)
    user = getAuthenticatedUser(request)

    collections = _repository.getCollections(user)
    return render_template(
        'alignments.html',
        collection=collection,
        collections=collections,
        loggedIn=isLoggedIn(request),
        user=user
    )


if __name__ == '__main__':
	app.run(port=app.config['API_PORT'], host=app.config['API_HOST'])