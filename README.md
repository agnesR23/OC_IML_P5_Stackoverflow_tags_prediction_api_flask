# 🐍 API Flask – Stack Overflow Tag Predictor  
Par Agnès Regaud – Projet 5 – OpenClassrooms – Parcours Ingénieur Machine Learning

![Tests](https://github.com/agnesR23/OC_IML_P5_Stackoverflow_tags_prediction_api_flask/actions/workflows/test.yml/badge.svg?branch=main)

Ce répertoire contient le code source de l’API Flask qui expose un service REST permettant de prédire automatiquement les tags d’une question Stack Overflow à partir de son titre et de son contenu.

🎯 Objectif

- Fournir une API REST simple et robuste pour recevoir une question (titre + corps) et retourner des prédictions de tags via deux modèles : supervisé (CatBoost) et non supervisé (NMF).

📁 Contenu du répertoire

- app.py : point d’entrée de l’API Flask  
- artifacts/ : modèles entraînés et objets de prétraitement (non versionnés, à placer avant lancement)  
- environment.yml : environnement conda complet pour l’API  
- environment-tests.yml : environnement léger dédié aux tests unitaires  
- tests/ : tests unitaires Pytest  
- Dockerfile : définition de l’image Docker pour l’API  
- README.md : ce fichier

▶️ Lancement local (conda)

conda env create -f environment.yml  
conda activate flask_app_env  
python app.py

# L’API sera accessible sur : http://localhost:5001

Important :  
- Avant de lancer l’API en local, placez tous les artefacts nécessaires dans le dossier artifacts/.

🧪 Tests unitaires

conda env create -f environment-tests.yml  
conda activate stackoverflow_tests  
pytest

🐳 Docker

docker build -t app_flask .  
docker run -p 5001:5001 app_flask

▶️ Déploiement sur AWS ECS Fargate

- Construisez et poussez l’image Docker sur Amazon ECR.  
- Déployez la task ECS avec le port 5001 ouvert en inbound.  
- Placez les artefacts (modèles, preprocess) dans le container via un volume ou lors du build.  
- Après chaque déploiement, récupérez l’IP publique de la tâche ECS pour mettre à jour le dashboard Streamlit (voir README du dashboard pour la procédure).

🔍 Tests automatisés

Le projet comprend une suite de tests unitaires automatisés avec pytest, couvrant notamment :

- Prétraitement des données (normalisation, nettoyage)  
- Endpoints de l’API (/predict, etc.) en mode CatBoost et NMF  
- Gestion des erreurs et des cas limites (artefacts manquants, mauvais champs, etc.)  
- Mocks pour les dépendances externes

⚙️ Intégration continue

Les tests sont exécutés automatiquement via GitHub Actions à chaque push grâce à un workflow CI (`test.yml`).

---

Note :  
- Les artefacts sont nécessaires au fonctionnement de l’API mais **non versionnés** (non inclus dans le repo).  
- L’API doit être exposée publiquement (port 5001) pour être consommée par le dashboard Streamlit Cloud.
