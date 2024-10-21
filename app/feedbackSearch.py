'''
To Do:
-Use Blueprint to organize feedback routes
-Add route to get feedback through User ID
-fix up html
'''
from flask import Blueprint, request, render_template
from flask_login import current_user
import datetime

from .models.user import User
from .models.feedback import Feedback

bp = Blueprint('feedbackSearch', __name__)

@bp.route('/search_feedback', methods=['GET'])
def search_feedback():
    user_id = request.args.get('user_id')
    if not user_id:
        return render_template('feedback.html', error="No user ID provided")

    # want to get 5 most recent feedback entries
    feedback_entries = Feedback.get_recent_feedback(user_id)

    if not feedback_entries:
        return render_template('feedback.html', error=f"No feedback found for user ID {user_id}", user_id=user_id)

    return render_template('feedback.html', feedback_entries=feedback_entries, user_id=user_id)

