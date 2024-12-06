'''
To Do:
-Need to create get_recent_feedback method to get 5 most recent 
feedback entries for given uid

Also add:
-A get method to obtain feedback entry based on product id
-Also create a method to get all entries for specific user 
(order from most recent to oldest)
'''


from flask import current_app as app

class Feedback:
    def __init__(self, id, pid, product_name, comment, rating, comment_time):
        self.id = id
        # self.uid = uid
        self.pid = pid
        self.product_name = product_name
        self.comment = comment
        self.rating = rating
        self.comment_time = comment_time

#     @staticmethod
#     def get(id):
#         rows = app.db.execute('''
# SELECT f.id, f.uid, f.pid, p.name AS product_name, f.comment, f.comment_time
# FROM Feedbacks f
# JOIN Products p ON f.pid = p.id
# WHERE f.id = :id
# ''',
#                               id=id)
#         return Feedback(*(rows[0])) if rows else None

    @staticmethod
    def get_recent_feedback(uid):
        rows = app.db.execute('''
SELECT 
    f.id AS "Feedback ID", 
    f.pid AS "Product ID", 
    p.name AS "Product Name", 
    f.comment AS "Comment", 
    f.rating AS "Rating",
    f.comment_time AS "Feedback Time"
FROM Feedbacks f
JOIN Products p ON f.pid = p.id
WHERE f.uid = :uid
ORDER BY f.comment_time DESC
LIMIT 5;
''',
                              uid=uid)
        return [Feedback(*row) for row in rows]

    @staticmethod
    def get_all_feedback(uid):
        rows = app.db.execute("""
SELECT 
    f.id AS "Feedback ID", 
    f.pid AS "Product ID", 
    p.name AS "Product Name", 
    f.comment AS "Comment", 
    f.rating AS "Rating",
    f.comment_time AS "Feedback Time"
FROM Feedbacks f
JOIN Products p ON f.pid = p.id
WHERE f.uid = :uid
ORDER BY f.comment_time DESC;
""",                        uid=uid)
        return [Feedback(*row) for row in rows]


    @staticmethod
    def submit_feedback(uid, pid, comment, rating):
        existing_feedback = app.db.execute(
            "SELECT id FROM Feedbacks WHERE uid = :uid AND pid = :pid",
            {'uid': uid, 'pid': pid}
        ).fetchone()

        if existing_feedback:
            app.db.execute(
                "UPDATE Feedbacks SET comment = :comment, rating = :rating, comment_time = CURRENT_TIMESTAMP WHERE id = :id",
                {'comment': comment, 'rating': rating, 'id': existing_feedback['id']}
            )
        else:
            app.db.execute(
                "INSERT INTO Feedbacks (uid, pid, comment, rating, comment_time) VALUES (:uid, :pid, :comment, :rating, CURRENT_TIMESTAMP)",
                {'uid': uid, 'pid': pid, 'comment': comment, 'rating': rating}
            )
    @staticmethod
    def update_feedback(feedback_id, uid, comment, rating):
        try:
            app.db.execute(
                "UPDATE Feedbacks SET comment = :comment, rating = :rating, comment_time = CURRENT_TIMESTAMP WHERE id = :id AND uid = :uid",
                {'id': feedback_id, 'uid': uid, 'comment': comment, 'rating': rating}
            )
            app.db.commit()
        except Exception as e:
            app.logger.error(f"Error updating review: {str(e)}")
            return False
        return True

    @staticmethod
    def delete_feedback(feedback_id, uid):
        try:
            app.db.execute(
                "DELETE FROM Feedbacks WHERE id = :id AND uid = :uid",
                {'id': feedback_id, 'uid': uid}
            )
            app.db.commit()
        except Exception as e:
            app.logger.error(f"Error deleting review: {str(e)}")
            return False
        return True