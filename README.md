# KB Support Basedoc - Base de Connaissances IT

Application web de gestion de procédures pour le service IT de Gagneraud.

## 🎯 Caractéristiques

- **Interface Dark Theme** - Style technique/terminal
- **Authentification sécurisée** - Flask-Login avec bcrypt
- **CRUD Procédures** - Création, édition, recherche de procédures
- **Catégorisation avancée** - Arborescence de catégories dépliable
- **Tags intelligents** - Génération automatique via IA Claude (optionnel)
- **Recherche** - Recherche par mots-clés avec auto-complétion
- **Upload fichiers** - Support multiples formats (scripts, docs, images, vidéos)
- **Versioning** - Historique des modifications
- **Administration** - Gestion utilisateurs et catégories

## 🛠️ Stack Technique

- **Backend**: Python 3.12 / Flask
- **Base de données**: PostgreSQL 16
- **Serveur web**: Nginx + Gunicorn
- **SSL**: Let's Encrypt (Certbot)
- **IA**: API Claude Anthropic (Sonnet 4.5) - optionnel
- **Auth**: Flask-Login (sessions sécurisées)

## 📋 Prérequis

- Ubuntu 24.04 LTS (ou similaire)
- Python 3.12+
- PostgreSQL 16+
- Nginx
- Accès root/sudo

## 🚀 Installation Automatique (Production)

### 1. Cloner le projet

```bash
git clone <repository-url>
cd BasedeConnaissances
```

### 2. Rendre le script exécutable

```bash
chmod +x install.sh
```

### 3. Exécuter le script d'installation

```bash
sudo ./install.sh
```

Le script va:
- Installer tous les prérequis (Python, PostgreSQL, Nginx)
- Créer la base de données
- Configurer l'application
- Initialiser les données (catégories + admin)
- Configurer Nginx et systemd
- Démarrer l'application

### 4. Configurer SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d gagneraud.basedoc.fr
```

### 5. Configurer la clé API Claude (optionnel)

Éditer le fichier `.env`:

```bash
sudo nano /var/www/kb_basedoc/.env
```

Ajouter:

```
CLAUDE_API_KEY=your-claude-api-key-here
```

Redémarrer l'application:

```bash
sudo systemctl restart kb_basedoc
```

## 🔧 Installation Manuelle (Développement)

### 1. Installer les dépendances système

```bash
sudo apt update
sudo apt install python3.12 python3.12-venv postgresql libpq-dev
```

### 2. Créer la base de données

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE kb_basedoc;
CREATE USER kb_user WITH PASSWORD 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON DATABASE kb_basedoc TO kb_user;
\q
```

### 3. Créer l'environnement virtuel

```bash
python3.12 -m venv venv
source venv/bin/activate
```

### 4. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

### 5. Configurer les variables d'environnement

Créer un fichier `.env`:

```bash
cp .env.example .env
```

Éditer `.env` avec vos configurations:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://kb_user:password@localhost/kb_basedoc
UPLOAD_FOLDER=./storage
CLAUDE_API_KEY=your-claude-api-key  # optionnel
```

### 6. Initialiser la base de données

```bash
python seed_data.py
```

### 7. Lancer l'application en développement

```bash
python run.py
```

L'application sera accessible sur `http://localhost:5000`

## 👤 Connexion Admin par défaut

- **Email**: dheurtebise@basedoc.fr
- **Mot de passe**: Admin123!

⚠️ **IMPORTANT**: Changez ce mot de passe immédiatement après la première connexion!

## 📁 Structure du Projet

```
BasedeConnaissances/
├── app/
│   ├── __init__.py          # Factory Flask
│   ├── models.py            # Modèles SQLAlchemy
│   ├── routes/              # Routes (blueprints)
│   │   ├── auth.py
│   │   ├── procedures.py
│   │   ├── search.py
│   │   ├── admin.py
│   │   └── api.py
│   ├── services/            # Services métier
│   │   ├── ai_service.py
│   │   ├── file_service.py
│   │   └── search_service.py
│   ├── templates/           # Templates Jinja2
│   └── static/              # CSS, JS, fonts
├── storage/                 # Fichiers uploadés
├── config.py               # Configuration
├── requirements.txt        # Dépendances Python
├── run.py                  # Point d'entrée
├── seed_data.py           # Script d'initialisation
├── gunicorn_config.py     # Config Gunicorn
└── install.sh             # Script d'installation
```

## 🎨 Design System

### Couleurs

- **Backgrounds**: `#1f2937`, `#111827`, `#374151`, `#4b5563`
- **Textes**: `#f9fafb`, `#9ca3af`, `#6b7280`
- **Accents**: Cyan `#06b6d4`, Orange `#f97316`, Green `#10b981`

### Catégories

- 📧 **Office 365** - Cyan `#06b6d4`
- 🖥️ **Matériel** - Orange `#f97316`
- 🌐 **Réseau** - Green `#10b981`
- 👤 **Comptes et accès** - Yellow `#fbbf24`
- 💾 **Logiciels** - Purple `#8b5cf6`
- ⚙️ **Système** - Red `#ef4444`

## 🔒 Sécurité

- ✅ Mots de passe hashés avec bcrypt
- ✅ Protection CSRF (Flask-WTF)
- ✅ Sessions sécurisées (HTTPOnly, Secure, SameSite)
- ✅ Validation des uploads (type MIME)
- ✅ Limite taille fichiers (50 MB)

## 📝 Utilisation

### Créer une procédure

1. Cliquer sur **+ NEW**
2. Remplir le formulaire:
   - Titre (obligatoire)
   - Catégorie (obligatoire)
   - Durée estimée (optionnel)
   - Description (optionnel)
   - Tags (manuels ou générés par IA)
3. Rédiger le contenu en Markdown
4. **Enregistrer**

### Génération de tags avec IA

1. Remplir le titre et le contenu
2. Cliquer sur **🤖 Générer avec IA**
3. L'IA Claude analysera le contenu et suggérera des tags pertinents

**Note**: Requiert une clé API Claude configurée dans `.env`

### Rechercher une procédure

- **Barre de recherche** (header): Auto-complétion en temps réel
- **Filtrer par catégorie**: Utiliser la sidebar
- **Recherche par tag**: Cliquer sur un tag dans une procédure

## 🔧 Commandes Utiles

### Production

```bash
# Redémarrer l'application
sudo systemctl restart kb_basedoc

# Voir le statut
sudo systemctl status kb_basedoc

# Voir les logs
sudo journalctl -u kb_basedoc -f

# Logs Nginx
sudo tail -f /var/log/nginx/kb_basedoc_error.log

# Logs Gunicorn
sudo tail -f /var/log/gunicorn/error.log
```

### Développement

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Lancer en mode debug
FLASK_ENV=development python run.py

# Réinitialiser la base de données
python seed_data.py
```

## 📦 Backup

### Base de données

```bash
# Backup
sudo -u postgres pg_dump kb_basedoc > backup_$(date +%Y%m%d).sql

# Restore
sudo -u postgres psql kb_basedoc < backup_20240101.sql
```

### Fichiers uploadés

```bash
# Backup
tar -czf storage_backup_$(date +%Y%m%d).tar.gz /var/www/kb_basedoc/storage/

# Restore
tar -xzf storage_backup_20240101.tar.gz -C /var/www/kb_basedoc/
```

## 🐛 Dépannage

### L'application ne démarre pas

```bash
# Vérifier les logs
sudo journalctl -u kb_basedoc -n 50

# Vérifier la config Gunicorn
sudo -u www-data /var/www/kb_basedoc/venv/bin/gunicorn --check-config gunicorn_config.py
```

### Erreur de connexion à la base de données

```bash
# Vérifier PostgreSQL
sudo systemctl status postgresql

# Tester la connexion
psql -U kb_user -d kb_basedoc -h localhost
```

### Problème de permissions

```bash
# Réparer les permissions
sudo chown -R www-data:www-data /var/www/kb_basedoc
sudo chown -R www-data:www-data /var/www/kb_basedoc/storage
```

## 📚 Documentation API

### Endpoints

- `GET /api/categories/tree` - Arborescence des catégories
- `GET /search/suggestions?q=query` - Suggestions de recherche
- `POST /api/tags/generate` - Générer des tags avec IA
- `POST /api/procedures/<id>/autosave` - Auto-save d'une procédure

## 🚀 Fonctionnalités Futures (Phases 2-5)

- ✨ Recherche sémantique IA
- 📊 Statistiques d'utilisation
- 📤 Export PDF des procédures
- 🔄 Versioning complet avec restore
- 📎 Support upload vidéos et fichiers multiples
- 🎨 Coloration syntaxe PowerShell
- 📱 Interface mobile responsive

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/ma-fonctionnalite`)
3. Commit (`git commit -m 'Ajout de ma fonctionnalité'`)
4. Push (`git push origin feature/ma-fonctionnalite`)
5. Ouvrir une Pull Request

## 📄 Licence

Propriétaire - Gagneraud 2024

## 👨‍💻 Auteur

David Heurtebise - Support IT Gagneraud

## 📞 Support

Pour toute question ou problème, contacter le service IT.
