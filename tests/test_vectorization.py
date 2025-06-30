import pytest
from app import tfidf_vectorizer
from utils import normalize_text, languages_frameworks
from scipy.sparse import csr_matrix

def test_tfidf_vectorization_output():
    text = "How to center a div in CSS?"
    norm_text = normalize_text(text, languages_frameworks)
    X = tfidf_vectorizer.transform([norm_text])
    
    assert isinstance(X, csr_matrix)
    assert X.shape[0] == 1
    assert X.shape[1] > 0  # il doit y avoir des features
