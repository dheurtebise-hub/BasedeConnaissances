# Guide de l'Éditeur Quill WYSIWYG

## 🎯 Fonctionnalités

L'éditeur Quill remplace le textarea simple et offre des capacités avancées pour répondre à vos besoins :

### ✅ Copier-coller d'images
- **Capture d'écran** : Faites `Windows + Shift + S`, capturez une zone, puis collez avec `Ctrl+V` dans l'éditeur
- **Image depuis navigateur** : Clic droit sur une image web > Copier l'image > Coller dans l'éditeur
- **Image depuis dossier** : Copier un fichier image > Coller dans l'éditeur
- Les images sont automatiquement encodées en Base64 et intégrées au contenu

### ✅ Copier-coller depuis Word/PDF
- Ouvrez votre document Word ou PDF
- Sélectionnez le contenu avec mise en forme (titres, listes, gras, couleurs, etc.)
- Copiez avec `Ctrl+C`
- Collez dans l'éditeur Quill avec `Ctrl+V`
- **La mise en forme est préservée automatiquement**

### ✅ Glisser-déposer d'images
- Ouvrez votre explorateur de fichiers Windows
- Glissez une image (PNG, JPG, GIF) directement dans l'éditeur
- L'image est insérée automatiquement à l'emplacement du curseur

### ✅ Barre d'outils complète
- **En-têtes** : H1, H2, H3, H4, H5, H6
- **Styles de texte** : Gras, Italique, Souligné, Barré
- **Listes** : Ordonnées (numérotées), À puces
- **Indentation** : Augmenter/Diminuer
- **Alignement** : Gauche, Centre, Droite, Justifié
- **Couleurs** : Texte et fond
- **Citations** : Blocs de citation
- **Code** : Blocs de code
- **Liens et images** : Insertion manuelle

## 🚀 Comment l'utiliser

### 1. Accéder au formulaire de création/édition
- Cliquez sur `+ NEW` dans le header
- Ou éditez une procédure existante

### 2. L'éditeur se charge automatiquement
- Vous verrez un message "🔄 Chargement de l'éditeur..."
- Après 1-2 secondes, la barre d'outils Quill apparaît
- Si l'éditeur ne charge pas en 5 secondes, un textarea simple s'affiche automatiquement

### 3. Rédiger votre contenu
**Option A : Rédaction directe**
- Tapez votre texte normalement
- Utilisez la barre d'outils pour formater
- Cliquez sur le bouton "Image" pour insérer une image depuis URL

**Option B : Coller depuis Word/PDF**
1. Ouvrez votre document Word/PDF existant
2. Sélectionnez tout (`Ctrl+A`) ou une partie
3. Copiez (`Ctrl+C`)
4. Collez dans Quill (`Ctrl+V`)
5. Votre mise en forme est conservée !

**Option C : Ajouter des images**
- **Copier-coller** : Copiez une image depuis n'importe où, collez avec `Ctrl+V`
- **Glisser-déposer** : Glissez un fichier image dans l'éditeur
- **Capture d'écran** : `Win+Shift+S` > Capturez > `Ctrl+V` dans l'éditeur

### 4. Génération de tags automatique
- Le bouton "🤖 Générer avec IA" fonctionne avec Quill
- Il analyse le contenu de l'éditeur pour suggérer des tags

### 5. Enregistrer
- Cliquez sur "💾 Enregistrer"
- Le contenu HTML est automatiquement synchronisé et sauvegardé

## 🎨 Interface

L'éditeur Quill a été stylisé pour s'intégrer au thème dark de l'application :

- **Barre d'outils** : Fond gris foncé avec boutons clairs
- **Zone d'édition** : Fond noir avec texte blanc
- **Images** : Coins arrondis, espacement automatique
- **Code** : Blocs avec fond sombre et bordure
- **Citations** : Barre bleue à gauche

## 🔧 Fonctionnement technique

### Stockage des images
Les images sont encodées en **Base64** et intégrées directement dans le HTML du contenu. Cela signifie :
- ✅ Pas de gestion de fichiers séparés
- ✅ Pas de serveur d'upload nécessaire
- ✅ Contenu auto-suffisant et portable
- ⚠️ Les images très grandes augmentent la taille du HTML

### Compatibilité navigateur
Testé et fonctionnel sur :
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

### Fallback automatique
Si Quill ne charge pas (problème réseau, CDN bloqué, etc.) :
1. Le système détecte automatiquement l'échec
2. Un textarea HTML simple s'affiche
3. Vous pouvez quand même coller du HTML brut
4. Un message d'avertissement apparaît

## 🐛 Dépannage

### L'éditeur ne charge pas
**Symptôme** : Message "🔄 Chargement de l'éditeur..." qui reste affiché

**Causes possibles** :
1. Connexion Internet coupée (Quill se charge depuis CDN)
2. Pare-feu bloquant cdn.quilljs.com
3. Adblocker trop agressif

**Solution** :
- Attendez 5 secondes, le textarea simple s'affichera automatiquement
- Ou désactivez temporairement votre adblocker
- Ou vérifiez votre connexion Internet

### Les images ne se collent pas
**Symptôme** : Ctrl+V ne colle pas l'image

**Vérifications** :
1. Êtes-vous sûr d'avoir copié une **image** et non un chemin de fichier ?
2. Testez avec une capture d'écran : `Win+Shift+S` puis `Ctrl+V`
3. Vérifiez la console navigateur (F12) pour voir les erreurs

### La mise en forme Word n'est pas préservée
**Symptôme** : Le texte se colle sans formatage

**Causes** :
- Vous avez collé du texte brut (`Ctrl+Shift+V` au lieu de `Ctrl+V`)
- Le document Word a un formatage non standard

**Solution** :
- Utilisez bien `Ctrl+V` (pas Ctrl+Shift+V)
- Depuis Word, sélectionnez et copiez à nouveau
- Si ça ne fonctionne pas, copiez depuis Word vers un nouvel email Gmail, puis depuis Gmail vers Quill (Gmail normalise le HTML)

## 📝 Exemples d'utilisation

### Créer une procédure "Créer une boîte mail partagée"

1. **Titre** : "Créer une boîte mail partagée dans Outlook 365"

2. **Contenu** (à copier depuis Word ou rédiger dans Quill) :
   ```
   # Prérequis
   - Droits administrateur Exchange
   - Accès au Centre d'administration Microsoft 365

   # Étapes
   1. Se connecter au portail admin.microsoft.com
   2. Aller dans **Équipes et groupes** > **Boîtes aux lettres partagées**
   3. Cliquer sur **+ Ajouter une boîte aux lettres partagée**
   4. Remplir les informations :
      - Nom d'affichage
      - Adresse e-mail
   5. Ajouter les membres qui auront accès

   # Capture d'écran
   [Collez ici une capture d'écran du portail admin avec Win+Shift+S puis Ctrl+V]

   # Permissions
   Par défaut, les membres ont un accès complet.
   Pour modifier :
   - Sélectionner la boîte partagée
   - Cliquer sur **Modifier** à côté de "Membres"
   - Choisir le niveau : Lecture seule ou Accès complet
   ```

3. **Tags** : Cliquez sur "🤖 Générer avec IA" pour auto-générer, ou saisissez : `outlook, boite-partagee, o365, exchange`

4. **Catégorie** : Office 365 > Outlook

5. **Enregistrer** : Cliquez sur "💾 Enregistrer"

## 🎓 Astuces avancées

### Coller du code
Pour coller du code informatique (PowerShell, Python, etc.) :
1. Cliquez sur le bouton "Code" dans la barre d'outils Quill
2. Collez votre code
3. Il sera affiché avec fond sombre et police monospace

### Nettoyer le formatage
Si vous collez du texte avec un formatage indésirable :
1. Sélectionnez le texte problématique
2. Cliquez sur le bouton "Gomme" (dernier bouton de la barre d'outils)
3. Le formatage est supprimé, seul le texte reste

### Images trop grandes
Si une image collée est trop grande :
1. Cliquez sur l'image dans l'éditeur
2. Redimensionnez-la en tirant les coins (si module de redimensionnement activé)
3. Ou coupez l'image, éditez-la avec Paint, puis recollez

### Sauvegarder un brouillon
Le contenu est synchronisé automatiquement avec le formulaire.
Si vous fermez par accident sans sauvegarder :
- ⚠️ **Le contenu est perdu** (pas d'autosave pour l'instant)
- Solution : Sauvegardez régulièrement avec "💾 Enregistrer"

## 📊 Limites connues

### Taille des images
Les images sont encodées en Base64, ce qui augmente leur taille de ~33%.
Recommandations :
- ✅ Captures d'écran : OK (généralement < 500 Ko)
- ✅ Images optimisées PNG/JPG : OK (< 1 Mo)
- ⚠️ Photos haute résolution : À éviter (> 5 Mo)
- ❌ Fichiers RAW, BMP non compressés : Non recommandé

### Vidéos
Quill ne supporte pas l'intégration de vidéos directement.
Alternatives :
- Insérez un lien YouTube avec le bouton "Lien"
- Ou mettez un lien vers le fichier vidéo sur SharePoint

### Tableaux complexes
Les tableaux Word avec fusion de cellules peuvent avoir un rendu approximatif.
Solution :
- Simplifiez le tableau dans Word avant de copier
- Ou utilisez des listes à la place

## ✅ Checklist de test

Pour vérifier que tout fonctionne :

- [ ] L'éditeur Quill se charge en moins de 3 secondes
- [ ] La barre d'outils est visible avec tous les boutons
- [ ] Je peux taper du texte normalement
- [ ] Je peux formater en gras, italique, souligné
- [ ] Je peux créer une liste à puces
- [ ] Je peux créer une liste numérotée
- [ ] Je peux coller une capture d'écran (Win+Shift+S puis Ctrl+V)
- [ ] L'image apparaît dans l'éditeur
- [ ] Je peux coller du texte formaté depuis Word
- [ ] La mise en forme Word est préservée
- [ ] Je peux glisser une image PNG/JPG dans l'éditeur
- [ ] Le bouton "🤖 Générer avec IA" fonctionne
- [ ] Je peux enregistrer la procédure
- [ ] En consultant la procédure, le contenu s'affiche correctement

## 📞 Support

Si vous rencontrez un problème non résolu par ce guide :
1. Ouvrez la console du navigateur (F12)
2. Regardez l'onglet "Console" pour voir les erreurs en rouge
3. Copiez les erreurs et contactez le développeur

---

**Version Quill** : 1.3.7
**Date de mise à jour** : 2025-12-11
**Compatibilité** : Chrome 90+, Firefox 88+, Edge 90+, Safari 14+
