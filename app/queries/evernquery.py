from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
import evernote.edam.type.ttypes as Types
from evernote.edam.type.ttypes import NoteSortOrder

# client = EvernoteClient(token=dev_token, sandbox=False)
# note_store = client.get_note_store() # Evernote's Note Store object is the access point to all note-related information
# all_tags = note_store.listTags()
# todo_guid = [tag for tag in all_tags if tag.name == "todo"][0].guid # compare all tags to "todo" and grab guid
#
# note_filter = NoteFilter() # the notefilter object allows us to define filters for our eventual findNotesMetadata call
# note_filter.tagGuids = [todo_guid] # find note with todo guid (ie, the todo note)
# offset, max_notes = 0, 10
# result_spec = NotesMetadataResultSpec(includeTitle=True) # allows us to request specific info be returned about the note
# result_list = note_store.findNotesMetadata(dev_token, note_filter, offset, max_notes, result_spec)
# todo_note_guids = [note.guid for note in result_list.notes]


def get_todo_notes():
    """executes EN api query and returns content of note tagged 'todo'"""
    out_notes = []
    for guid in todo_note_guids:
        out_notes.append(note_store.getNote(dev_token, str(guid), True, False, False, False))
    return out_notes

def post_todo_updates(updates):
    """updates EN api with modifications to the notes"""
    HEADER = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">\n<en-note>'
    TAIL = '</en-note>'
    for index, tdn in enumerate(get_todo_notes()): # use get_todo_notes bc it's a handy way to get guid and title. probs slow.
        upnote = Types.Note()
        upnote.title, upnote.guid = tdn.title, tdn.guid
        upnote.content = HEADER + updates[index] + TAIL # updates is a list
        note_store.updateNote(upnote)

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

