from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, address, balance):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.balance = balance

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname, address, balance
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname, address, balance):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, password, firstname, lastname, address, balance)
VALUES(:email, :password, :firstname, :lastname, :address, :balance)
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname, lastname=lastname,
                                  address=address,
                                  balance=balance)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname, address, balance
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None


    @staticmethod
    def update_profile(id, firstname, lastname, email, address, password):
        try:
            rows = app.db.execute("""
UPDATE Users
SET firstname = :firstname, lastname = :lastname, email = :email, address = :address, password = :password
WHERE id = :id
""",
                                 firstname = firstname,
                                 lastname = lastname,
                                 email = email,
                                 address = address,
                                 id = id,
                                 password=generate_password_hash(password))
            return User.get(id)
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def update_balance(id, deposit, withdrawal):
        rows1 = app.db.execute("""
SELECT balance
FROM Users
WHERE id = :id
""",
        id = id)
        balance1 = float(rows1[0][0])
        try:
            rows = app.db.execute("""
UPDATE Users
SET balance = :balance
WHERE id = :id
""",
                                id = id,
                                balance = balance1 + float(deposit) - float(withdrawal))
            return User.get(id)
        except Exception as e:
            print(str(e))
            return None
        
    @staticmethod
    def get_balance(id):
        try:
            rows = app.db.execute("""
            SELECT balance
            FROM Users
            WHERE id = :id
            """, id=id)
            return float(rows[0][0]) if rows else None
        except Exception as e:
            print(f"Error retrieving balance for user {id}: {str(e)}")
            return None

    @staticmethod
    def is_seller(id):
        rows = app.db.execute("""
SELECT id
FROM Sellers
WHERE id = :id
""",
                              id=id)
        return len(rows) > 0
    
    @staticmethod
    def add_seller(user_id):
        app.db.execute("""
                INSERT INTO Sellers(id)
                VALUES(:user_id)
                """, user_id=user_id)