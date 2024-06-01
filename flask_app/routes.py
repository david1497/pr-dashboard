from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
import sqlalchemy as sa
from flask_app import db
from flask_app.forms import LoginForm, RegistrationForm
from flask_app.models import User

from . import app

user_name = ""

@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')


@app.route('/overview/', methods=["GET", "POST"])
@login_required
def overview():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('overview'))


@app.route('/auth', methods=["GET", "POST"])
def login():
    print(f'\n\nGot in the login method\n\n')

    if current_user.is_authenticated:
        print(f'\n\nDEBUG:Current user is authenticated and should be able to move to overview\n\n')
        return redirect(url_for('overview'))
    
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        print(f"Got the user {user}")
        if user is None or not user.check_password(form.password.data):
            flash(f'Invalid username {form.username.data}')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('overview')
        return redirect(next_page) 

    return render_template('auth.html', form=form)


@app.route('/logout')
def logout():
    if current_user.is_anonymous:
        return(redirect(url_for('login')))
    else:
        logout_user()
        return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('overview'))
    form = RegistrationForm()   
    if form.validate_on_submit():
        user = User(
            f_name = form.f_name.data,
            l_name = form.l_name.data,
            username = form.username.data,
            role = form.role.data,
            email = form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'User {user.username} created successfully!')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)