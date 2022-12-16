from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
from . import config
from .utils import current_time
import base64

"""
We edit these, I think we could keep a very similar thing for user, Review will be very similar as well 
"""
@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()


class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    profile_pic = db.ImageField()

    # Returns unique string identifying our object
    def get_id(self):
        return self.username
    


class Review(db.Document):
    commenter = db.ReferenceField(User, required=True)
    content = db.StringField(required=True, min_length=5, max_length=500)
    date = db.StringField(required=True)
    boba_name = db.StringField(required=True, min_length=1, max_length=9)
    boba_price = db.IntField(required=True, min_length=1, max_length=100)
    image = db.StringField()


class Boba(db.Document):
    buyer = db.ReferenceField(User, required=True)
    boba_name = db.StringField(required=True, min_length=1, max_length=100)
    boba_price = db.IntField(required=True, min_length=1, max_length=100)
    image = db.StringField()

