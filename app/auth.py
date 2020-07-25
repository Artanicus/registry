#!/usr/bin/env python3

from absl import logging
from flask import Blueprint, render_template, flash, redirect, request
from flask_login import UserMixin, login_user, login_required, logout_user, current_user

import grpc
from urllib.parse import urlparse, urljoin

from steward import user_pb2 as u
from steward import registry_pb2_grpc

from app.forms import LoginForm
from app.extensions import lm, mail, bcrypt
from app import util
bp = Blueprint("auth", __name__)

channel = grpc.insecure_channel('localhost:50051')
users = registry_pb2_grpc.UserServiceStub(channel)

logging.set_verbosity(logging.INFO)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        target_user = users.GetUser(u.GetUserRequest(email=form.email.data))
        if bcrypt.check_password_hash(target_user.password, form.password.data):
            user = WrappedUser()
            user.load(target_user)
            login_user(user)
            flash('Login succeeded for user {}'.format(form.email.data))

            next = util.get_redirect_target()
            return redirect(next)
        else:
            logging.info('email login fail: {}'.format(target_user.email))
            flash('Incorrect password')
    return render_template('login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = CreateUserForm()
    if form.validate_on_submit():
        user = u.CreateUserRequest()
        user.name = form.name.data
        user.email = form.email.data
        user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        users.CreateUser(user)
        flash('User Created for {}'.format(form.email.data))
        return redirect('/')
    return render_template('register.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@lm.user_loader
def load_user(user_id):
    if user_id:
        user = WrappedUser(user_id)
        return user
    else:
        logging.error('load_user called without valid id!')

class WrappedUser(UserMixin):
    def __init__(self, user_id=None):
        if user_id:
            logging.debug('user created by id: {user_id}'.format(user_id=user_id))
            self.user = users.GetUser(u.User(_id=user_id))
        else:
            logging.debug('LazyLoading user')
            self.user = 'noneuser'
    def get_id(self):
        return self.user._id

    def load(self, proto):
        if proto:
            logging.debug('Loading user: {}'.format(proto))
            self.user = proto
        else:
            logging.error('Tried to load user with empty proto!')