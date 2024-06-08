from flask import render_template, redirect, url_for, request, flash, session, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
import sqlalchemy as sa
from flask_app import db, login
from flask_app.forms import LoginForm, RegistrationForm
from flask_app.models import User

from . import app

user_name = ""

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')


@app.route('/overview', methods=["GET", "POST"])
@login_required
def overview():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('overview'))
    

@app.route('/costs', methods=["GET", "POST"])
@login_required
def costs():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('costs'))
    

@app.route('/suppliers', methods=["GET", "POST"])
@login_required
def suppliers():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('suppliers'))
    

@app.route('/labour', methods=["GET", "POST"])
@login_required
def labour():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('labour'))
    

@app.route('/materials', methods=["GET", "POST"])
@login_required
def materials():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('materials'))
    

@app.route('/reports', methods=["GET", "POST"])
@login_required
def reports():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('reports'))


@app.route('/auth', methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('overview'))
    
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
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



# @app.route('/get_user_info', methods=["GET"])
# def get_user_info():
#     if 'user_id' in session:
#         user_id = session['user_id']
#         user = User.query.get(user_id)
#         user_info = {
#             'id': user.id,
#             'username': user.username,
#             'email': user.email
#             # Add other user info as needed
#         }
#         return jsonify(user_info)
#     return jsonify({'error': 'User not logged in'}), 401