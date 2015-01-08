import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'this-is-super-secret-u-guys-69+420'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True
GOOGLE_OPENID = [
        {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
        ]

EN_CONSUMER_KEY = 'wceichelb-6766'
EN_CONSUMER_SECRET = '381adfd541c539c7'

EN_REQUEST_TOKEN_URL = 'https://sandbox.evernote.com/oauth'
EN_ACCESS_TOKEN_URL = 'https://sandbox.evernote.com/oauth'
EN_AUTHORIZE_URL = 'https://sandbox.evernote.com/OAuth.action'

EN_HOST = "sandbox.evernote.com"
EN_USERSTORE_URIBASE = "https://" + EN_HOST + "/edam/user"
EN_NOTESTORE_URIBASE = "https://" + EN_HOST + "/edam/note/"
