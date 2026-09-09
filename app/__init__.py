from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import config

db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__, instance_relative_config=True)
    selected_config = config[config_name]
    app.config.from_object(selected_config)

    if hasattr(selected_config, 'validate'):
        selected_config.validate()

    db.init_app(app)

    # Register blueprints
    from .routes.main import main_bp
    from .routes.companies import companies_bp
    from .routes.applications import applications_bp
    from .routes.rounds import rounds_bp
    from .routes.export import export_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(companies_bp, url_prefix='/companies')
    app.register_blueprint(applications_bp, url_prefix='/applications')
    app.register_blueprint(rounds_bp, url_prefix='/rounds')
    app.register_blueprint(export_bp, url_prefix='/export')

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    return app