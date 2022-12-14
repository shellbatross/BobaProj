from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import boba_client
from ..forms import BobaReviewForm, SearchForm, AddToCartForm
from ..models import User, Review, Boba
from ..utils import current_time
import os 
import io
import base64
bobas = Blueprint("bobas", __name__)

def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

""" ************ View functions ************ """
#Sign going to have to nuke this soon 

@bobas.route("/", methods=["GET", "POST"])
def index():
    pics = '/images/chocolate.png'
    # AddToCartForm
    # return redirect(url_for("bobas.cart"))
    return render_template("index.html", all_flavors= pics)


#WIP
#TODO: Do AddToCart here since we have boba id and all the info
@bobas.route("/bobas/<boba_id>", methods=["GET", "POST"])
def boba_detail(boba_id):
    try:
        result = boba_client.retrieve_boba_by_id(boba_id) #TODO: harcode a list of bobas
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("users.login"))

    review_form = BobaReviewForm()
    if review_form.validate_on_submit() and current_user.is_authenticated:
        review = Review(
            commenter=current_user._get_current_object(),
            content=review_form.text.data,
            date=current_time(),
            boba_name = result.name,
            boba_price = result.price, 
            image = get_b64_img(current_user._get_current_object().username)
        )
        review.save()
        return redirect(request.path)
    
    cart_form = AddToCartForm()
    if cart_form.validate_on_submit() and current_user.is_authenticated:
        boba = Boba(
            buyer = current_user._get_current_object(),
            boba_name = result.name,
            boba_price = result.price
        )
        boba.save()

    
    reviews = Review.objects(boba_name=boba_id)

    return render_template(
        "boba_detail.html", form=review_form, cart_form = cart_form, boba=result, reviews=reviews
    )

@bobas.route("/bobas/<boba_id>/nutrition", methods=["GET", "POST"])
def boba_nutrition(boba_id):
    try:
        nutrition = boba_client.get_nutrition(boba_id)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("users.login"))

    return render_template(
        "nutrition.html", nutrition = nutrition, boba = boba_id
    )

@bobas.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    reviews = Review.objects(commenter=user)
    img = get_b64_img(user.username)

    return render_template("user_detail.html", username=username, reviews=reviews, image=img)

#TODO: WIP
@bobas.route("/user/cart")
def cart_detail():
    user = current_user._get_current_object()
    img = get_b64_img(user.username)
    cart = Boba.objects(buyer=user) # gets the cart for username

    return render_template("cart_detail.html", user=user, cart=cart, image=img)