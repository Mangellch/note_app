from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == 'root':
            session['user'] = username
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('notes.home'))
        else:
            flash('Usuario no permitido', 'error')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('auth.login'))