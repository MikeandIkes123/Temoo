from flask import current_app as app
from app.models.user import User
from flask import flash, redirect, url_for


#I made adjustments on cart.py, carts.py, cart.html, and user.py. I also created an order confirmation page that displays the orders after submitting.
#The problem is that the current items dont have an order table, and im kinda reluctant to mess anything up

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
    
    @staticmethod
    def add_item(user_id, product_id, quantity):
        query = '''
            INSERT INTO Cart (uid, pid, quantity)
            VALUES (:user_id, :product_id, :quantity)
            ON CONFLICT (uid, pid) DO UPDATE 
            SET quantity = Cart.quantity + :quantity
        '''
        app.db.execute(query, user_id=user_id, product_id=product_id, quantity=quantity)


    @staticmethod
    def remove_item(user_id, product_id):
        query = '''
            DELETE FROM Cart
            WHERE uid = :user_id AND pid = :product_id
        '''
        app.db.execute(query, user_id=user_id, product_id=product_id)

    @staticmethod
    def clear_cart(user_id):
        query = '''
            DELETE FROM Cart
            WHERE uid = :user_id
        '''
        app.db.execute(query, user_id=user_id)

    @staticmethod
    def update_item(user_id, product_id, quantity):
        query = '''
            UPDATE Cart
            SET quantity = :quantity
            WHERE uid = :user_id AND pid = :product_id
        '''
        app.db.execute(query, user_id=user_id, product_id=product_id, quantity=quantity)

    @staticmethod
    def get_total_price(user_id):
        query = '''
            SELECT SUM(Cart.quantity * Products.price) AS total_price
            FROM Cart
            JOIN Products ON Cart.pid = Products.id
            WHERE Cart.uid = :user_id
        '''
        result = app.db.execute(query, user_id=user_id)
        
        # Check if result is not empty, then get the total_price by index
        total_price = result[0][0] if result else 0  # result[0][0] accesses the first value in the first row (total_price)
        
        return total_price
    
    @staticmethod
    def submit_cart(user_id):
        total_price = Cart.get_total_price(user_id)

        current_balance = User.get_balance(user_id)
        if current_balance < total_price:
            raise ValueError("Insufficient balance to complete the purchase")

        query_purchase = '''
            INSERT INTO Purchases (uid, pid, sid, time_purchased, quantity)
            SELECT Cart.uid, Cart.pid, Sells.uid AS sid, CURRENT_TIMESTAMP, Cart.quantity
            FROM Cart
            JOIN Sells ON Cart.pid = Sells.pid
            WHERE Cart.uid = :user_id
        '''
        app.db.execute(query_purchase, user_id=user_id)

        User.update_balance(user_id, 0, total_price)  # Assuming withdrawal only (no deposit)

        Cart.clear_cart(user_id)

        return total_price


