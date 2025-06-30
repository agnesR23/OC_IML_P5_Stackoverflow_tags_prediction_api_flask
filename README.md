# 🐍 API Flask – Stack Overflow Tag Predictor  
*Projet 5 – OpenClassrooms – Parcours Ingénieur Machine Learning*

![Tests](https://github.com/agnesR23/OC_IML_P5_Stackoverflow_tags_prediction_api_flask/actions/workflows/test.yml/badge.svg?branch=main)



Ce répertoire contient le code de l'API Flask permettant de prédire automatiquement les tags d'une question Stack Overflow.

## 🎯 Objectif

Fournir une API REST simple capable de recevoir une question (titre + corps) et de renvoyer une prédiction de tags.

## 📁 Contenu du répertoire

- `app.py` : point d’entrée de l’API Flask
- `artifacts/` : modèle entraîné et objets de prétraitement
- `environment.yml` : dépendances conda de l’API
- `environment-tests.yml` : dépendances conda légères pour les tests unitaires
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
conda env create -f environment-tests.yml
conda activate stackoverflow_tests
pytest

🐳 Docker
docker build -t app_flask .
docker run -p 5001:5001 app_flask


🔍 Tests automatisés
Ce projet comprend une suite de tests unitaires automatisés avec pytest, couvrant les aspects suivants :

✅ Prétraitement des données
Vérification que la fonction normalize_text nettoie et transforme les textes comme attendu.

Cas testés : suppression des majuscules, des caractères spéciaux, des balises HTML, etc.

✅ API Flask de prédiction de tags
/predict avec CatBoost :

Envoie d’une requête valide avec title + body ⇒ réponse attendue : 200 OK.

Vérifie la structure de la réponse (predicted_tags, scores, threshold, etc.).

/predict avec NMF :

Requête avec model_type="nmf" ⇒ réponse correcte sans seuil (threshold=None).

Gestion des erreurs :

Champs manquants (body absent) ⇒ renvoie 400 Bad Request.

Artefacts non chargés (modèle ou vectorizer absents) ⇒ renvoie 500 Internal Server Error.

Tous les composants externes (modèle, vectorizer…) sont mockés dans les tests pour isoler le comportement de l'API.

⚙️ Intégration continue
Les tests sont exécutés automatiquement via GitHub Actions à chaque push grâce à un workflow CI (python-app.yml).