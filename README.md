# ANG Patrimoine — Django / PostgreSQL

Application web interne : bureaux et salles, sites, directions/commissions, occupants, inventaire des équipements, parc informatique, parc automobile, maintenance, statistiques et journal d'activité. Interface en rouge, jaune et vert. Le logo ANG est provisoire.

## Installation Windows
1. Installer Python 3.11+ et PostgreSQL 14+.
2. Dans PowerShell, à la racine du projet :
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
3. Créer la base et l'utilisateur PostgreSQL :
```sql
CREATE DATABASE ang_patrimoine;
CREATE USER ang_user WITH PASSWORD 'mot-de-passe-fort';
GRANT ALL PRIVILEGES ON DATABASE ang_patrimoine TO ang_user;
```
Pour PostgreSQL 15+, connectez-vous à la base puis exécutez `GRANT ALL ON SCHEMA public TO ang_user;`.
4. Définir les variables d'environnement PowerShell (adapter le mot de passe et IP) :
```powershell
$env:DB_NAME='ang_patrimoine'; $env:DB_USER='ang_user'; $env:DB_PASSWORD='mot-de-passe-fort'; $env:DB_HOST='127.0.0.1'; $env:DB_PORT='5432'
$env:DJANGO_SECRET_KEY='une-cle-secrete-longue-et-aleatoire'; $env:DJANGO_DEBUG='False'; $env:DJANGO_ALLOWED_HOSTS='127.0.0.1,localhost,192.168.1.100'
```
5. Générer et appliquer les migrations, créer le compte admin :
```powershell
python manage.py makemigrations patrimoine
python manage.py migrate
python manage.py createsuperuser
python manage.py check
```
6. Test : `python manage.py runserver 127.0.0.1:8000` puis `http://127.0.0.1:8000/`.

## Réseau interne
Pour un test temporaire sur le LAN, `python manage.py runserver 0.0.0.0:8000` puis ouvrir `http://IP_DU_SERVEUR:8000/` depuis un poste autorisé. Restreindre le port au réseau interne dans le pare-feu. En production, ne pas utiliser `runserver` : utiliser Gunicorn derrière Nginx/Apache avec TLS, sauvegardes PostgreSQL, politique de mots de passe, supervision et tests de restauration. `ALLOWED_HOSTS` doit inclure le nom/IP du serveur.

## Utilisation
Créer d'abord les sites, directions/commissions, locaux puis équipements. Pour les fiches informatiques et véhicules, créer d'abord l'équipement correspondant. Créer ensuite les maintenances/réparations. Utilisateurs et groupes sont gérés dans `/admin/`. Créer des groupes métier et attribuer les permissions Django avant le déploiement.

## À valider avant mise en production
Cette version est une base fonctionnelle initiale. Les formulaires métier requièrent une connexion, mais il reste à appliquer les permissions par rôle de façon granulaire, mettre en place HTTPS et sauvegardes, valider les champs avec les services, et tester les workflows. Les occupants sont actuellement enregistrés dans un champ texte ; un registre du personnel et l'historique nominatif des affectations peuvent être ajoutés ensuite. Les migrations ne sont pas précréées : exécuter `makemigrations patrimoine`.

## Navigation détaillée ajoutée
- Cliquez sur une direction ou commission pour voir ses locaux, le nombre estimé d’occupants et les matériels associés.
- Cliquez sur un bureau ou une salle pour voir sa capacité, ses occupants et la liste de ses matériels.
- Pour calculer les occupants, saisissez les noms séparés par une virgule ou un retour à la ligne dans le champ « occupants ».
