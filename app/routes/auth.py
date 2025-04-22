from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.models import User
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('member.profile'))
        flash('Invalid email or password')
    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('auth.register'))
        
        user = User(
            email=email,
            firstname=request.form.get('firstname'),
            lastname=request.form.get('lastname')
        )
        user.set_password(request.form.get('password'))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('member.profile'))
    return render_template('auth/register.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
