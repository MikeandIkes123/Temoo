from flask import render_template
from flask_login import current_user
import datetime
from flask import request

from .models.product import Product
from .models.purchase import Purchase
from .models.sells import Sells

from flask import Blueprint
bp = Blueprint('sellerSearch', __name__)

@bp.route('/search_sellers', methods=['GET'])
def search_sellers():
    user_id = request.args.get('seller_id')
    if not user_id:
        return render_template('seller.html', error="No seller ID provided")

    # get all inventory from the SQL database where uid = user_id 
    inventory = Sells.get_inventory_by_seller(user_id)

    if not inventory:
        return render_template('seller.html', error=f"No items found for seller ID {user_id}", user_id=user_id)

    return render_template('seller.html', inventory=inventory, seller_id=user_id)

