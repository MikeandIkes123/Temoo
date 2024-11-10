from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('myprofile', __name__)


@bp.route('/myprofile')
def myprofile():
    return render_template('myprofile.html', title='My Profile')

@bp.route('/purchase_history', methods=['GET'])
def purchase_history():
    user_id = current_user.id

    # get all purchases
    purchases = Purchase.get_all_by_uid(user_id)

    if not purchases:
        return render_template('purchases.html', error=f"No purchases found for user ID {user_id}", user_id=user_id)

    return render_template('purchases.html', purchases=purchases, user_id=user_id)