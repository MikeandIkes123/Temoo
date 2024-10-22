from flask import Blueprint, render_template, request
from flask_login import current_user
from .models.cart import Cart
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

# def view_cart():
#     # if current_user.is_authenticated:
#     cart_items = Cart.get_cart_items()
#     return render_template('cart.html', cart_items=cart_items)
#     # else:
#     #     return render_template('cart.html', cart_items=[], error="Please log in to view your cart.")


# def add_to_cart():
#     if not current_user.is_authenticated:
#         flash("You need to be logged in to add items to your cart!", "danger")
#         return redirect(url_for('users.login'))

#     pid = request.form.get('pid')  # Product ID
#     quantity = request.form.get('quantity')  # Quantity

#     # Insert the item into the Cart table
#     app.db.execute('''
#         INSERT INTO Cart (user_id, pid, quantity) VALUES (:user_id, :pid, :quantity)
#     ''', {
#         'user_id': current_user.id,
#         'pid': pid,
#         'quantity': quantity
#     })

#     flash("Item added to cart successfully!", "success")
#     return redirect(url_for('index.index'))  # Redirect to home or desired page