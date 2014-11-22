from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
import json
from app import app, db, lm, oid
import app.queries.evernquery as evernquery
from bs4 import BeautifulSoup
from forms import LoginForm
from models import User
from datetime import datetime

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
    """finds all en-todos on the page"""
    req = BeautifulSoup(request.get_data().decode("string-escape"))
    all_divs = req.findAll("div")
    update_divs = []
    for div in all_divs:
        if div['id'] == 'tdcontent':
            del(div['id'])
            for child in div.children:
                try:
                    if child["checked"] == "checked":
                        child["checked"] = "true"
                except:
                    pass
            update_divs.append(div)
        elif div['id'] == "tdheader":
            del(div['id'])
            update_divs.append(div)
        elif div['id'] == 'nav' or div['id'] == 'tdholder':
            pass
        else:
            print "something's gone wrong in the sync route"
    updates = unicode.join(u'\n', map(unicode, update_divs))
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

