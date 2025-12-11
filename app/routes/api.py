"""API endpoints"""

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models import Procedure, Tag
from app.services.ai_service import generate_tags

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/procedures/<int:id>/autosave', methods=['POST'])
@login_required
def autosave(id):
    """Auto-save d'une procédure"""
    procedure = Procedure.query.get_or_404(id)

    data = request.get_json()
    if 'content' in data:
        procedure.content = data['content']
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Auto-saved'})

    return jsonify({'status': 'error', 'message': 'No content provided'}), 400


@bp.route('/tags/generate', methods=['POST'])
@login_required
def generate_tags_api():
    """Générer des tags avec IA"""
    data = request.get_json()
    title = data.get('title', '')
    content = data.get('content', '')

    if not title and not content:
        return jsonify({'error': 'Title or content required'}), 400

    try:
        tags = generate_tags(title, content)
        return jsonify({'tags': tags})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/categories/tree')
@login_required
def categories_tree():
    """Récupérer l'arborescence des catégories"""
    from app.models import Category

    def build_tree(parent_id=None):
        categories = Category.query.filter_by(parent_id=parent_id)\
            .order_by(Category.display_order).all()

        return [{
            'id': cat.id,
            'name': cat.name,
            'short_name': cat.short_name,
            'color_code': cat.color_code,
            'children': build_tree(cat.id)
        } for cat in categories]

    tree = build_tree()
    return jsonify(tree)
