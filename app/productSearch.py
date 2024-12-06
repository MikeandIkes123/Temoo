from flask import render_template
from flask_login import current_user
import datetime
from flask import request

from .models.product import Product
from .models.feedback import Feedback
from .models.sells import Sells

from flask import Blueprint
bp = Blueprint('productSearch', __name__)

@bp.route('/search_products_price', methods=['GET'])
def search_products_price():
    top_k = request.args.get('top_k_expensive')
    
    if not top_k:
        products = Product.get_top_k(k=top_k, all=True)
    else: 
        products = Product.get_top_k(k=top_k, all=False)
    
    return render_template('products.html', products=products)

@bp.route('/search_products_category', methods=['GET'])
def search_products_category():
    main_category = request.args.get('main_category')
    
    if not main_category:
        products = Product.get_category(cat=main_category, all=True)
    else: 
        products = Product.get_category(cat=main_category, all=False)
    
    return render_template('products.html', products=products)

@bp.route('/search_products_keyword', methods=['GET'])
def search_products_keyword():
    keyword = request.args.get('keyword')
    
    if not keyword:
        products = Product.get_keyword(word=keyword, all=True)
    else: 
        products = Product.get_keyword(word=keyword, all=False)
    
    return render_template('products.html', products=products)

@bp.route('/product_details/<int:product_id>')
def product_details(product_id):
    # product_id = request.args.get('product_id')
    product = Product.get(product_id)
    feedback = Feedback.get_feedback_by_product(product_id)
    
    sellers_info = Sells.get_seller_from_product(product_id)
    
    if not sellers_info:
        sellers_info = [Sells(uid="NA", pid=product_id, quantity=0)]
    
    if product:
        return render_template('product_details.html', product=product, current_user = current_user, feedbacks = feedback)
    else:
        return "Product not found", 404
