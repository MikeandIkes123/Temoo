# from flask import current_app as app

# class Orders:
#     @staticmethod
#     def create_order(user_id, total_price):
#         # Insert order into Orders table
#         query = '''
#         INSERT INTO Orders (user_id, total_price, order_date)
#         VALUES (:user_id, :total_price, CURRENT_TIMESTAMP)
#         RETURNING id
#         '''
#         rows = app.db.execute(query, user_id=user_id, total_price=total_price)
#         return rows[0][0]  # Return the new order_id

#     @staticmethod
#     def add_order_item(order_id, product_id, quantity, unit_price):
#         # Insert order item into OrderItems table
#         query = '''
#         INSERT INTO OrderItems (order_id, product_id, quantity, unit_price)
#         VALUES (:order_id, :product_id, :quantity, :unit_price)
#         '''
#         app.db.execute(query, order_id=order_id, product_id=product_id, quantity=quantity, unit_price=unit_price)
