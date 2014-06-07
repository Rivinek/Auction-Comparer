from google.appengine.ext import db
from google.appengine.ext import blobstore


class Searched(db.Model):
    """Model for individual searcher with his date"""
    author = db.UserProperty()
    content = db.StringProperty()
    date = db.DateProperty(auto_now_add=True)
    url = db.LinkProperty()
    blob_allegro = blobstore.BlobReferenceProperty()
    blob_nokaut = blobstore.BlobReferenceProperty()


def user_key(user_name='default_results'):
    """Constructs a datastore key for a Results entity with user_name."""
    return db.Key.from_path('Results', user_name)
