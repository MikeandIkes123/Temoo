
from flask import current_app as app

class SFeedback:
    def __init__(self, id, sid, uid, comment, rating, comment_time):
        self.id = id
        # self.uid = uid
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
    sf.seller_id AS "Seller ID",
    s.name AS "Seller Name",
    sf.comment AS "Comment",
    sf.rating AS "Rating",
    sf.feedback_time AS "Feedback Time"
FROM SellerFeedbacks sf
JOIN Sellers s ON sf.seller_id = s.id
WHERE sf.uid = :uid
ORDER BY sf.feedback_time DESC
LIMIT 5;
''',
                              uid=uid)
        return [SFeedback(*row) for row in rows]