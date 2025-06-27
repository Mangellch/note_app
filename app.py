from flask import Flask, request
from config import Config
from extensions import db, mail, migrate     
from notes.routes import notes_bp
from auth.routes import auth_bp

from dotenv import load_dotenv
load_dotenv()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa extensiones
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    # Registrar blueprints
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

    return app
