from flask import current_app as app
from flask_login import current_user

from .product import Product


class Sells:
    def __init__(self, uid, pid, quantity=0): # Bernie added quantity
        self.uid = uid # user id that sells it 
        self.pid = pid # product id that is being sold 
            
        # Bernie added
        self.quantity = quantity
    @staticmethod
    def get_inventory_by_seller(uid):
        rows = app.db.execute('''
                            SELECT pid, name, price, p.quantity, description, main_category, sub_category, ratings, no_of_ratings, image_url
                            FROM Sells s, Products p
                            WHERE s.uid = :uid 
                            AND s.pid = p.id
                            ''', uid = uid )
        return [Product(*row) for row in rows] if rows else None
    
    def add_product(uid, pid, quantity):
        app.db.execute('''
                        INSERT INTO Sells (uid, pid, quantity)
                        VALUES (:uid, :pid, :quantity)
                        ON CONFLICT (uid, pid) DO NOTHING
                        ''', uid = uid, pid = pid, quantity = quantity)

    def update_item(product):
        app.db.execute('''
                        UPDATE Sells
                        SET quantity = :quantity
                        WHERE uid = :uid AND pid = :pid
                        ''', uid = product.uid, pid = product.pid, quantity = product.quantity)
    # TODO: 
    def get_seller_from_product(pid):
        rows = app.db.execute('''
                            SELECT uid, pid, quantity
                            FROM Sells
                            WHERE pid = :pid
                            ''', pid = pid)
        # return Product(*(rows[0])) if rows else None
        return [Sells(*row) for row in rows] if rows else None
