from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Mail, Message

from .. import bcrypt, mail
from werkzeug.utils import secure_filename
import io
import base64
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm
from ..models import User



"""
Definitely keeping these to use as reference for when we make our own blueprints
"""
def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

users = Blueprint("users", __name__)

""" ************ User Management views ************ """

@users.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("bobas.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        user.save()
        msg = Message(
                'Hello',
                sender ='bobatea.shop1@gmail.com',
                recipients = [form.email.data]
               )
        msg.body = 'Hewwo, thanks for registering for our boba shop account uwu'
        mail.send(msg)

        return redirect(url_for("users.login"))

    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("bobas.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()

        if user is not None and bcrypt.check_password_hash(
            user.password, form.password.data
        ):
            login_user(user)
            return redirect(url_for("users.account"))
        else:
            flash("Login failed. Check your username and/or password")
            return redirect(url_for("users.login"))

    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("bobas.index"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    user_form = UpdateUsernameForm()
    picture_form = UpdateProfilePicForm()
    if current_user:
        if picture_form.validate_on_submit():
            img = picture_form.picture.data
            filename = secure_filename(img.filename)
            content_type = f'images/{filename[-3:]}'

            if current_user.profile_pic.get() is None:
                current_user.profile_pic.put(img.stream, content_type=content_type)
            else:
                current_user.profile_pic.replace(img.stream, content_type=content_type)
            current_user.save()
        img = get_b64_img(current_user.get_id())
    if user_form.validate_on_submit():
        user = User.objects(username=current_user.get_id()).first()
        if (user is not None):
            user.modify(username=user_form.username.data)
            user.save()
    
    return render_template("account.html", title="Account", user_form=user_form, picture_form=picture_form, image=img)
