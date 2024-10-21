from flask import render_template
from flask_login import current_user
import datetime
from flask import request

from .models.product import Product

from flask import Blueprint
bp = Blueprint('productSearch', __name__)

@bp.route('/search_products', methods=['GET'])
def search_products():
    top_k = request.args.get('top_k_expensive')
    
    if not top_k:
        products = Product.get_top_k(k=top_k, all=True)
    else: 
        products = Product.get_top_k(k=top_k, all=False)
    
    return render_template('products.html', products=products)
