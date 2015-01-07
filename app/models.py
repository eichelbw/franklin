from hashlib import md5
from app import db
import app.queries.evernquery as evernquery
from bs4 import BeautifulSoup

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def is_authenticated(self):
        """returns false if user is not allowed to authenticate"""
        return True # pass for now

    def is_active(self):
        """returns false if user has been banned (for example)"""
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        """returns unique id generated by db layer for user"""
        return unicode(self.id) # python 2

    def avatar(self, size):
        """grabs the user's gravatar"""
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

    def get_todo_content(self):
        """call queries/evernquery.get_todo_notes. return a list of all divs
        that contain en-todo tags along with their 'checked' status. seperate
        text not associated with en-todo tags and pass that along as well."""
        query_response = evernquery.get_todo_notes()
        out_divs = dict()
        for note in query_response:
            out_divs[str(note.title)] = self.munge_note(note)
        return out_divs

    def munge_note(self, note):
        """takes a note and return a list of all divs that contain en-todo tags
        along w their 'checked' status. separate text not associated w en-todo
        tags and pass that as long as well."""
        soup = BeautifulSoup(note.content)
        todo_title = note.title
        all_divs = soup.findAll("div")
        relevant_divs = []
        for div in all_divs:
            self.div_decision_tree(div, relevant_divs)
        return relevant_divs

    def div_decision_tree(self, div, relevant_divs):
        """formats div with info based on id as it comes from EN. returns
        div formatted for to pass to franklin front end."""
        if div.contents[0].name == "en-todo":
            div['id'] = 'tdcontent'
            try:
                if div.contents[0]['checked'] == 'true':
                    div.contents[0]['checked'] = 'checked' # change "checked" attr to jquery-compatible
            except KeyError: # en-todo is not checked. pass on to jquery as is
                pass
            relevant_divs.append([div, 'checked' in div.contents[0].attrs])
        else:
            div['id'] = 'tdheader'
            relevant_divs.append([div, "something's wrong if this gets touched"])
        return relevant_divs

    def __repr__(self):
        """how to print items from the db. used for debugging"""
        return "<User %r>" % (self.id)

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
#     def __repr__(self):
#         return '<Post %r>' % (self.body)
