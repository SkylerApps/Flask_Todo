import bcrypt
from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import current_user, login_user, login_required, logout_user

from extensions import db
from models.User import User
from forms.Login import LoginForm
from forms.Registration import RegistrationForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('todo.show_todos'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user.password):
            login_user(user, remember=True)
            return redirect(url_for('todo.show_todos'))
        else:
            flash('Invalid email or password', 'danger')

    # We render the template because 'redirect' will cause a loop when this hits
    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('todo.show_todos'))


@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('todo.show_todos'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('auth.login'))

    elif request.form.get('email'):
        username = request.form.get('email')
        password = request.form.get('password')
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = User(email=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

    return render_template('register.html', title='Register', form=form)
