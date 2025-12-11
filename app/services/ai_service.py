"""Service d'intégration IA Claude pour génération de tags"""

import json
import os
from anthropic import Anthropic


def generate_tags(title, content, api_key=None):
    """
    Génère des tags pertinents via Claude API

    Args:
        title: Titre de la procédure
        content: Contenu de la procédure
        api_key: Clé API Claude (optionnel, utilise CLAUDE_API_KEY env si non fourni)

    Returns:
        Liste de tags suggérés
    """

    if not api_key:
        api_key = os.environ.get('CLAUDE_API_KEY')

    if not api_key:
        raise ValueError('CLAUDE_API_KEY not found')

    # Limiter le contenu pour réduire les coûts
    content_preview = content[:1000] if len(content) > 1000 else content

    prompt = f"""Tu es un assistant qui analyse des procédures IT.

Analyse ce titre et contenu de procédure.
Extrais 4 à 8 tags pertinents basés sur :
- Mots-clés récurrents (>3 occurrences)
- Termes techniques (logiciels, commandes)
- Actions principales (installation, configuration, dépannage)
- Contexte général

Titre : {title}
Contenu : {content_preview}

Retourne UNIQUEMENT un objet JSON :
{{"tags": ["tag1", "tag2", "tag3"]}}

Tags en minuscules, sans accents, avec tirets si composés.
Exemples : outlook, boite-partagee, powershell, exchange, vpn"""

    try:
        client = Anthropic(api_key=api_key)

        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parser la réponse JSON
        response_text = message.content[0].text.strip()

        # Trouver le JSON dans la réponse
        if '{' in response_text:
            json_start = response_text.index('{')
            json_end = response_text.rindex('}') + 1
            json_text = response_text[json_start:json_end]
            tags_data = json.loads(json_text)
            return tags_data.get('tags', [])

        return []

    except Exception as e:
        print(f"Erreur génération tags IA: {e}")
        return []


def semantic_search(query, procedures, api_key=None):
    """
    Recherche sémantique via Claude (Phase 3)

    Args:
        query: Question de l'utilisateur
        procedures: Liste des procédures à analyser
        api_key: Clé API Claude

    Returns:
        Liste de procédures triées par pertinence avec scores
    """

    if not api_key:
        api_key = os.environ.get('CLAUDE_API_KEY')

    if not api_key:
        raise ValueError('CLAUDE_API_KEY not found')

    client = Anthropic(api_key=api_key)
    results = []

    # Limiter le nombre de procédures analysées pour limiter les coûts
    for proc in procedures[:20]:
        content_preview = proc.content[:500] if len(proc.content) > 500 else proc.content

        prompt = f"""Question utilisateur : {query}

Titre procédure : {proc.title}
Contenu : {content_preview}

Cette procédure répond-elle à la question ?
Réponds par un score de 0 à 100 (uniquement le nombre)."""

        try:
            message = client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=50,
                messages=[{"role": "user", "content": prompt}]
            )

            score_text = message.content[0].text.strip()
            score = int(''.join(filter(str.isdigit, score_text)))

            if score > 50:
                results.append({
                    'procedure': proc,
                    'relevance': score
                })

        except Exception as e:
            print(f"Erreur analyse procédure {proc.id}: {e}")
            continue

    # Trier par pertinence
    results.sort(key=lambda x: x['relevance'], reverse=True)

    return results
