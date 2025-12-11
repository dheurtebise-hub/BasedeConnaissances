"""Routes de recherche"""

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app.models import Procedure, Tag
from sqlalchemy import or_

bp = Blueprint('search', __name__, url_prefix='/search')


@bp.route('/')
@login_required
def search():
    """Page de recherche"""
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = 20

    if not query:
        return render_template('search/results.html', procedures=None, query='')

    # Recherche simple par mots-clés
    search_term = f'%{query}%'
    results = Procedure.query.filter(
        or_(
            Procedure.title.ilike(search_term),
            Procedure.content.ilike(search_term),
            Procedure.description.ilike(search_term)
        )
    ).filter_by(is_archived=False)\
     .order_by(Procedure.updated_at.desc())\
     .paginate(page=page, per_page=per_page, error_out=False)

    return render_template('search/results.html',
                         procedures=results,
                         query=query)


@bp.route('/suggestions')
@login_required
def suggestions():
    """API de suggestions pour l'auto-complétion"""
    query = request.args.get('q', '')

    if len(query) < 3:
        return jsonify([])

    search_term = f'%{query}%'
    results = Procedure.query.filter(
        or_(
            Procedure.title.ilike(search_term),
            Procedure.content.ilike(search_term)
        )
    ).filter_by(is_archived=False)\
     .limit(10)\
     .all()

    suggestions = [{
        'id': p.id,
        'title': p.title,
        'category': p.category.name if p.category else '',
        'description': p.description or ''
    } for p in results]

    return jsonify(suggestions)


@bp.route('/tags')
@login_required
def search_tags():
    """Recherche par tags"""
    tag_name = request.args.get('tag', '')

    if not tag_name:
        return render_template('search/results.html', procedures=None, query='')

    tag = Tag.query.filter_by(name=tag_name.lower()).first()

    if not tag:
        return render_template('search/results.html', procedures=[], query=tag_name)

    procedures = [p for p in tag.procedures if not p.is_archived]

    return render_template('search/results.html',
                         procedures=procedures,
                         query=f'Tag: {tag_name}')
