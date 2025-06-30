"""
Tests pour l'API Flask de prédiction de tags Stack Overflow.

- test_predict_success : vérifie qu'une requête POST avec un titre et un corps
  valide renvoie un statut 200 et une réponse JSON contenant les clés attendues 
  ("predicted_tags", "scores", "threshold") avec les types corrects.

- test_predict_nmf_success : teste la prédiction en spécifiant le modèle "nmf" 
  en entrée. Vérifie la présence des tags prédits, scores, que le type de modèle
  est bien "nmf" et que le threshold est None (car NMF ne fournit pas de seuil).

- test_predict_missing_fields : vérifie que l'API répond avec un code 400 (bad request)
  si les champs obligatoires (ici "body") manquent dans la requête.

- test_predict_model_not_loaded : simule une erreur serveur en remplaçant le modèle
  et le vectorizer par None. Vérifie que l'API renvoie une erreur 500 et un message d'erreur.
"""



import pytest
import json
from app import app, model, vectorizer
import numpy as np

# ✅ Mocks simples directement avec monkeypatch
@pytest.fixture(autouse=True)
def mock_models(monkeypatch):
    class DummyModel:
        def predict_proba(self, X):
            return np.array([[0.8, 0.1, 0.1]])
        @property
        def classes_(self):
            return ["python", "list", "reverse"]

    class DummyVectorizer:
        def transform(self, X):
            return np.array([[0.1, 0.2, 0.3]])

    class DummyBinarizer:
        @property
        def classes_(self):
            return ["python", "list", "reverse"]

    class DummyNMF:
        def transform(self, X):
            return np.array([[0.7, 0.2, 0.1]])

    class DummyTFIDF:
        def transform(self, X):
            return np.array([[0.1, 0.2, 0.3]])

    monkeypatch.setattr("app.model", DummyModel())
    monkeypatch.setattr("app.vectorizer", DummyVectorizer())
    monkeypatch.setattr("app.binarizer", DummyBinarizer())
    monkeypatch.setattr("app.nmf_model", DummyNMF())
    monkeypatch.setattr("app.tfidf_vectorizer", DummyTFIDF())
    monkeypatch.setattr("app.H", np.array([[0.1, 0.2, 0.7], [0.3, 0.5, 0.2], [0.4, 0.4, 0.2]]))
    monkeypatch.setattr("app.feature_names", ["css", "html", "center"])



@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_predict_success(client):
    data = {
        "title": "How to reverse a list in Python?",
        "body": "I want to reverse a list efficiently."
    }
    response = client.post("/predict", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 200
    json_data = response.get_json()
    assert "predicted_tags" in json_data
    assert isinstance(json_data["predicted_tags"], list)
    assert "scores" in json_data
    assert isinstance(json_data["scores"], dict)
    assert "threshold" in json_data
    assert isinstance(json_data["threshold"], float)

def test_predict_nmf_success(client):
    data = {
        "title": "How to center a div in CSS?",
        "body": "I want to center a div both vertically and horizontally using CSS.",
        "model_type": "nmf"
    }
    response = client.post("/predict", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 200
    json_data = response.get_json()
    assert "predicted_tags" in json_data
    assert isinstance(json_data["predicted_tags"], list)
    assert "scores" in json_data
    assert isinstance(json_data["scores"], dict)
    assert json_data["model_type"] == "nmf"
    assert json_data["threshold"] is None  # NMF ne renvoie pas de threshold


def test_predict_missing_fields(client):
    data = {
        "title": "Missing body field"
    }
    response = client.post("/predict", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    json_data = response.get_json()
    assert "error" in json_data

def test_predict_model_not_loaded(monkeypatch, client):
    # Simule modèle et vectorizer non chargés
    monkeypatch.setattr("app.model", None)
    monkeypatch.setattr("app.vectorizer", None)
    
    data = {
        "title": "Test title",
        "body": "Test body"
    }
    response = client.post("/predict", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 500
    json_data = response.get_json()
    assert "error" in json_data
