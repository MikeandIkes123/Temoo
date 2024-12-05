from flask import current_app as app

class Purchase:
    def __init__(self, id, uid, pid, sid, time_purchased, quantity):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.sid = sid  # Added sid
        self.time_purchased = time_purchased
        self.quantity = quantity

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, sid, time_purchased, quantity
FROM Purchases
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, pid, sid, time_purchased, quantity
FROM Purchases
WHERE uid = :uid
AND time_purchased >= :since
ORDER BY time_purchased DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]
    
    @staticmethod
    def get_all_by_uid(uid):
        rows = app.db.execute('''
SELECT id, uid, pid, sid, time_purchased, quantity
FROM Purchases
WHERE uid = :uid
ORDER BY time_purchased DESC
''',
                              uid=uid)
        return [Purchase(*row) for row in rows]
    
    @staticmethod
    def add_purchase(user_id, product_id, seller_id, quantity, time_purchased):
        query = '''
            INSERT INTO Purchases (uid, pid, sid, quantity, time_purchased)
            VALUES (:user_id, :product_id, :seller_id, :quantity, :time_purchased)
        '''
        app.db.execute(query, user_id=user_id, product_id=product_id, seller_id=seller_id, quantity=quantity, time_purchased=time_purchased)
