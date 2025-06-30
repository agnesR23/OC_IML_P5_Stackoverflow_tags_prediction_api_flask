# 🐍 API Flask – Stack Overflow Tag Predictor  
*Projet 5 – OpenClassrooms – Parcours Ingénieur Machine Learning*

Ce répertoire contient le code de l'API Flask permettant de prédire automatiquement les tags d'une question Stack Overflow.

## 🎯 Objectif

Fournir une API REST simple capable de recevoir une question (titre + corps) et de renvoyer une prédiction de tags.

## 📁 Contenu du répertoire

- `app.py` : point d’entrée de l’API Flask
- `artifacts/` : modèle entraîné et objets de prétraitement
- `environment.yml` : dépendances conda de l’API
- `tests/` : tests unitaires Pytest
- `Dockerfile` : image Docker de l’API
- `README.md` : ce fichier

## ▶️ Lancement local (conda)

```bash
conda env create -f environment.yml
conda activate flask_app_env
python app.py

#L’API sera accessible sur : http://localhost:5001

🧪 Tests unitaires
pytest

🐳 Docker
docker build -t app_flask .
docker run -p 5001:5001 app_flask
