#!/usr/bin/env python3
"""Script pour initialiser les données de base (catégories et admin)"""

import os
from app import create_app, db
from app.models import User, Category

def seed_database():
    """Initialiser les données de base"""

    app = create_app('development')

    with app.app_context():
        print("Initialisation de la base de données...")

        # Créer toutes les tables
        db.create_all()

        # Vérifier si des catégories existent déjà
        if Category.query.count() > 0:
            print("Les catégories existent déjà. Nettoyage...")
            Category.query.delete()
            db.session.commit()

        # Créer les catégories principales et sous-catégories
        categories_data = [
            {
                'name': 'Office 365',
                'short_name': 'o365',
                'color_code': '#06b6d4',
                'display_order': 1,
                'children': [
                    {'name': 'Outlook', 'short_name': 'out'},
                    {'name': 'Teams', 'short_name': 'team'},
                    {'name': 'OneDrive', 'short_name': 'one'},
                    {'name': 'SharePoint', 'short_name': 'share'},
                    {'name': 'Exchange', 'short_name': 'exch'},
                ]
            },
            {
                'name': 'Matériel',
                'short_name': 'hard',
                'color_code': '#f97316',
                'display_order': 2,
                'children': [
                    {'name': 'Ordinateurs', 'short_name': 'pc'},
                    {'name': 'Imprimantes', 'short_name': 'print'},
                    {'name': 'Périphériques', 'short_name': 'periph'},
                    {'name': 'Téléphonie', 'short_name': 'phone'},
                ]
            },
            {
                'name': 'Réseau',
                'short_name': 'net',
                'color_code': '#10b981',
                'display_order': 3,
                'children': [
                    {'name': 'VPN', 'short_name': 'vpn'},
                    {'name': 'Wi-Fi', 'short_name': 'wifi'},
                    {'name': 'Partages réseau', 'short_name': 'share'},
                    {'name': 'Accès distant', 'short_name': 'remote'},
                ]
            },
            {
                'name': 'Comptes et accès',
                'short_name': 'acct',
                'color_code': '#fbbf24',
                'display_order': 4,
                'children': [
                    {'name': 'Active Directory', 'short_name': 'ad'},
                    {'name': 'Création comptes', 'short_name': 'create'},
                    {'name': 'Reset passwords', 'short_name': 'reset'},
                    {'name': 'Permissions', 'short_name': 'perms'},
                ]
            },
            {
                'name': 'Logiciels',
                'short_name': 'soft',
                'color_code': '#8b5cf6',
                'display_order': 5,
                'children': [
                    {'name': 'Installation', 'short_name': 'inst'},
                    {'name': 'Désinstallation', 'short_name': 'uninst'},
                    {'name': 'Mises à jour', 'short_name': 'update'},
                    {'name': 'Licences', 'short_name': 'lic'},
                    {'name': 'Maintenance', 'short_name': 'maint'},
                ]
            },
            {
                'name': 'Système',
                'short_name': 'sys',
                'color_code': '#ef4444',
                'display_order': 6,
                'children': [
                    {'name': 'Windows 10/11', 'short_name': 'win'},
                    {'name': 'PowerShell', 'short_name': 'ps'},
                    {'name': 'GPO', 'short_name': 'gpo'},
                    {'name': 'Sauvegardes', 'short_name': 'backup'},
                ]
            },
        ]

        print("Création des catégories...")

        for cat_data in categories_data:
            # Créer la catégorie parent
            parent = Category(
                name=cat_data['name'],
                short_name=cat_data['short_name'],
                color_code=cat_data['color_code'],
                display_order=cat_data['display_order']
            )
            db.session.add(parent)
            db.session.flush()  # Pour obtenir l'ID

            # Créer les sous-catégories
            for i, child_data in enumerate(cat_data['children']):
                child = Category(
                    name=child_data['name'],
                    short_name=child_data['short_name'],
                    parent_id=parent.id,
                    color_code=cat_data['color_code'],
                    display_order=i + 1
                )
                db.session.add(child)

            print(f"  ✓ {cat_data['name']} ({len(cat_data['children'])} sous-catégories)")

        db.session.commit()
        print(f"Total: {Category.query.count()} catégories créées")

        # Créer l'utilisateur admin si nécessaire
        admin_email = os.environ.get('ADMIN_EMAIL', 'dheurtebise@basedoc.fr')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'Admin123!')

        if not User.query.filter_by(email=admin_email).first():
            print(f"\nCréation de l'utilisateur admin: {admin_email}")

            admin = User(
                email=admin_email,
                full_name='David Heurtebise',
                is_admin=True,
                is_active=True
            )
            admin.set_password(admin_password)

            db.session.add(admin)
            db.session.commit()

            print(f"  ✓ Admin créé")
            print(f"  Email: {admin_email}")
            print(f"  Mot de passe: {admin_password}")
            print("\n  ⚠️  CHANGEZ LE MOT DE PASSE APRÈS LA PREMIÈRE CONNEXION!")
        else:
            print(f"\nL'utilisateur admin existe déjà: {admin_email}")

        print("\n✅ Base de données initialisée avec succès!")


if __name__ == '__main__':
    seed_database()
