from utils import normalize_text

def test_normalize_text_basic():
    text = "How to Use Pandas in PYTHON!?!"
    tech_words = ["python", "pandas"]
    result = normalize_text(text, tech_words)

    assert "python" in result
    assert "pandas" in result
    assert "!" not in result
    assert "?" not in result
    assert result == result.lower()  # tout doit être en minuscules
    
def test_normalize_text_empty_string():
    text = ""
    tech_words = ["python", "pandas"]
    result = normalize_text(text, tech_words)

    assert isinstance(result, str)
    assert result == ""
