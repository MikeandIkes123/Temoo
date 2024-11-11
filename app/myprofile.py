from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('myprofile', __name__)


@bp.route('/myprofile')
def myprofile():
    return render_template('myprofile.html', title='My Profile')

class UpdateProfileForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Update Profile')

    def validate_email(self, email):
        if User.email_exists(email.data) and email.data != current_user.email:
            raise ValidationError('Already a user with this email.')


@bp.route('/update_profile', methods = ["GET", "POST"])
def update_profile():
    form = UpdateProfileForm()
    if request.method == "GET":
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.email.data = current_user.email
        form.address.data = current_user.address
    if form.validate_on_submit():
        id = current_user.id
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        address = form.address.data
        password = form.password.data

        if User.update_profile(id, firstname, lastname, email, address, password):
            return redirect(url_for('myprofile.myprofile'))

    return render_template('update_profile.html', title='Edit Profile', form=form)


class UpdateBalanceForm(FlaskForm):
    deposit = DecimalField('Deposit: ', places=2)
    withdrawal = DecimalField('Withdraw: ', places=2)
    submit = SubmitField('Update Balance')
    def validate_withdrawal(self, withdrawal):
        if withdrawal.data and withdrawal.data > current_user.balance:
            raise ValidationError("Insufficient balance for this withdrawal.")

@bp.route('/update_balance', methods = ["GET", "POST"])
def update_balance():
    form = UpdateBalanceForm()
    if request.method == "GET":
        form.deposit.data = 0.0
        form.withdrawal.data = 0.0
    if form.validate_on_submit():
        id = current_user.id
        deposit = form.deposit.data
        withdrawal = form.withdrawal.data
        if User.update_balance(id, deposit, withdrawal):
            return redirect(url_for('myprofile.myprofile'))
    return render_template('balance.html', title='Update Balance', form=form)


@bp.route('/purchase_history', methods=['GET'])
def purchase_history():
    user_id = current_user.id

    # get all purchases
    purchases = Purchase.get_all_by_uid(user_id)

    if not purchases:
        return render_template('purchases.html', error=f"No purchases found for user ID {user_id}", user_id=user_id)

    return render_template('purchases.html', purchases=purchases, user_id=user_id)