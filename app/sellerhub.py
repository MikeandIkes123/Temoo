from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User
from .models.product import Product
from .models.purchase import Purchase
from .models.sells import Sells


from flask import Blueprint
bp = Blueprint('sellerhub', __name__)

@bp.route('/view_sellerhub', methods=['GET'])
def view_hub():
    if not current_user.is_authenticated or not current_user.is_seller(current_user.id):
        render_template('seller.html', error="You are not a seller.")
        
    inventory = Sells.get_inventory_by_seller(current_user.id)
    orders = Purchase.get_all_purchases_for_seller(current_user.id)

    return render_template('seller.html', inventory = inventory, orders = orders)

@bp.route('/add_product', methods=['POST'])
def add_product():
    product_name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('description')
    category = request.form.get('main_category')
    sub_category = request.form.get('sub_category')
    img_link = request.form.get('image')
    quantity = request.form.get('quantity')
    
    print(product_name, price, description, category, sub_category, img_link, quantity)
    new_prod_id = Product.new_product(product_name, price, quantity, description, category, sub_category, img_link)
    Sells.add_product(current_user.id, new_prod_id, quantity)
    
    return redirect(url_for('sellerhub.view_hub'))

@bp.route('/update_product', methods=['POST'])
def update_product():
    product_id = request.form.get('product_id')
    price = request.form.get('price')
    quantity = request.form.get('quantity')
    
    if price:
        Product.update_product_price(product_id, price)
    if quantity:
        Product.update_product_quantity(product_id, quantity)
    return redirect(url_for('sellerhub.view_hub'))

@bp.route('/delete_product', methods=['POST'])
def delete_product():
    product_id = request.form.get('product_id')
    Product.delete_product(product_id)
    
    return redirect(url_for('sellerhub.view_hub'))

@bp.route('/update_order', methods=['POST'])
def update_order():
    order_id = request.form.get('order_id')

    Purchase.update_order_status(order_id)
    
    return redirect(url_for('sellerhub.view_hub'))