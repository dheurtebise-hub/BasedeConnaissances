"""Factory Flask pour KB Basedoc"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import config

# Extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()


def create_app(config_name='default'):
    """Factory pour créer l'application Flask"""

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialiser les extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Configuration Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
    login_manager.login_message_category = 'info'

    # Importer les modèles
    from app import models

    # Enregistrer les blueprints
    from app.routes import auth, procedures, search, admin, api

    app.register_blueprint(auth.bp)
    app.register_blueprint(procedures.bp)
    app.register_blueprint(search.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(api.bp)

    # Page d'accueil
    @app.route('/')
    def index():
        from flask import redirect, url_for
        from flask_login import current_user

        if current_user.is_authenticated:
            return redirect(url_for('procedures.home'))
        return redirect(url_for('auth.login'))

    return app
