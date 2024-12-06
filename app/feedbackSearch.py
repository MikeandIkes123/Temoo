'''
To Do:
-Use Blueprint to organize feedback routes
-Add route to get feedback through User ID
-fix up html
'''
from flask import Blueprint, request, redirect, url_for, render_template, flash
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

@bp.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    pid = request.form.get('product_id')
    comment = request.form.get('comment')
    rating = request.form.get('rating')

    if not pid or not comment or not rating:
        flash('All fields are required.', 'error')
        return redirect(url_for('productSearch.view_product', pid = pid))
    success = Feedback.submit_feedback(current_user.id, pid, comment, rating)
    if success:
        flash('Your review has been successfully posted!', 'success')
    else:
        flash('Error: review could not be posted.', 'error')
    return redirect(url_for('productSearch.view_protduct', pid = pid))

@bp.route('/edit_feedback/<int:feedback_id>', methods=['GET', 'POST'])
def edit_feedback(feedback_id):
    if request.method == 'POST':
        comment = request.form.get('comment')
        rating = request.form.get('rating')

        if not comment or not rating:
            flash('All fields are required.', 'error')
            return redirect(url_for('feedbackSearch.edit_feedback', feedback_id=feedback_id))
        
        Feedback.update_feedback(feedback_id, current_user.id, comment, rating)
        flash('Review updated successfully!', 'success')
        return redirect(url_for('feedbackSearch.search_feedback', user_id=current_user.id))
    
    feedback = Feedback.get_feedback(feedback_id)
    if not feedback or feedback['uid'] != current_user.id:
        flash('Unauthorized access.', 'error')
        return redirect(url_for('index.index'))
    
    return render_template('edit_feedback.html', feedback=feedback)

@bp.route('/delete_feedback/<int:feedback_id>', methods=['POST'])
def delete_feedback(feedback_id):
    Feedback.delete_feedback(feedback_id, current_user.id)
    flash('Review deleted successfully!', 'success')
    return redirect(url_for('feedbackSearch.search_feedback', user_id=current_user.id))
