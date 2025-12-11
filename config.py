import os
from datetime import timedelta

class Config:
    """Configuration de base pour l'application KB Basedoc"""

    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://kb_user:kb_password@localhost/kb_basedoc'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Upload
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or '/var/www/kb_basedoc/storage'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB
    ALLOWED_EXTENSIONS = {
        'ps1', 'sh', 'bat',
        'pdf', 'doc', 'docx',
        'png', 'jpg', 'jpeg', 'gif', 'webp',
        'mp4', 'avi', 'mov',
        'ini', 'conf', 'xml', 'json', 'txt',
        'zip', 'rar'
    }

    # Session
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False') == 'True'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

    # Claude API
    CLAUDE_API_KEY = os.environ.get('CLAUDE_API_KEY')
    CLAUDE_MODEL = 'claude-sonnet-4-5-20250929'

    # Application
    APP_NAME = 'KB Support Basedoc'
    COMPANY_NAME = 'Support IT - Gagneraud'

    # Flask config
    JSON_AS_ASCII = False  # Support UTF-8


class DevelopmentConfig(Config):
    """Configuration pour développement"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Configuration pour production"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
