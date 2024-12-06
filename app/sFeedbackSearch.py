from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user
import datetime

from .models.user import User
from .models.sFeedback import SFeedback
from .models.product import Product

bp = Blueprint('sFeedbackSearch', __name__)

@bp.route('/search_sfeedback', methods=['GET'])
def search_sfeedback():
    user_id = request.args.get('user_id')
    if not user_id:
        return render_template('sfeedback.html', error="No user ID provided")

    # want to get 5 most recent feedback entries
    sfeedback_entries = SFeedback.get_recent_sfeedback(user_id)

    if not sfeedback_entries:
        return render_template('sfeedback.html', error=f"No reviews found for user ID {user_id}", user_id=user_id)

    return render_template('sfeedback.html', sfeedback_entries=sfeedback_entries, user_id=user_id)


@bp.route('/submit_sfeedback', methods=['POST'])
def submit_sfeedback():
    sid = request.form.get('seller_id')
    comment = request.form.get('comment')
    rating = request.form.get('rating')
    # if not (sid and comment and rating):
    #     return render_template('public_view.html', seller_id=sid, error="All fields are required.")
    success = SFeedback.submit_feedback(current_user.id, sid, comment, rating)
    return redirect(url_for('publicViewSearch.public_view', user_id=sid))

@bp.route('/edit_sfeedback_comment/', methods=['POST'])
def edit_scomment():
    review_id = request.form.get('review_id')
    curr_rating = request.form.get('curr_rating')
    new_comment = request.form.get('comment')
    seller_id = request.form.get('seller_id')
    SFeedback.update_feedback(review_id, current_user.id, new_comment, curr_rating)
    return redirect(url_for('publicViewSearch.public_view', user_id=seller_id))

@bp.route('/edit_sfeedback_rating/', methods=['POST'])
def edit_srating():
    review_id = request.form.get('review_id')
    curr_comment = request.form.get('curr_comment')
    new_rating = request.form.get('rating')
    seller_id = request.form.get('seller_id')
    SFeedback.update_feedback(review_id, current_user.id, curr_comment, new_rating)
    return redirect(url_for('publicViewSearch.public_view', user_id=seller_id))


@bp.route('/delete_sfeedback/', methods=['POST'])
def delete_sfeedback():
    review_id = request.form['review_id']
    seller_id = request.form.get('seller_id')
    SFeedback.delete_feedback(review_id)
    return redirect(url_for('publicViewSearch.public_view', user_id=seller_id))

