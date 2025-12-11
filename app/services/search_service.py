"""Service de recherche"""

from app.models import Procedure
from sqlalchemy import or_


def simple_search(query, limit=50):
    """
    Recherche simple par mots-clés

    Args:
        query: Terme de recherche
        limit: Nombre maximum de résultats

    Returns:
        Liste de procédures correspondantes
    """

    if not query or len(query) < 2:
        return []

    search_term = f'%{query}%'

    results = Procedure.query.filter(
        or_(
            Procedure.title.ilike(search_term),
            Procedure.content.ilike(search_term),
            Procedure.description.ilike(search_term)
        )
    ).filter_by(is_archived=False)\
     .order_by(Procedure.updated_at.desc())\
     .limit(limit)\
     .all()

    return results


def calculate_relevance(procedure, query):
    """
    Calcule un score de pertinence simple

    Args:
        procedure: Procédure à analyser
        query: Terme de recherche

    Returns:
        Score de pertinence (0-100)
    """

    score = 0
    query_lower = query.lower()

    # Titre exact
    if query_lower == procedure.title.lower():
        score += 50

    # Titre contient le terme
    elif query_lower in procedure.title.lower():
        score += 30

    # Contenu contient le terme
    if query_lower in procedure.content.lower():
        score += 20

    # Description contient le terme
    if procedure.description and query_lower in procedure.description.lower():
        score += 10

    return min(score, 100)


def search_by_category(category_id, archived=False):
    """
    Recherche par catégorie

    Args:
        category_id: ID de la catégorie
        archived: Inclure les procédures archivées

    Returns:
        Liste de procédures de cette catégorie
    """

    query = Procedure.query.filter_by(category_id=category_id)

    if not archived:
        query = query.filter_by(is_archived=False)

    return query.order_by(Procedure.updated_at.desc()).all()
