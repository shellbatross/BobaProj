from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import movie_client
from ..forms import BobaReviewForm, SearchForm
from ..models import User, Review, Boba
from ..utils import current_time
import os 
bobas = Blueprint("bobas", __name__)

""" ************ View functions ************ """
#Sign going to have to nuke this soon 

@bobas.route("/", methods=["GET", "POST"])
def index():
    pics = '/images/chocolate.png'
    # AddToCartForm
    # return redirect(url_for("bobas.cart"))
    return render_template("index.html", all_flavors= pics)


@bobas.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = movie_client.search(query)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("movies.index"))

    return render_template("query.html", results=results)

#WIP
#TODO: Do AddToCart here since we have boba id and all the info
@bobas.route("/bobas/<boba_id>", methods=["GET", "POST"])
def boba_detail(boba_id):
    try:
        result = movie_client.retrieve_boba_by_id(boba_id) #TODO: harcode a list of bobas
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("users.login"))

    form = BobaReviewForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            boba_id = result.id,
            boba_name = result.name,
            boba_price = result.price
        )
        review.save()

        return redirect(request.path)

    reviews = Review.objects(boba_id=boba_id)

    return render_template(
        "boba_detail.html", form=form, boba=result, reviews=reviews
    )


@bobas.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    reviews = Review.objects(commenter=user)

    return render_template("user_detail.html", username=username, reviews=reviews)

#TODO: WIP
@bobas.route("/cart/<username>")
def cart_detail(username):
    user = User.objects(username=username).first()
    cart = Boba.objects(buyer=username) # gets the cart for username

    return render_template("cart_detail.html", username=username, cart=cart)