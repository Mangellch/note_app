from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from datetime import date

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.Date, default=date.today) 

    def __repr__(self):
        return f'<Note {self.id}: {self.title}>'


class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80),  unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at    = db.Column(db.DateTime, default=date.today)

    # ---------- Helpers ----------
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)