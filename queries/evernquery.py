from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types

dev_token = "S=s385:U=3e7d2ff:E=150f8d4c12f:C=149a12394c0:P=1cd:A=en-devtoken:V=2:H=44734894e812cbfe03d83cc365d8c9c5"
client = EvernoteClient(token=dev_token, sandbox=False)
userStore = client.get_user_store()
user = userStore.getUser()
print user.username

noteStore = client.get_note_store()
notebooks = noteStore.listNotebooks()
for n in notebooks:
    print n.name

#note = Types.Note()
#note.title = "test note"
#note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd"><en-note>Hello world!</en-note>'
#note = noteStore.createNote(note)
