from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import Note
from extensions import db

notes_bp = Blueprint('notes', __name__)

# ---------- Home ----------
@notes_bp.route('/')
def home():
    if 'user' not in session:
        flash("Por favor, inicia sesión para ver las notas.", "error")
        return redirect(url_for('auth.login'))

    page = request.args.get('page', 1, type=int)          # ← lee ?page=N (default 1)
    per_page = 10                                         # ← 10 notas por página

    pagination = Note.query.order_by(Note.created_at.desc()) \
                            .paginate(page=page, per_page=per_page, error_out=False)

    notes = pagination.items                              # ← solo las notas de esa página
    return render_template('home.html',
                           notes=notes,
                           pagination=pagination)

# ---------- Crear ----------
@notes_bp.route('/crear-nota', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        title   = request.form.get('title', '')
        content = request.form.get('content', '')

        new_note = Note(title=title, content=content)
        
        db.session.add(new_note)
        db.session.commit()
        flash("Nota creada exitosamente!", "success")
        return redirect(url_for('notes.home'))

    # GET: muestra formulario vacío
    return render_template('note_form.html')

# ---------- Editar ----------
@notes_bp.route('/editar-nota/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    note = Note.query.get_or_404(id)

    if request.method == 'POST':
        note.title   = request.form.get('title', '')
        note.content = request.form.get('content', '')
        db.session.commit()
        flash("Cambios guardados!", "success")
        return redirect(url_for('notes.home'))

    # GET: muestra formulario con datos precargados
    return render_template('edit_note.html', note=note)

# ---------- Eliminar ----------
@notes_bp.route('/eliminar-nota/<int:id>', methods=['POST'])
def del_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    flash("Nota eliminada!", "success")
    return redirect(url_for('notes.home'))
