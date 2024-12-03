
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