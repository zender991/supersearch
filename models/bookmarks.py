from app import db
from flask_login import current_user

class Bookmarks(db.Model):

    __tablename__ = 'bookmarks'
    id = db.Column(db.Integer, primary_key=True)
    user_bookmark = db.Column(db.String(150))
    user_id_bm = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, user_bookmark, user_id_bm):
        self.user_bookmark = user_bookmark
        self.user_id_bm = user_id_bm