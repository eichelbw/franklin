from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
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
    #todo_content = note_store.getNote(dev_token, str(todo_note_guid), True, False, False, False).content
    return note_store.getNote(dev_token, str(todo_note_guid), True, False, False, False)

def set_todo_content(updated_note):
    """updates EN api with modifications to updated_note"""
    note_store.updateNote(updated_note)

#note = Types.Note()
#note.title = "test note"
#note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd"><en-note>Hello world!</en-note>'
#note = noteStore.createNote(note)

#userStore = client.get_user_store()
#user = userStore.getUser()
#print user.username

