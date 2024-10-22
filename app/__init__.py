from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .purchaseSearch import bp as purchaseSearch_bp
    app.register_blueprint(purchaseSearch_bp)
    
    from .productSearch import bp as productSearch_bp
    app.register_blueprint(productSearch_bp)

    from .myprofile import bp as myprofile_bp
    app.register_blueprint(myprofile_bp)
    
    from .feedbackSearch import bp as feedbackSearch_bp
    app.register_blueprint(feedbackSearch_bp)
    
    from .sellerSearch import bp as sellerSearch_bp
    app.register_blueprint(sellerSearch_bp)

    from .carts import bp as cart_bp
    app.register_blueprint(cart_bp)

    return app
