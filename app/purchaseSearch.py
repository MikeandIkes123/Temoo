from flask import render_template
from flask_login import current_user
import datetime
from flask import request

from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('purchaseSearch', __name__)

@bp.route('/search_purchases', methods=['GET'])
def search_purchases():
    user_id = request.args.get('user_id')
    if not user_id:
        return render_template('purchases.html', error="No user ID provided")

    # get all purchases
    purchases = Purchase.get_all_by_uid(user_id)

    if not purchases:
        return render_template('purchases.html', error=f"No purchases found for user ID {user_id}", user_id=user_id)

    return render_template('purchases.html', purchases=purchases, user_id=user_id)

