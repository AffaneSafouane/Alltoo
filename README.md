# Facturo

**Facturo** est une application web développée avec Django permettant de gérer des produits et de générer des factures associant ces produits. Elle offre une interface claire pour la gestion des produits, la création et la consultation des factures, avec un système de pagination pour faciliter la navigation.

---

## Fonctionnalités

- Gestion complète des produits (création, lecture, mise à jour, suppression)  
- Création de factures en sélectionnant plusieurs produits  
- Vue détaillée des factures (nombre de produits, total à payer, etc.)  
- Pagination pour les listes de produits et de factures  

---

## Prérequis

- Python 3.x  
- [venv](https://docs.python.org/fr/3/library/venv.html) (environnement virtuel Python)  

---

## Installation et lancement

1. **Cloner le dépôt** (ou télécharger les fichiers du projet)  
   ```bash
   git clone https://github.com/AffaneSafouane/Alltoo.git
   cd Alltoo
   ```
2. **Créer et activer l’environnement virtuel**  
   Sous Linux/macOS :
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```
   Sous Windows :
      ```bash
      python -m venv venv
      .\venv\Scripts\Activate.ps1
      ```
3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```
4. **Appliquer les migrations (création de la base de données SQLite et tables)**
   ```bash
   cd facturo
   python manage.py migrate
   ```
5. **Charger les données dans la base**  
   Faites attention à bien charger les fixtures dans le bon ordre
   ```bash
   python manage.py loaddata products_fixture.json
   python manage.py loaddata invoices_fixture.json
   python manage.py loaddata invoiceproducts_fixture.json
   ```
6. **Créer un super-utilisateur (pour accéder à l’interface d’administration)**
   Choisissez un nom d'utilisateur et un mot de passe, vous pouvez ignorer l'email.
   ```bash
   python manage.py createsuperuser
   ```
7. **Lancer le serveur de développement**
   ```bash
   python manage.py runserver
   ```
   
---

## Accès à l'application

Ouvrez votre navigateur et rendez-vous sur :  
http://127.0.0.1:8000
