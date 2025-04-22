# Formation AssMat

Application de gestion des formations pour les assistantes maternelles.

## Fonctionnalités

- Partie publique présentant l'application
- Espace membre pour les utilisateurs
  - Gestion du profil
  - Gestion des souhaits de formation
  - Suivi des formations réalisées
- Espace administrateur
  - Gestion des formations
  - Gestion des utilisateurs
  - Administration des actions de formation

## Installation

1. Cloner le repository
2. Créer un environnement virtuel Python :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Créer un fichier `.env` à la racine du projet avec les variables suivantes :
```
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///app.db
```

5. Initialiser la base de données :
```bash
flask db init
flask db migrate
flask db upgrade
```

## Lancement

```bash
flask run
```

L'application sera accessible à l'adresse : http://localhost:5000
