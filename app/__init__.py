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

def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.DevConfig')

    # Initialize Plugins
    db.init_app(app)
    r.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    with app.app_context():
        # Include local applications routing
        from .authentication.home.routes import home_bp
        from .authentication.auth.routes import auth_bp
        from .authentication.user.routes import user_bp

        from .environment.simulator.routes import simulator_bp

        from .mechanisms.amm.routes import amm_bp

        from .interpreters.plotter.routes import plotter_bp

        ## Including satic asset handling
            ### ???
        # from .api import routes
        # from .assets import compile_static_assets

        # Register Blueprints
        app.register_blueprint(home_bp)
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(user_bp, url_prefix='/user')
        app.register_blueprint(simulator_bp, url_prefix='/simulator')
        app.register_blueprint(amm_bp, url_prefix='/amm')
        app.register_blueprint(plotter_bp, url_prefix='/plotter')

        # Create Database Models
        db.create_all()

        # Compile static assets
        # compile_static_assets(assets)  # Execute logic

        return app
