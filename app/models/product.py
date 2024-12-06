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
    

    def get_category(cat, all=False):
        if all:
            query = '''
                    SELECT * 
                    FROM Products
                    WHERE quantity > 0
                    ORDER BY ratings DESC
                    LIMIT 100
                    '''
        else:
            query = f'''
                SELECT * 
                FROM Products
                WHERE main_category LIKE '%{cat}%'
                ORDER BY ratings DESC
                '''

        rows = app.db.execute(query, cat=cat)
        return [Product(*row) for row in rows]
    
    
    def get_keyword(word, all=False):
        if all:
            query = '''
                    SELECT * 
                    FROM Products
                    WHERE quantity > 0
                    ORDER BY ratings DESC
                    LIMIT 100
                    '''
        else:
            query = f'''
                SELECT * 
                FROM Products
                WHERE name LIKE '%{word}%'
                ORDER BY ratings DESC
                '''

        rows = app.db.execute(query, word=word)
        return [Product(*row) for row in rows]