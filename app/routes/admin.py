"""Routes d'administration"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models import User, Category, Procedure, Tag

bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Décorateur pour vérifier si l'utilisateur est admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Accès réservé aux administrateurs', 'error')
            return redirect(url_for('procedures.home'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/')
@login_required
@admin_required
def dashboard():
    """Tableau de bord admin"""
    stats = {
        'users_count': User.query.count(),
        'procedures_count': Procedure.query.filter_by(is_archived=False).count(),
        'categories_count': Category.query.count(),
        'tags_count': Tag.query.count()
    }

    return render_template('admin/dashboard.html', stats=stats)


@bp.route('/users')
@login_required
@admin_required
def users():
    """Gestion des utilisateurs"""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)


@bp.route('/users/new', methods=['GET', 'POST'])
@login_required
@admin_required
def user_new():
    """Créer un nouvel utilisateur"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        is_admin = request.form.get('is_admin') == 'on'

        # Vérifier si l'email existe déjà
        if User.query.filter_by(email=email).first():
            flash('Cet email est déjà utilisé', 'error')
            return redirect(url_for('admin.user_new'))

        # Créer l'utilisateur
        user = User(
            email=email,
            full_name=full_name,
            is_admin=is_admin
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash(f'Utilisateur {email} créé avec succès', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/user_edit.html', user=None)


@bp.route('/users/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def user_edit(id):
    """Éditer un utilisateur"""
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        user.email = request.form.get('email')
        user.full_name = request.form.get('full_name')
        user.is_admin = request.form.get('is_admin') == 'on'
        user.is_active = request.form.get('is_active') == 'on'

        # Changer le mot de passe si fourni
        password = request.form.get('password')
        if password:
            user.set_password(password)

        db.session.commit()

        flash(f'Utilisateur {user.email} mis à jour', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/user_edit.html', user=user)


@bp.route('/categories')
@login_required
@admin_required
def categories():
    """Gestion des catégories"""
    categories = Category.query.order_by(Category.display_order).all()
    return render_template('admin/categories.html', categories=categories)
