from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_redis import FlaskRedis


# Globally accessible libraries
db = SQLAlchemy()
r = FlaskRedis()
migrate = Migrate()
login_manager = LoginManager()

# from routes.address_bp import address_bp
# app.register_blueprint(address_bp, url_prefix='/address')

def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.DevConfig')

    # Initialize Plugins
    # assets = Environment()  # Create an assets environment
    # assets.init_app(app)  # Initialize Flask-Assets
    db.init_app(app)
    r.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    with app.app_context():
        # Include our Routes
        from .home import routes
        from .auth import routes
        from .user import routes


        # from .api import routes
        # from .assets import compile_static_assets

        # Register Blueprints
        app.register_blueprint(home.routes.home_bp)
        app.register_blueprint(auth.routes.auth_bp, url_prefix='/auth')
        app.register_blueprint(user.routes.user_bp, url_prefix='/user')

        # Create Database Models
        db.create_all()

        # Compile static assets
        # compile_static_assets(assets)  # Execute logic

        return app
