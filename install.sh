#!/bin/bash

#################################################
# Script d'installation KB Support Basedoc
# Pour Ubuntu 24.04 LTS
#################################################

set -e

echo "========================================="
echo "Installation KB Support Basedoc"
echo "========================================="
echo ""

# Vérifier si root
if [ "$EUID" -ne 0 ]; then
    echo "⚠️  Ce script doit être exécuté en tant que root (sudo)"
    exit 1
fi

# Variables
APP_DIR="/var/www/kb_basedoc"
APP_USER="www-data"
DOMAIN="gagneraud.basedoc.fr"
DB_NAME="kb_basedoc"
DB_USER="kb_user"
DB_PASSWORD=$(openssl rand -base64 32)

echo "Configuration:"
echo "  - Domaine: $DOMAIN"
echo "  - Répertoire app: $APP_DIR"
echo "  - Base de données: $DB_NAME"
echo ""

read -p "Continuer l'installation? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

# 1. Mise à jour système
echo ""
echo "[1/10] Mise à jour du système..."
apt update
apt upgrade -y

# 2. Installation Python 3.12
echo ""
echo "[2/10] Installation Python 3.12..."
apt install -y python3.12 python3.12-venv python3-pip python3.12-dev build-essential

# 3. Installation PostgreSQL
echo ""
echo "[3/10] Installation PostgreSQL..."
apt install -y postgresql postgresql-contrib libpq-dev

# 4. Configuration PostgreSQL
echo ""
echo "[4/10] Configuration de la base de données..."
sudo -u postgres psql << EOF
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
ALTER DATABASE $DB_NAME OWNER TO $DB_USER;
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
\q
EOF

echo "  ✓ Base de données créée"
echo "  DB_USER: $DB_USER"
echo "  DB_PASSWORD: $DB_PASSWORD"

# Sauvegarder les credentials
echo "DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@localhost/$DB_NAME" > /root/.kb_basedoc_db

# 5. Installation Nginx
echo ""
echo "[5/10] Installation Nginx..."
apt install -y nginx

# 6. Création des répertoires
echo ""
echo "[6/10] Création des répertoires..."
mkdir -p $APP_DIR
mkdir -p $APP_DIR/storage/procedures
mkdir -p /var/log/gunicorn
mkdir -p /var/run/gunicorn

# 7. Copie des fichiers (si script exécuté depuis le repo)
echo ""
echo "[7/10] Copie des fichiers de l'application..."
if [ -d "./app" ]; then
    cp -r ./* $APP_DIR/
    echo "  ✓ Fichiers copiés depuis le répertoire courant"
else
    echo "  ⚠️  Fichiers non trouvés. Veuillez copier manuellement l'application vers $APP_DIR"
fi

# 8. Configuration Python venv et installation dépendances
echo ""
echo "[8/10] Installation des dépendances Python..."
cd $APP_DIR
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 9. Configuration Nginx
echo ""
echo "[9/10] Configuration Nginx..."
cat > /etc/nginx/sites-available/kb_basedoc << 'EOF'
server {
    listen 80;
    server_name DOMAIN_PLACEHOLDER;

    location / {
        return 301 https://$server_name$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name DOMAIN_PLACEHOLDER;

    # SSL (à configurer avec certbot)
    # ssl_certificate /etc/letsencrypt/live/DOMAIN_PLACEHOLDER/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/DOMAIN_PLACEHOLDER/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    access_log /var/log/nginx/kb_basedoc_access.log;
    error_log /var/log/nginx/kb_basedoc_error.log;

    # Static files
    location /static {
        alias /var/www/kb_basedoc/app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Storage
    location /storage {
        alias /var/www/kb_basedoc/storage;
        internal;
    }

    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        client_max_body_size 50M;
    }
}
EOF

sed -i "s/DOMAIN_PLACEHOLDER/$DOMAIN/g" /etc/nginx/sites-available/kb_basedoc

ln -sf /etc/nginx/sites-available/kb_basedoc /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

nginx -t
systemctl restart nginx

echo "  ✓ Nginx configuré"

# 10. Configuration systemd service
echo ""
echo "[10/10] Configuration du service systemd..."
cat > /etc/systemd/system/kb_basedoc.service << EOF
[Unit]
Description=KB Basedoc Gunicorn Service
After=network.target postgresql.service

[Service]
Type=notify
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
Environment="DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@localhost/$DB_NAME"
Environment="FLASK_ENV=production"
ExecStart=$APP_DIR/venv/bin/gunicorn --config $APP_DIR/gunicorn_config.py run:app
ExecReload=/bin/kill -s HUP \$MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Permissions
chown -R $APP_USER:$APP_USER $APP_DIR
chown -R $APP_USER:$APP_USER /var/log/gunicorn
chown -R $APP_USER:$APP_USER /var/run/gunicorn

# Créer le fichier .env
cat > $APP_DIR/.env << EOF
FLASK_ENV=production
SECRET_KEY=$(openssl rand -hex 32)
DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@localhost/$DB_NAME
UPLOAD_FOLDER=$APP_DIR/storage
SESSION_COOKIE_SECURE=True
CLAUDE_API_KEY=
EOF

chown $APP_USER:$APP_USER $APP_DIR/.env
chmod 600 $APP_DIR/.env

# Initialiser la base de données
echo ""
echo "Initialisation de la base de données..."
cd $APP_DIR
source venv/bin/activate
export FLASK_APP=run.py
export DATABASE_URL="postgresql://$DB_USER:$DB_PASSWORD@localhost/$DB_NAME"

# Créer les tables et seed
python3 seed_data.py

# Démarrer le service
systemctl daemon-reload
systemctl enable kb_basedoc
systemctl start kb_basedoc

echo ""
echo "========================================="
echo "✅ Installation terminée!"
echo "========================================="
echo ""
echo "Informations importantes:"
echo ""
echo "  Base de données:"
echo "    - Nom: $DB_NAME"
echo "    - User: $DB_USER"
echo "    - Password: (sauvegardé dans /root/.kb_basedoc_db)"
echo ""
echo "  Application:"
echo "    - Répertoire: $APP_DIR"
echo "    - Service: kb_basedoc.service"
echo "    - Config: $APP_DIR/.env"
echo ""
echo "  Admin par défaut:"
echo "    - Email: dheurtebise@basedoc.fr"
echo "    - Password: Admin123!"
echo "    ⚠️  CHANGEZ CE MOT DE PASSE IMMÉDIATEMENT!"
echo ""
echo "Prochaines étapes:"
echo ""
echo "  1. Configurer la clé API Claude dans $APP_DIR/.env"
echo "  2. Installer certbot pour SSL:"
echo "     apt install certbot python3-certbot-nginx"
echo "     certbot --nginx -d $DOMAIN"
echo ""
echo "  3. Vérifier le service:"
echo "     systemctl status kb_basedoc"
echo ""
echo "  4. Accéder à l'application:"
echo "     http://$DOMAIN (redirection HTTPS après certbot)"
echo ""
echo "Commandes utiles:"
echo "  - Redémarrer: systemctl restart kb_basedoc"
echo "  - Logs: journalctl -u kb_basedoc -f"
echo "  - Nginx logs: tail -f /var/log/nginx/kb_basedoc_error.log"
echo ""
