"""Routes pour les procédures"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Procedure, Category, Tag
from datetime import datetime

bp = Blueprint('procedures', __name__, url_prefix='/procedures')


@bp.route('/home')
@login_required
def home():
    """Page d'accueil"""
    # Récupérer les procédures récentes
    recent_procedures = Procedure.query.filter_by(is_archived=False)\
        .order_by(Procedure.updated_at.desc())\
        .limit(10)\
        .all()

    # Récupérer les catégories principales
    categories = Category.query.filter_by(parent_id=None)\
        .order_by(Category.display_order)\
        .all()

    return render_template('procedures/home.html',
                         recent_procedures=recent_procedures,
                         categories=categories)


@bp.route('/list')
@login_required
def list():
    """Liste des procédures"""
    category_id = request.args.get('category', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = 20

    query = Procedure.query.filter_by(is_archived=False)

    if category_id:
        query = query.filter_by(category_id=category_id)

    procedures = query.order_by(Procedure.updated_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    categories = Category.query.filter_by(parent_id=None)\
        .order_by(Category.display_order)\
        .all()

    return render_template('procedures/list.html',
                         procedures=procedures,
                         categories=categories,
                         selected_category=category_id)


@bp.route('/<int:id>')
@login_required
def detail(id):
    """Détail d'une procédure"""
    procedure = Procedure.query.get_or_404(id)

    return render_template('procedures/detail.html', procedure=procedure)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    """Créer une nouvelle procédure"""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category_id = request.form.get('category_id', type=int)
        description = request.form.get('description')
        estimated_time = request.form.get('estimated_time', type=int)
        tags_str = request.form.get('tags', '')

        # Validation
        if not title or not content or not category_id:
            flash('Le titre, le contenu et la catégorie sont obligatoires', 'error')
            return redirect(url_for('procedures.new'))

        # Créer la procédure
        procedure = Procedure(
            title=title,
            content=content,
            category_id=category_id,
            description=description,
            estimated_time=estimated_time,
            created_by=current_user.id
        )

        # Traiter les tags
        if tags_str:
            tag_names = [t.strip().lower() for t in tags_str.split(',') if t.strip()]
            for tag_name in tag_names:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                procedure.tags.append(tag)
                tag.usage_count += 1

        db.session.add(procedure)
        db.session.commit()

        flash('Procédure créée avec succès', 'success')
        return redirect(url_for('procedures.detail', id=procedure.id))

    # GET - afficher le formulaire
    categories = Category.query.order_by(Category.display_order).all()
    return render_template('procedures/edit.html',
                         procedure=None,
                         categories=categories)


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Éditer une procédure"""
    procedure = Procedure.query.get_or_404(id)

    if request.method == 'POST':
        procedure.title = request.form.get('title')
        procedure.content = request.form.get('content')
        procedure.category_id = request.form.get('category_id', type=int)
        procedure.description = request.form.get('description')
        procedure.estimated_time = request.form.get('estimated_time', type=int)
        procedure.updated_at = datetime.utcnow()

        # Mettre à jour les tags
        tags_str = request.form.get('tags', '')
        procedure.tags.clear()

        if tags_str:
            tag_names = [t.strip().lower() for t in tags_str.split(',') if t.strip()]
            for tag_name in tag_names:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                procedure.tags.append(tag)
                tag.usage_count += 1

        db.session.commit()

        flash('Procédure mise à jour avec succès', 'success')
        return redirect(url_for('procedures.detail', id=procedure.id))

    # GET - afficher le formulaire
    categories = Category.query.order_by(Category.display_order).all()
    tags_str = ', '.join([tag.name for tag in procedure.tags])

    return render_template('procedures/edit.html',
                         procedure=procedure,
                         categories=categories,
                         tags_str=tags_str)


@bp.route('/<int:id>/archive', methods=['POST'])
@login_required
def archive(id):
    """Archiver une procédure"""
    procedure = Procedure.query.get_or_404(id)
    procedure.is_archived = True
    db.session.commit()

    flash('Procédure archivée', 'success')
    return redirect(url_for('procedures.list'))


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """Supprimer une procédure (admin uniquement)"""
    if not current_user.is_admin:
        flash('Action non autorisée', 'error')
        return redirect(url_for('procedures.detail', id=id))

    procedure = Procedure.query.get_or_404(id)
    db.session.delete(procedure)
    db.session.commit()

    flash('Procédure supprimée', 'success')
    return redirect(url_for('procedures.list'))
