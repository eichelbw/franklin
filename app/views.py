import urlparse
import urllib

from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
import json
from app import app, oid, lm
from .forms import LoginForm
import app.queries.evernquery as evernquery
import app.queries.enauth as enauth
import config
from bs4 import BeautifulSoup
import oauth2 as oauth
from models import User
from datetime import datetime
from helpers import view

@app.route('/')
@app.route('/index')
def index():
    """index route"""
    user = g.user
    # posts = [  # fake array of posts
    #     {
    #         'author': {'nickname': 'John'},
    #         'body': 'Beautiful day in Portland!'
    #     },
    #     {
    #         'author': {'nickname': 'Susan'},
    #         'body': 'The Avengers movie was so cool!'
    #     }
    # ]
    return render_template('index.html',
            title = 'Home',
            )

@app.route('/login', methods=['GET','POST'])
@oid.loginhandler
def login():
    """login!"""
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['email'])
    return render_template('login.html',
            title='Sign In',
            form=form,
            providers=app.config['GOOGLE_OPENID'])

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# @app.route('/user/<nickname>')
# @login_required
# def user(nickname):
#     """returns profile page for user"""
#     user = User.query.filter_by(nickname=nickname).first()
#     if user == None:
#         flash('User %s not found.' % nickname)
#         return redirect(url_for('index'))
#     posts = [
#             {'author': user, 'body': 'Test post 1'},
#             {'author': user, 'body': 'Test post 2'}
#             ]
#     return render_template('user.html',
#             user=user,
#             posts=posts)

# this and the following method lifted unflinchingly from
# https://github.com/dasevilla/evernote-oauth-example
@app.route('/auth')
@login_required
def auth_start():
    """Makes a request to Evernote for the request token then redirects the
    user to Evernote to authorize the application using the request token.

    After authorizing, the user will be redirected back to auth_finish()."""

    client = enauth.get_oauth_client()

    # Make the request for the temporary credentials (Request Token)
    callback_url = 'http://%s%s' % ('127.0.0.1:5000', url_for('auth_finish'))
    request_url = '%s?oauth_callback=%s' % (config.EN_REQUEST_TOKEN_URL,
        urllib.quote(callback_url))

    resp, content = client.request(request_url, 'GET')

    if resp['status'] != '200':
        raise Exception('Invalid response %s.' % resp['status'])

    request_token = dict(urlparse.parse_qsl(content))

    # Save the request token information for later
    session['oauth_token'] = request_token['oauth_token']
    session['oauth_token_secret'] = request_token['oauth_token_secret']

    # Redirect the user to the Evernote authorization URL
    return redirect('%s?oauth_token=%s' % (config.EN_AUTHORIZE_URL,
        urllib.quote(session['oauth_token'])))


@app.route('/authComplete')
@login_required
def auth_finish():
    """After the user has authorized this application on Evernote's website,
    they will be redirected back to this URL to finish the process."""

    oauth_verifier = request.args.get('oauth_verifier', '')

    token = oauth.Token(session['oauth_token'], session['oauth_token_secret'])
    token.set_verifier(oauth_verifier)

    client = enauth.get_oauth_client()
    client = enauth.get_oauth_client(token)

    # Retrieve the token credentials (Access Token) from Evernote
    resp, content = client.request(config.EN_ACCESS_TOKEN_URL, 'POST')

    if resp['status'] == '401':
        flash("Sorry, looks like you declined authorization :(")
        return redirect(url_for('index'))
    elif resp['status'] != '200':
        raise Exception('Invalid response %s.' % resp['status'])

    access_token = dict(urlparse.parse_qsl(content))
    authToken = access_token['oauth_token']

    userStore = enauth.get_userstore()
    user = userStore.getUser(authToken)

    # Save the users information to so we can make requests later
    session['shardId'] = user.shardId
    session['identifier'] = authToken

    # print "%s - authenticated user. got authToken: %s and shardId: %s" % \
    #         (datetime.now, authToken, user.shardId)
    print type(user)

    flash('Successfully logged in!')
    return redirect(url_for('todos'))

@app.route('/todos')
def todos():
    user = g.user
    return render_template('todos.html',
            title="TODO",
            user=user
            )

@app.route('/sync', methods=['POST'])
def sync():
    """gets the request from the front end, does a bunch of housekeeping,
    and then sends a list with each update along to the EN interface"""
    req = BeautifulSoup(request.get_data().decode("string-escape"))
    updates = []
    for tag in req:
        if tag.name == "h1":
            update_batch = list(view.split_request(tag)) # look in view helper
            updates.append(view.format_divs_for_EN(update_batch))
    evernquery.post_todo_updates(updates)
    return jsonify(result={"status": 200})

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        # db.session.add(g.user)
        # db.session.commit()

@lm.user_loader
def load_user(id):
    """loads a user from the db by id"""
    return User.query.get(int(id))

@oid.after_login
def after_login(resp):
    """handles what to do once a user hits the login button"""
    if resp.email is None or resp.email == "":
        flash("Invalid login. Please try again.")
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        user = User(email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))
