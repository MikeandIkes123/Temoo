from flask import current_app as app

from .product import Product


class Sells:
    def __init__(self, uid, pid):
        self.uid = uid # user id that sells it 
        self.pid = pid # product id that is being sold 

    # @staticmethod 
    # def get_sells_by_seller(uid):
    #     rows = app.db.execute('''
    #                         SELECT uid, pid
    #                         FROM Sells
    #                         WHERE uid = :uid
    #                         ''')
    #     return Sells(*(rows[0])) if rows else None
    
    #TODO - could probably move this somewhere else 
    @staticmethod
    def get_inventory_by_seller(uid):
        rows = app.db.execute('''
                            SELECT pid, name, price, available
                            FROM Sells s, Products p
                            WHERE s.uid = :uid 
                            AND s.pid = p.id
                            ''', uid = uid )
        return [Product(*row) for row in rows] if rows else None

    # TODO: 
    # def get_seller_from_product(pid):
    #     rows = app.db.execute('''
    #                         SELECT uid
    #                         FROM Sells
    #                         WHERE pid = :pid
    #                         ''')
    #     return Product(*(rows[0])) if rows else None
