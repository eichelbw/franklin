import oauth2 as oauth
import config

# all this from https://github.com/dasevilla/evernote-oauth-example
def get_oauth_client(token=None):
    """Return an instance of the OAuth client."""
    consumer = oauth.Consumer(config.EN_CONSUMER_KEY, config.EN_CONSUMER_SECRET)
    if token:
        client = oauth.Client(consumer, token)
    else:
        client = oauth.Client(consumer)
    return client


def get_notestore():
    """Return an instance of the Evernote NoteStore. Assumes that 'shardId' is
    stored in the current session."""
    shardId = session['shardId']
    noteStoreUri = EN_NOTESTORE_URIBASE + shardId
    noteStoreHttpClient = THttpClient.THttpClient(noteStoreUri)
    noteStoreProtocol = TBinaryProtocol.TBinaryProtocol(noteStoreHttpClient)
    noteStore = NoteStore.Client(noteStoreProtocol)
    return noteStore


def get_userstore():
    """Return an instance of the Evernote UserStore."""
    userStoreHttpClient = THttpClient.THttpClient(EN_USERSTORE_URIBASE)
    userStoreProtocol = TBinaryProtocol.TBinaryProtocol(userStoreHttpClient)
    userStore = UserStore.Client(userStoreProtocol)
    return userStore
