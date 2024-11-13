from flask import Blueprint, request, render_template
from flask_login import current_user
import datetime

from .models.user import User
from .models.sFeedback import SFeedback

bp = Blueprint('SFeedbackSearch', __name__)

@bp.route('/search_sfeedback', methods=['GET'])
def search_sfeedback():
    user_id = request.args.get('user_id')
    if not user_id:
        return render_template('sfeedback.html', error="No user ID provided")

    # want to get 5 most recent feedback entries
    feedback_entries = SFeedback.get_recent_sfeedback(user_id)

    if not feedback_entries:
        return render_template('sfeedback.html', error=f"No reviews found for user ID {user_id}", user_id=user_id)

    return render_template('sfeedback.html', feedback_entries=feedback_entries, user_id=user_id)

