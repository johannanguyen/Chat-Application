import flask_sqlalchemy
from app import db


class MessageHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    db_username = db.Column(db.String(50))
    db_message = db.Column(db.String(200))
    db_image = db.Column(db.String(200))
    
    def __init__(self, db_username, db_message, db_image):
        self.db_username = db_username
        self.db_message = db_message
        self.db_image = db_image
        
    def __repr__(self):
        return '<Message %s>' % self.db_message 