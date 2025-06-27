import unittest

from app import create_app

from models import db, Note

class NoteTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app("config.TestConfig")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def test_create_note(self):
        with self.app.app_context():
            note_db = Note(title = 'Titulo', content = 'Contenido')
            db.session.add(note_db)
            db.session.commit()

            note = Note.query.first()

            self.assertEqual(note.title, 'Titulo')
            self.assertEqual(note.content, 'Contenido')

def test_create_note_route(self):
    with self.app.app_context():
        response = self.client.post('/crear-nota', data={
            'title': 'Prueba route',
            'content': 'Contenido route'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Prueba route', response.data)