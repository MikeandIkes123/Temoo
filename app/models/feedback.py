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

#     @staticmethod
#     def get_all_feedback(uid):
#         rows = app.db.execute('''
# SELECT f.id, f.uid, f.pid, p.name AS product_name, f.comment, f.comment_time
# FROM Feedbacks f
# JOIN Products p ON f.pid = p.id
# WHERE f.uid = :uid
# ORDER BY f.comment_time DESC
# ''',
#                               uid=uid)
#         return [Feedback(*row) for row in rows]
