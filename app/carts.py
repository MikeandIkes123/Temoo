from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required # type: ignore
from .models.cart import Cart
bp = Blueprint('cart', __name__)


@bp.route('/view_cart', methods=['GET'])
@login_required
def view_cart():
    # Get user_id from the query parameter, if available, otherwise use current_user
    #FIXME: doesn't work unless person is logged in :( -> change default behavior 
    user_id = request.args.get('user_id', default=current_user.id, type=int)
 
    # Fetch the cart items for the user
    cart_items = Cart.get_cart_items(user_id)
    total_price = Cart.get_total_price(user_id)  # Get the total price of the cart
    # Pass the cart items to the template
    return render_template('cart.html', cart_items=cart_items, user_id=user_id, total_price=total_price)

@bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = request.form.get('quantity', 1)  # Default quantity to 1 if not specified
    user_id = current_user.id  # Assuming user is logged in and current_user is available

    # Logic to add the product to the cart
    Cart.add_item(user_id, product_id, quantity)  # Implement this method in Cart model

    # Redirect to view_cart with user_id as a query parameter
    return redirect(url_for('cart.view_cart', user_id=user_id))

@bp.route('/update_cart', methods=['POST'])
def update_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 0))
    user_id = current_user.id

    if quantity > 0:
        Cart.update_item(user_id, product_id, quantity)  
    else:
        Cart.remove_item(user_id, product_id)  

    return redirect(url_for('cart.view_cart', user_id=user_id))

@bp.route('/clear_cart', methods=['POST'])
def clear_cart():
    user_id = current_user.id  # Ensure it only clears the current user's cart
    Cart.clear_cart(user_id)
    return redirect(url_for('cart.view_cart', user_id=user_id))

@bp.route('/submit_cart', methods=['POST'])
def submit_cart():
    user_id = current_user.id

    cart_items = Cart.get_cart_items(user_id)
    if not cart_items:
        return redirect(url_for('cart.view_cart'))

    Cart.submit_cart(user_id)
    return redirect(url_for('myprofile.purchase_history'))


