from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask import request
from flask import session
from app.models import UserInfo
from app.models import Role
from app import app
from app import db
import os


@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html', title='Login')


@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html', title='Profile')


@app.route('/adduser', methods=['POST', 'GET'])
def adduser():
    status = ''
    message = ''
    form = [request.form['firstname'], request.form['lastname'], request.form['middlename'],
            request.form['birthdate'], request.form['address'], request.form['cemail'],
            request.form['cnumber'], request.form['username'], request.form['password'],
            request.form['role']]

    if request.method == 'POST' and request.form['password'] == request.form['cpassword']:
        user_info = UserInfo(request.form['firstname'], request.form['lastname'], request.form['middlename'],
                             request.form['birthdate'], request.form['address'], request.form['cemail'],
                             request.form['cnumber'], request.form['username'], request.form['password'],
                             request.form['role'])
        db.session.add(user_info)
        db.session.commit()
        message = 'New user was added.'
        status = 'success'
    elif request.method == 'POST' and request.form['password'] != request.form['cpassword']:
        message = 'Password doesn\'t match!'
        status = 'fail'
    else:
        message = 'Please fill all fields with asterisk (*).'
        status = 'none'

    return render_template('adduser.html', title='Add User', status=status, message=message, form=form)


@app.route('/viewuser')
@app.route('/viewuser.html')
def viewuser():
    return render_template('viewuser.html', title='View User')
