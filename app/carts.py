from flask import Blueprint, render_template, request, url_for, redirect, flash
from .models.cart import Cart
from flask import current_app as app

bp = Blueprint('cart', __name__)


@bp.route('/cart', methods=['GET'])
def view_cart():
    user_id = request.args.get('user_id')
    
    if not user_id:
        return render_template('cart.html', error="No user ID provided")

    # Get the cart items for the specified user ID
    cart_items = Cart.get_cart_items(user_id)  # Implement this method in your Cart model

    if not cart_items:
        return render_template('cart.html', error=f"No items found in the cart for user ID {user_id}")

    return render_template('cart.html', cart_items=cart_items, user_id=user_id)
