import numpy as np
import pandas as pd
import pytest
from utils import (
    compute_metrics,
    coverage_score,
    precision_at_k,
    coverage_score_true_pred,
    precision_at_k_true_pred,
    compute_row_scores,
    f1_at_k
)

# ======= Tests métriques supervisées (binarisées) =======

def test_coverage_score():
    y_true = np.array([
        [1, 0, 1],
        [0, 1, 0],
        [1, 1, 0]
    ])
    y_pred = np.array([
        [0, 0, 1],  # overlap in last tag
        [0, 0, 0],  # no overlap
        [1, 0, 0]   # overlap in first tag
    ])
    result = coverage_score(y_true, y_pred)
    assert 0 <= result <= 1
    assert pytest.approx(result, 0.01) == 2/3

def test_precision_at_k():
    y_true = np.array([
        [1, 0, 1],
        [0, 1, 0]
    ])
    y_pred_probs = np.array([
        [0.9, 0.1, 0.8],
        [0.2, 0.7, 0.1]
    ])
    result = precision_at_k(y_true, y_pred_probs, k=2)
    assert 0 <= result <= 1

def test_compute_metrics():
    y_true = np.array([
        [1, 0, 1],
        [0, 1, 0]
    ])
    y_pred_probs = np.array([
        [0.9, 0.1, 0.8],
        [0.2, 0.7, 0.1]
    ])
    df_metrics = compute_metrics(y_true, y_pred_probs, thresholds=[0.5], k=2, model_name="test_model")
    assert isinstance(df_metrics, pd.DataFrame)
    assert "F1_micro" in df_metrics.columns
    assert "Coverage" in df_metrics.columns
    assert df_metrics["ModelName"].iloc[0] == "test_model"

# ======= Tests métriques non supervisées (listes de tags) =======

def test_coverage_score_true_pred():
    y_true = [
        ["python", "list"],
        ["java"],
        ["css", "html"]
    ]
    y_pred = [
        ["list", "dict"],  # overlap "list"
        ["python"],        # no overlap
        ["html", "css"]    # full overlap
    ]
    result = coverage_score_true_pred(y_true, y_pred)
    assert 0 <= result <= 1
    assert pytest.approx(result, 0.01) == 2/3

def test_precision_at_k_true_pred():
    y_true = [
        ["python", "list"],
        ["java"],
        ["css", "html"]
    ]
    y_pred = [
        ["list", "dict", "tuple"],
        ["python", "java", "c++"],
        ["html", "css", "bootstrap"]
    ]
    result = precision_at_k_true_pred(y_true, y_pred, k=2)
    assert 0 <= result <= 1

def test_f1_at_k():
    p = 0.6
    r = 0.8
    f1 = f1_at_k(p, r)
    assert 0 <= f1 <= 1
    assert f1 == pytest.approx(2 * p * r / (p + r))

def test_compute_row_scores():
    true_tags = ["python", "list", "dict"]
    pred_tags = ["list", "python", "set"]
    precision, recall, f1 = compute_row_scores(true_tags, pred_tags, k=2)
    assert 0 <= precision <= 1
    assert 0 <= recall <= 1
    assert 0 <= f1 <= 1

if __name__ == "__main__":
    pytest.main()
