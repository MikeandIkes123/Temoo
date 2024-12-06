
from flask import current_app as app

class SFeedback:
    def __init__(self, id, sid, uid, comment, rating, comment_time):
        self.id = id
        self.uid = uid
        self.sid = sid
        self.uid = uid
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
    def get_recent_sfeedback(uid):
        rows = app.db.execute('''
SELECT
    sf.id AS "Feedback ID",
    sf.sid AS "Seller ID",
    sf.uid AS "User ID",
    sf.comment AS "Comment",
    sf.rating AS "Rating",
    sf.comment_time AS "Feedback Time"
FROM sFeedbacks sf
JOIN Sellers s ON sf.sid = s.id
WHERE sf.uid = :uid
ORDER BY sf.comment_time DESC
LIMIT 5;
''',
                              uid=uid)
        return [SFeedback(*row) for row in rows]

    @staticmethod
    def get_sfeedback(uid):
        rows = app.db.execute('''
            SELECT
                sf.id AS "Feedback ID",
                sf.sid AS "Seller ID",
                sf.uid AS "User ID",
                sf.comment AS "Comment",
                sf.rating AS "Rating",
                sf.comment_time AS "Feedback Time"
            FROM sFeedbacks sf
            JOIN Sellers s ON sf.sid = s.id
            WHERE sf.uid = :uid
            ORDER BY sf.comment_time DESC;
            ''',
                uid=uid)
        return [SFeedback(*row) for row in rows]
    
    @staticmethod
    def get_reviews_of_seller(sid):
        rows = app.db.execute('''
            SELECT
                sf.id AS "Feedback ID",
                sf.sid AS "Seller ID",
                sf.uid AS "User ID",
                sf.comment AS "Comment",
                sf.rating AS "Rating",
                sf.comment_time AS "Feedback Time"
            FROM sFeedbacks sf
            JOIN Sellers s ON sf.sid = s.id
            WHERE sf.sid = :sid
            ORDER BY sf.comment_time DESC;
        ''',
            sid=sid)
        return [SFeedback(*row) for row in rows]


    @staticmethod
    def submit_feedback(uid, sid, comment, rating):
        try:
            # check if the user has bought soemthing from the seller 
            existing_purchase = app.db.execute(
                "SELECT id FROM Purchases WHERE uid = :uid AND sid = :sid", 
                uid = uid, sid = sid
            )

            if existing_purchase:
                existing_feedback = app.db.execute(
                    "SELECT id from sFeedbacks WHERE uid = :uid AND sid = :sid",
                    uid = uid, sid = sid
                )

                if existing_feedback: 
                    # update existing review
                    app.db.execute(
                        "UPDATE sFeedbacks SET comment = :comment, rating = :rating, comment_time = CURRENT_TIMESTAMP WHERE id = :id",
                        id = existing_feedback['id'], comment = comment, rating = rating
                    )
                else:
                    # insert new review
                    app.db.execute(
                        "INSERT INTO sFeedbacks (uid, sid, comment, rating, comment_time) VALUES (:uid, :sid, :comment, :rating, CURRENT_TIMESTAMP)",
                        uid = uid, sid = sid, comment = comment, rating = rating
                    )
                    print("Feedback submitted and inserted into DB")
                return True
            return False
        
        except Exception as e:
            app.logger.error(f"Error submitting feedback: {str(e)}")
            return False

    @staticmethod
    def update_feedback(feedback_id, uid, comment, rating):
        try:
            app.db.execute(
                "UPDATE sFeedbacks SET comment = :comment, rating = :rating, comment_time = CURRENT_TIMESTAMP WHERE id = :id AND uid = :uid",
                id = feedback_id, uid = uid, comment = comment, rating = rating
            )
    
        except Exception as e:
            app.logger.error(f"Error updating review: {str(e)}")
            return False
        return True


    @staticmethod
    def get_feedback(feedback_id):
        rows = app.db.execute("""
        SELECT 
            f.id AS "Feedback ID", 
            f.uid AS "User ID",
            f.sid AS "Seller ID",
            p.name AS "Product Name",
            f.comment AS "Comment", 
            f.rating AS "Rating",
            f.comment_time AS "Feedback Time"
        FROM Feedbacks f
        JOIN Products p ON f.pid = p.id
        WHERE f.id = :feedback_id
        """, feedback_id =  feedback_id)
        return [SFeedback(*row) for row in rows]

    @staticmethod
    def delete_feedback(review_id):
        query = '''
            DELETE FROM sFeedbacks
            WHERE id = :review_id
        '''
        app.db.execute(query, review_id = review_id)