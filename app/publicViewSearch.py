from flask import Blueprint, request, render_template
from .models.user import User
from .models.feedback import Feedback
from .models.sFeedback import SFeedback

bp = Blueprint('publicViewSearch', __name__)

@bp.route('/public_view', methods=['GET'])
def public_view():
    user_id = request.args.get('user_id')
    if not user_id:
        return render_template('public_view.html', error="No user ID provided", user_id=user_id)
    user = User.get_user(user_id)
    is_seller= User.is_seller(user_id)

    seller_reviews = []
    if is_seller:
        seller_reviews = SFeedback.get_reviews_of_seller(user_id)

    return render_template(
        'public_view.html',
        user=user,
        feedbacks=seller_reviews,
        is_seller=is_seller,
    )