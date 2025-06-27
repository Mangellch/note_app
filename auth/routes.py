import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from extensions import db, mail                    # <— usa las mismas instancias
from models import User
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy import func

auth_bp = Blueprint('auth', __name__)

# --- Login con admin/root ---
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if username.lower() == 'admin' and password == 'root':
            session['user_id'] = 0
            session['user'] = 'admin'
            flash('Inicio de sesión exitoso ✨ (admin)', 'success')
            return redirect(url_for('notes.home'))

        user = User.query.filter(func.lower(User.username) == username.lower()).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user'] = user.username
            flash('Inicio de sesión exitoso ✨', 'success')
            return redirect(url_for('notes.home'))

        flash('Usuario o contraseña incorrectos', 'error')
        return redirect(url_for('auth.login'))
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if len(password) < 6 or not re.search(r'\d', password):
            flash("La contraseña debe tener al menos 6 caracteres y un número.", "error")
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first():
            flash("Ese correo ya está registrado.", "error")
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=username).first():
            flash("Ese nombre de usuario ya existe.", "error")
            return redirect(url_for('auth.register'))

        new_user = User(email=email, username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("¡Cuenta creada! Inicia sesión por favor 😊", "success")
        return redirect(url_for('auth.login'))
    return render_template('register.html')


def generate_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-recovery')


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='password-recovery', max_age=expiration)
    except Exception:
        return False
    return email


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            token = generate_token(user.email)
            reset_url = url_for('auth.reset_password', token=token, _external=True)

            msg = Message("Recuperar contraseña", recipients=[email])
            msg.body = f"Para restablecer tu contraseña, haz click aquí: {reset_url}"
            msg.charset = 'utf-8'
            mail.send(msg)

            flash("Correo de recuperación enviado. Revisa tu bandeja.", "success")
        else:
            flash("Correo no encontrado.", "error")
        return redirect(url_for('auth.login'))
    return render_template('forgot_password.html')


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = confirm_token(token)
    if not email:
        flash("El enlace de recuperación no es válido o ha expirado.", "error")
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password')
        if len(password) < 6 or not re.search(r'\d', password):
            flash("La contraseña debe tener al menos 6 caracteres y un número.", "error")
            return redirect(url_for('auth.reset_password', token=token))
        user = User.query.filter_by(email=email).first()
        if user:
            user.set_password(password)
            db.session.commit()
            flash("Contraseña actualizada correctamente.", "success")
            return redirect(url_for('auth.login'))
        else:
            flash("Usuario no encontrado.", "error")
            return redirect(url_for('auth.forgot_password'))
    return render_template('reset_password.html')
