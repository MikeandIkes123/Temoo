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
from .models.product import Product

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




# @bp.route('/submit_feedback', methods=['POST'])
# def submit_feedback():
#     pid = request.form.get('product_id')
#     comment = request.form.get('comment')
#     rating = request.form.get('rating')

#     if (not pid) or not comment or not rating:
#         flash('All fields are required.', 'error')
#         return redirect(url_for('productSearch.product_details', product_id = pid))
#     success = Feedback.submit_feedback(current_user.id, pid, comment, rating)
#     if success:
#         flash('Your review has been successfully posted!', 'success')
#     else:
#         flash('Error: review could not be posted.', 'error')
#     return redirect(url_for('productSearch.product_details', product_id = pid))

@bp.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    pid = request.form.get('product_id')
    comment = request.form.get('comment')
    rating = request.form.get('rating')

    if not (pid and comment and rating):
        return render_template('product_details.html', product_id=pid, error="All fields are required.")

    success = Feedback.submit_feedback(current_user.id, pid, comment, rating)
    if success:
        message = 'Your review has been successfully posted!'
    else:
        message = 'Error: review could not be posted.'

    # get updated list of reviews for product to display on detailed prod page
    feedbacks = Feedback.get_feedback_by_product(pid)
    product = Product.get(pid) 
    print(current_user.id)
    return render_template('product_details.html', product=product, current_user = current_user.id, feedbacks=feedbacks, message=message)

@bp.route('/edit_feedback_comment/', methods=['POST'])
def edit_comment():
    review_id = request.form.get('review_id')
    curr_rating = request.form.get('curr_rating')
    new_comment = request.form.get('comment')
    product_id = request.form.get('product_id')
    Feedback.update_feedback(review_id, current_user.id, new_comment, curr_rating)
    return redirect(url_for('productSearch.product_details', product_id=product_id))

@bp.route('/edit_feedback_rating/', methods=['POST'])
def edit_rating():
    review_id = request.form.get('review_id')
    curr_comment = request.form.get('curr_comment')
    new_rating = request.form.get('rating')
    product_id = request.form.get('product_id')
    Feedback.update_feedback(review_id, current_user.id, curr_comment, new_rating)
    return redirect(url_for('productSearch.product_details', product_id=product_id))




    # if request.method == 'POST':
    #     comment = request.form.get('comment')
    #     rating = request.form.get('rating')

    #     if not (comment and rating):
    #         error_message = 'All fields are required.'
    #         feedback = Feedback.get_feedback(feedback_id)
    #         return render_template('edit_feedback.html', feedback=feedback, error=error_message)

    #     success = Feedback.update_feedback(feedback_id, current_user.id, comment, rating)
    #     if success:
    #         message = 'Review updated successfully!'
    #     else:
    #         message = 'Error updating review.'

    #     return redirect(url_for('feedbackSearch.my_reviews', message=message))

    # feedback = Feedback.get_feedback(feedback_id)
    # if not feedback or feedback.uid != current_user.id:
    #     return render_template('unauthorized.html', error='Unauthorized access.')

    # return render_template('edit_feedback.html', feedback=feedback)

@bp.route('/delete_feedback/', methods=['POST'])
def delete_feedback():
    product_id = request.form['product_id']
    user_id = current_user.id  
    Feedback.delete_feedback(user_id, product_id)
    return redirect(url_for('productSearch.product_details', product_id=product_id))
