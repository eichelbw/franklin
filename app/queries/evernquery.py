from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
import evernote.edam.type.ttypes as Types
from evernote.edam.type.ttypes import NoteSortOrder

dev_token = "S=s385:U=3e7d2ff:E=150f8d4c12f:C=149a12394c0:P=1cd:A=en-devtoken:V=2:H=44734894e812cbfe03d83cc365d8c9c5"
client = EvernoteClient(token=dev_token, sandbox=False)
note_store = client.get_note_store() # Evernote's Note Store object is the access point to all note-related information
all_tags = note_store.listTags()
todo_guid = [tag for tag in all_tags if tag.name == "todo"][0].guid # compare all tags to "todo" and grab guid

note_filter = NoteFilter() # the notefilter object allows us to define filters for our eventual findNotesMetadata call
note_filter.tagGuids = [todo_guid] # find note with todo guid (ie, the todo note)
offset, max_notes = 0, 1
result_spec = NotesMetadataResultSpec(includeTitle=True) # allows us to request specific info be returned about the note

# TODO increase max_notes and display todos from the same note together. probably change get_todo_notes()
#      to return a dictionary with keys being note.title and values being en-todos

def get_todo_notes():
    """executes EN api query and returns content of note tagged 'todo'"""
    result_list = note_store.findNotesMetadata(dev_token, note_filter, offset, max_notes, result_spec)
    todo_note_guid = result_list.notes[0].guid
    return note_store.getNote(dev_token, str(todo_note_guid), True, False, False, False)

def set_todo_content(updated_note):
    """updates EN api with modifications to updated_note"""
    # updateNote() needs three things:
    # 1) todo note's guid
    # 2) todo note's title
    # 3) todo note's full content with change.
    # ---
    # things in the way currently:
    # 1) not sure if i should create an object in this method to pass to updateNote and assign attributes
    #    directly from the earlier note from get_todo_notes() or to update previous object in jquery and
    #    pass it back to flask.
    # for example, the following series of commands works in terminal:
    # tdn = evernquery.get_todo_notes()
    # upnote = Types.Note()
    # upnote.title, upnote.guid = tdn.title, tdn.guid
    # upnote.content = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">\n<en-note><div>Hello world!</div><div><br clear="none"/></div><div>it\'s different now! even more so!</div><div><br clear="none"/></div><div><en-todo checked="true"></en-todo>learn how to interact with todos</div><div><en-todo checked="true"></en-todo>second one for testing</div></en-note>'
    # note_store.updateNote(upnote)

###############
### TESTING ###
###############

#note = Types.Note()
#note.title = "test note"
#note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd"><en-note>Hello world!</en-note>'
#note = noteStore.createNote(note)

#userStore = client.get_user_store()
#user = userStore.getUser()
#print user.username

