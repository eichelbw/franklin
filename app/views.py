from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
import json
from app import app, db, lm, oid
import app.queries.evernquery as evernquery
from bs4 import BeautifulSoup
from forms import LoginForm
from models import User
from datetime import datetime
from helpers import view

@app.route('/')
@app.route('/index')
@login_required
def index():
    """index route"""
    user = g.user
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
            title = 'Home',
            user=user,
            posts=posts)

@app.route('/login', methods=['GET','POST'])
@oid.loginhandler
def login():
    """login!"""
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
            title='Sign In',
            form=form,
            providers=app.config['OPENID_PROVIDERS'])

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    """returns profile page for user"""
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    posts = [
            {'author': user, 'body': 'Test post 1'},
            {'author': user, 'body': 'Test post 2'}
            ]
    return render_template('user.html',
            user=user,
            posts=posts)

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
        db.session.add(g.user)
        db.session.commit()

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
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

