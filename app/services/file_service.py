"""Service de gestion des fichiers uploadés"""

import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename):
    """Vérifie si le fichier est autorisé"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def save_uploaded_file(file, procedure_id):
    """
    Sauvegarde un fichier uploadé

    Args:
        file: Fichier uploadé (Werkzeug FileStorage)
        procedure_id: ID de la procédure

    Returns:
        dict avec les infos du fichier sauvegardé
    """

    if not file or not allowed_file(file.filename):
        raise ValueError('Type de fichier non autorisé')

    # Créer le dossier de destination
    upload_dir = os.path.join(
        current_app.config['UPLOAD_FOLDER'],
        'procedures',
        str(procedure_id)
    )
    os.makedirs(upload_dir, exist_ok=True)

    # Générer un nom de fichier sécurisé et unique
    original_filename = secure_filename(file.filename)
    file_extension = original_filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
    file_path = os.path.join(upload_dir, unique_filename)

    # Sauvegarder le fichier
    file.save(file_path)

    # Récupérer la taille
    file_size = os.path.getsize(file_path)

    return {
        'filename': unique_filename,
        'original_filename': original_filename,
        'file_type': file_extension,
        'file_size': file_size,
        'storage_path': file_path
    }


def delete_uploaded_file(file_path):
    """Supprimer un fichier uploadé"""
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False


def get_file_icon(file_type):
    """Retourne l'icône appropriée pour un type de fichier"""
    icons = {
        # Scripts
        'ps1': '💾',
        'sh': '💾',
        'bat': '💾',

        # Documents
        'pdf': '📄',
        'doc': '📄',
        'docx': '📄',

        # Images
        'png': '🖼️',
        'jpg': '🖼️',
        'jpeg': '🖼️',
        'gif': '🖼️',
        'webp': '🖼️',

        # Vidéos
        'mp4': '🎬',
        'avi': '🎬',
        'mov': '🎬',

        # Config
        'ini': '⚙️',
        'conf': '⚙️',
        'xml': '⚙️',
        'json': '⚙️',
        'txt': '⚙️',

        # Archives
        'zip': '📦',
        'rar': '📦',
    }

    return icons.get(file_type.lower(), '📎')
