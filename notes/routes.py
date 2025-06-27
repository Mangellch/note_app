from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import Note
from extensions import db

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/')
def home():
    if 'user_id' not in session:
        flash("Por favor, inicia sesión para ver las notas.", "error")
        return redirect(url_for('auth.login'))

    page = request.args.get('page', 1, type=int)
    per_page = 10

    pagination = Note.query.filter_by(user_id=session['user_id']) \
                            .order_by(Note.created_at.desc()) \
                            .paginate(page=page, per_page=per_page, error_out=False)

    notes = pagination.items
    return render_template('home.html', notes=notes, pagination=pagination)

@notes_bp.route('/crear-nota', methods=['GET', 'POST'])
def create_note():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para crear una nota.", "error")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form.get('title', '')
        content = request.form.get('content', '')

        new_note = Note(title=title, content=content, user_id=session['user_id'])
        db.session.add(new_note)
        db.session.commit()

        flash("Nota creada exitosamente!", "success")
        return redirect(url_for('notes.home'))

    return render_template('note_form.html')

@notes_bp.route('/editar-nota/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    note = Note.query.get_or_404(id)

    if 'user_id' not in session or note.user_id != session['user_id']:
        flash("No tienes permiso para editar esta nota.", "error")
        return redirect(url_for('notes.home'))

    if request.method == 'POST':
        note.title = request.form.get('title', '')
        note.content = request.form.get('content', '')
        db.session.commit()

        flash("Cambios guardados!", "success")
        return redirect(url_for('notes.home'))

    return render_template('edit_note.html', note=note)

@notes_bp.route('/eliminar-nota/<int:id>', methods=['POST'])
def del_note(id):
    note = Note.query.get_or_404(id)

    if 'user_id' not in session or note.user_id != session['user_id']:
        flash("No tienes permiso para eliminar esta nota.", "error")
        return redirect(url_for('notes.home'))

    db.session.delete(note)
    db.session.commit()

    flash("Nota eliminada!", "success")
    return redirect(url_for('notes.home'))
