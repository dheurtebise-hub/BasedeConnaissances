#!/usr/bin/env python3
"""Point d'entrée de l'application KB Basedoc"""

import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

from app import create_app, db
from app.models import User, Procedure, Category, Tag

# Créer l'application
app = create_app(os.getenv('FLASK_ENV') or 'development')

# Shell context pour flask shell
@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Procedure': Procedure,
        'Category': Category,
        'Tag': Tag
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
