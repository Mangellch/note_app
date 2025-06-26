from flask import Flask, request
from config import Config
from models import db
from notes.routes import notes_bp
from auth.routes import auth_bp
from flask_migrate import Migrate 

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)  # <-- inicializar migrate

app.register_blueprint(notes_bp)
app.register_blueprint(auth_bp)

@app.route('/about')
def about():
    return "This is the about page."

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        return "Form submitted successfully!", 201
    return "This is the contact page."


if __name__ == '__main__':
    app.run(debug=True)
