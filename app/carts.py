from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user # type: ignore
from .models.cart import Cart
bp = Blueprint('cart', __name__)


@bp.route('/view_cart', methods=['GET'])
def view_cart():
    # Get user_id from the query parameter, if available, otherwise use current_user
    #FIXME: doesn't work unless person is logged in :( -> change default behavior 
    user_id = request.args.get('user_id', default=current_user.id, type=int)
 
    # Fetch the cart items for the user
    cart_items = Cart.get_cart_items(user_id)

    # Pass the cart items to the template
    return render_template('cart.html', cart_items=cart_items, user_id=user_id)


@bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = request.form.get('quantity', 1)  # Default quantity to 1 if not specified
    user_id = current_user.id  # Assuming user is logged in and current_user is available

    # Logic to add the product to the cart
    Cart.add_item(user_id, product_id, quantity)  # Implement this method in Cart model

    # Redirect to view_cart with user_id as a query parameter
    return redirect(url_for('cart.view_cart', user_id=user_id))