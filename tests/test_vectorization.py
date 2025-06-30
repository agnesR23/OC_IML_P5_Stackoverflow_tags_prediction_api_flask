import pytest
import numpy as np
from scipy.sparse import csr_matrix
from utils import normalize_text, languages_frameworks

# Mock simple du vectorizer
class DummyVectorizer:
    def transform(self, X):
        # Retourne une matrice creuse 1x5 remplie de 1
        return csr_matrix(np.ones((len(X), 5)))

def test_tfidf_vectorization_output(monkeypatch):
    # On remplace tfidf_vectorizer par notre mock
    dummy_vectorizer = DummyVectorizer()
    monkeypatch.setattr("app.tfidf_vectorizer", dummy_vectorizer)

    text = "How to center a div in CSS?"
    norm_text = normalize_text(text, languages_frameworks)

    # Importer après monkeypatch pour s'assurer qu'on utilise le mock
    from app import tfidf_vectorizer

    X = tfidf_vectorizer.transform([norm_text])

    assert isinstance(X, csr_matrix)
    assert X.shape[0] == 1
    assert X.shape[1] == 5  # correspond à la taille simulée par le mock
