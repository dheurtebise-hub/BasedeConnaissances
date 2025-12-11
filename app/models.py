"""Modèles de base de données pour KB Basedoc"""

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    """Charger un utilisateur par ID"""
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """Modèle utilisateur"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # Relations
    procedures = db.relationship('Procedure', backref='author', lazy='dynamic')

    def set_password(self, password):
        """Hash et définir le mot de passe"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Vérifier le mot de passe"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


class Category(db.Model):
    """Modèle catégorie"""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    short_name = db.Column(db.String(10), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    display_order = db.Column(db.Integer)
    color_code = db.Column(db.String(7))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    parent = db.relationship('Category', remote_side=[id], backref='children')
    procedures = db.relationship('Procedure', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'


class Tag(db.Model):
    """Modèle tag"""
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    usage_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Tag {self.name}>'


class Procedure(db.Model):
    """Modèle procédure"""
    __tablename__ = 'procedures'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    description = db.Column(db.Text)
    estimated_time = db.Column(db.Integer)  # en minutes
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_archived = db.Column(db.Boolean, default=False)

    # Relations
    attachments = db.relationship('Attachment', backref='procedure', lazy='dynamic', cascade='all, delete-orphan')
    versions = db.relationship('ProcedureVersion', backref='procedure', lazy='dynamic', cascade='all, delete-orphan')
    tags = db.relationship('Tag', secondary='procedure_tags', backref='procedures')

    def __repr__(self):
        return f'<Procedure {self.title}>'


# Table de liaison procédures-tags
procedure_tags = db.Table('procedure_tags',
    db.Column('procedure_id', db.Integer, db.ForeignKey('procedures.id', ondelete='CASCADE'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True),
    db.Column('is_ai_generated', db.Boolean, default=False),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)


class Attachment(db.Model):
    """Modèle fichier joint"""
    __tablename__ = 'attachments'

    id = db.Column(db.Integer, primary_key=True)
    procedure_id = db.Column(db.Integer, db.ForeignKey('procedures.id', ondelete='CASCADE'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    file_size = db.Column(db.BigInteger)
    storage_path = db.Column(db.String(500), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Attachment {self.original_filename}>'


class ProcedureVersion(db.Model):
    """Modèle version de procédure"""
    __tablename__ = 'procedure_versions'

    id = db.Column(db.Integer, primary_key=True)
    procedure_id = db.Column(db.Integer, db.ForeignKey('procedures.id', ondelete='CASCADE'), nullable=False)
    version_number = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    changed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    user = db.relationship('User')

    def __repr__(self):
        return f'<ProcedureVersion {self.procedure_id} v{self.version_number}>'


class Setting(db.Model):
    """Modèle configuration"""
    __tablename__ = 'settings'

    key = db.Column(db.String(100), primary_key=True)
    value = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Setting {self.key}>'
