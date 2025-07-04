# 🐍 API Flask – Stack Overflow Tag Predictor  
*Par Agnès Regaud – Projet 5 – OpenClassrooms – Parcours Ingénieur Machine Learning*

![Tests](https://github.com/agnesR23/OC_IML_P5_Stackoverflow_tags_prediction_api_flask/actions/workflows/test.yml/badge.svg?branch=main)



Ce répertoire contient le code source de l’API Flask qui expose un service REST permettant de prédire automatiquement les tags d’une question Stack Overflow à partir de son titre et de son contenu.

## 🎯 Objectif

Fournir une API REST simple et robuste pour recevoir une question (titre + corps) et retourner des prédictions de tags via deux modèles : supervisé (CatBoost) et non supervisé (NMF).

## 📁 Contenu du répertoire

- `app.py` : point d’entrée de l’API Flask
- `artifacts/` : modèles entraînés et objets de prétraitement sauvegardés, non versionné
- `environment.yml` : environnement conda complet pour l’API
- `environment-tests.yml` : environnement léger dédié aux tests unitaires
- `tests/` : tests unitaires Pytest
- `Dockerfile` : définition de l’image Docker pour l’API
- `README.md` : ce fichier

## ▶️ Lancement local (conda)

```bash
conda env create -f environment.yml
conda activate flask_app_env
python app.py

#L’API sera accessible sur : http://localhost:5001

**Important :**
Avant de lancer l’API en local, vous devez donc récupérer ou générer les artefacts et les placer dans le dossier artifacts/

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
- /predict avec CatBoost : vérification des réponses et de la structure (tags prédits, scores, seuils, etc.).

- /predict avec NMF : vérification de la bonne gestion du modèle non supervisé et réponse correcte sans seuil (threshold=None).

- Gestion des erreurs : champs manquants, artefacts non chargés, etc.

- Isolation des composants externes via mocks dans les tests


⚙️ Intégration continue
Les tests sont exécutés automatiquement via GitHub Actions à chaque push grâce à un workflow CI (python-app.yml).