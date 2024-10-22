from flask import current_app as app

class Cart:
    def __init__(self, user_id, product_id, quantity):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity

    @staticmethod
    def get_cart_items(user_id):
        query = '''
                SELECT pid, quantity
                FROM Cart
                WHERE uid = :user_id
                '''
        rows = app.db.execute(query, user_id=user_id)
        return [Cart(user_id, *row) for row in rows]
        
        
