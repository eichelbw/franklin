Franklin is pseudonym for [microblog](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world/ "Flask Tutorial"), a demo app used to learn Flask made by [Miguel Grinberg](http://blog.miguelgrinberg.com/author/Miguel%20Grinberg). Since it's all his stuff anyway, I make no claim to original thought!

WIP

---

Okay so once this is over, the plan is to build a todo application (a la [TodoMVC](todomvc.com)) except that I'd like to pull tasks from the [Evernote](https://dev.evernote.com/doc/start/python.php) and [Google Calendar](https://developers.google.com/google-apps/calendar/firstapp) APIs.

**EDIT**

Have begun persuing the todo aspect of this project more than the Flask side of things. As such, _microblog_ progress is on hold.

Presently, sync works both ways for Evernote todos.

With that in mind. . .

**TODO**

- [X] Acquire dev key for Evernote
- [X] Write some API requests to get familiar
- [X] Get previously created todo note from Evernote
- [X] Display contents of todo note
- [X] Format todo contents as html
- [X] Allow user to interact with a todo (using javascript, probably)
- [X] Sync todo status to EN
- [X] Allow non-todo related divs to persist through syncs
- [X] Allow for multiple notes tagged todo
- [X] Get EN functionality working through oAuth
- [ ] Do all that with Google calander
- [ ] Finish the microblog tutorial
- [ ] Move Franklin off of /index
- [ ] Pretty the damn thing up a bit I suppose
