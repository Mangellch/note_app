from datetime import date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.Date, default=date.today)  # ← usa db.Date, no db.DateTime

    def __repr__(self):
        return f'<Note {self.id}: {self.title}>'
