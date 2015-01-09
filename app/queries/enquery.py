from flask import session
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
import evernote.edam.type.ttypes as Types
from evernote.edam.type.ttypes import NoteSortOrder
import app.queries.enauth as enauth

def get_todo_note_guids(session):
    # Evernote's Note Store object is the access point to all note-related
    # information
    auth_token = session['identifier']
    print auth_token

    note_store = enauth.get_notestore(session)

    all_tags = note_store.listTags(auth_token) # get the todo tag guid
    todo_guid = [tag for tag in all_tags if tag.name == "todo"][0].guid

    note_filter = NoteFilter() # the notefilter object allows us to define filters for our eventual findNotesMetadata call
    note_filter.tagGuids = [todo_guid] # find note with todo guid (ie, the todo note)
    offset, max_notes = 0, 10
    result_spec = NotesMetadataResultSpec(includeTitle=True) # allows us to request specific info be returned about the note
    result_list = note_store.findNotesMetadata(auth_token, note_filter, offset, max_notes, result_spec)
    return note_store, [note.guid for note in result_list.notes]


def get_todo_notes(session):
    """executes EN api query and returns content of note tagged 'todo'"""
    out_notes = []
    note_store, guids = get_todo_note_guids(session)
    for guid in guids:
        out_notes.append(note_store.getNote(session['identifier'], str(guid), True, False, False, False))
    return note_store, out_notes

def post_todo_updates(updates):
    """updates EN api with modifications to the notes"""
    HEADER = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">\n<en-note>'
    TAIL = '</en-note>'
    note_store, notes = get_todo_notes(session)
    for index, tdn in enumerate(notes): # use get_todo_notes bc it's a handy way to get guid and title. probs slow.
        upnote = Types.Note()
        upnote.title, upnote.guid = tdn.title, tdn.guid
        upnote.content = HEADER + updates[index] + TAIL # updates is a list
        note_store.updateNote(session['identifier'], upnote)
