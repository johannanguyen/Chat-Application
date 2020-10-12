import flask_sqlalchemy
from app import db


class SavedMessages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    db_message = db.Column(db.String(200))
    db_username = db.Column(db.String(20))
    
    def __init__(self, db_message, db_username):
        self.db_message = db_message
        self.db_username = db_username
        
    def __repr__(self):
        return '<Message: %s>' % self.db_message