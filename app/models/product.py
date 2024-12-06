from flask import current_app as app


class Product:
    def __init__(self, id, name, price, quantity, description="", main_category="", sub_category="", ratings="", no_of_ratings="", image_url=""):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.description = description
        self.main_category = main_category
        self.sub_category = sub_category
        self.ratings = ratings
        self.no_of_ratings = no_of_ratings
        self.image_url = image_url
    
    @staticmethod
    def new_product(name, price, quantity, description, main_category, sub_category, image_url):
        query = '''
                INSERT INTO Products (name, price, quantity, description, main_category, sub_category, image_url)
                VALUES (:name, :price, :quantity, :description, :main_category, :sub_category, :image_url)
                ON CONFLICT (name) DO NOTHING
                RETURNING id
                '''
        new_id = app.db.execute(query, name=name, price=price, quantity=quantity, description=description, main_category=main_category, sub_category=sub_category,image_url=image_url)
        return new_id[0][0] if new_id else None
    
    def update_product_price(id, price):
        app.db.execute('''
                        UPDATE Products
                        SET price = :price
                        WHERE id = :id
                        ''', price = price, id = id)
        
    def update_product_quantity(id, quantity):
        app.db.execute('''
                        UPDATE Products
                        SET quantity = :quantity
                        WHERE id = :id
                        ''', quantity = quantity, id = id)
        app.db.execute('''
                        UPDATE Sells
                        SET quantity = :quantity
                        WHERE pid = :id
                        ''', quantity = quantity, id = id)
        
    def delete_product(id):
        app.db.execute('''
                        DELETE FROM Sells
                        WHERE pid = :id
                        ''', id = id)
        app.db.execute('''
                        DELETE FROM Cart
                        WHERE pid = :id
                        ''', id = id)
        app.db.execute('''
                        DELETE FROM Purchases
                        WHERE pid = :id
                        ''', id = id) # I understand this loses data, but storing records of deleted purchases would take up a whole new relation
        app.db.execute('''
                        DELETE FROM Feedbacks
                        WHERE pid = :id
                        ''', id = id)
        app.db.execute('''
                DELETE FROM Products
                WHERE id = :id
                ''', id = id)

    @staticmethod
    def get(id):
#         rows = app.db.execute('''
# SELECT id, name, price, available
# FROM Products
# WHERE id = :id
# ''',
#                               id=id)
        rows = app.db.execute('''
SELECT *
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
#         rows = app.db.execute('''
# SELECT id, name, price, available
# FROM Products
# WHERE available = :available
# ''',
#                               available=available)
        rows = app.db.execute('''
SELECT *
FROM Products
WHERE quantity > 0
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_top_k(k, all=False):
        if all:
            query = '''
                    SELECT * 
                    FROM Products
                    WHERE quantity > 0
                    ORDER BY price DESC
                    '''
        else:
            query = '''
                    SELECT * 
                    FROM Products
                    WHERE quantity > 0
                    ORDER BY price DESC
                    LIMIT :k
                    '''
        rows = app.db.execute(query, k=k)
        return [Product(*row) for row in rows]