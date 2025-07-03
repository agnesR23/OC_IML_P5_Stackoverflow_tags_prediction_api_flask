import os
import pickle
import logging
import numpy as np
from flask import Flask, request, jsonify
from utils import normalize_text, languages_frameworks, coverage_score_true_pred, precision_at_k_true_pred

app = Flask(__name__)

ARTIFACT_DIR = "artifacts"  # <- Il manquait cette ligne cruciale

CATBOOST_DIR = os.path.join(ARTIFACT_DIR, "catboost")
NMF_DIR = os.path.join(ARTIFACT_DIR, "nmf")

# Chemins CatBoost
CATBOOST_MODEL_PATH = os.path.join(CATBOOST_DIR, "model.pkl")
CATBOOST_VECTORIZER_PATH = os.path.join(CATBOOST_DIR, "vectorizer.pkl")
BINARIZER_PATH = os.path.join(CATBOOST_DIR, "binarizer.pkl")

# Chemins NMF
NMF_MODEL_PATH = os.path.join(NMF_DIR, "model.pkl")
TFIDF_VECTORIZER_PATH = os.path.join(NMF_DIR, "vectorizer.pkl")
H_MATRIX_PATH = os.path.join(NMF_DIR, "H_matrix.pkl")
FEATURE_NAMES_PATH = os.path.join(NMF_DIR, "feature_names.pkl")

DEFAULT_THRESHOLD = 0.5  # configurable

# Chargement des fichiers
model = None
vectorizer = None
binarizer = None

nmf_model = None
tfidf_vectorizer = None
H = None
feature_names = None

def load_artifacts():
    global model, vectorizer, binarizer
    global nmf_model, tfidf_vectorizer, H, feature_names

    try:
        with open(CATBOOST_MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        with open(CATBOOST_VECTORIZER_PATH, "rb") as f:
            vectorizer = pickle.load(f)
        with open(BINARIZER_PATH, "rb") as f:
            binarizer = pickle.load(f)
        print("✅ Modèle CatBoost, vectorizer et binarizer chargés avec succès.")
    except Exception as e:
        print(f"❌ Erreur lors du chargement CatBoost : {e}")

    try:
        with open(NMF_MODEL_PATH, "rb") as f:
            nmf_model = pickle.load(f)
        with open(TFIDF_VECTORIZER_PATH, "rb") as f:
            tfidf_vectorizer = pickle.load(f)
        with open(H_MATRIX_PATH, "rb") as f:
            H = pickle.load(f)
        with open(FEATURE_NAMES_PATH, "rb") as f:
            feature_names = pickle.load(f)
        print("✅ Modèle NMF, TF-IDF vectorizer, H matrix et feature_names chargés avec succès.")
    except Exception as e:
        print(f"❌ Erreur lors du chargement NMF : {e}")
    # Vérification de la cohérence des tailles:
    if nmf_model is not None and tfidf_vectorizer is not None and H is not None:
        print(f"TF-IDF vocab size: {len(tfidf_vectorizer.get_feature_names_out())}")
        print(f"NMF components shape: {nmf_model.components_.shape}")
        if len(tfidf_vectorizer.get_feature_names_out()) != nmf_model.components_.shape[1]:
            print("⚠️ ATTENTION: Vocabulaire TF-IDF et NMF model incohérents !")


if os.environ.get("FLASK_ENV") != "testing":
    load_artifacts()

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API de prédiction de tags est en ligne."})

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route("/predict", methods=["POST"])
def predict_tags():
    data = request.get_json()
    if not data or "title" not in data or "body" not in data:
        return jsonify({"error": "Données JSON invalides, attendu 'title' et 'body'"}), 400
    
    title = data["title"]
    body = data["body"]
    true_tags = data.get("true_tags", None)
    print(type(true_tags), true_tags)

    if not isinstance(title, str) or not isinstance(body, str):
        return jsonify({"error": "'title' et 'body' doivent être des chaînes de caractères."}), 400
    
    threshold = data.get("threshold", DEFAULT_THRESHOLD)
    model_type = data.get("model_type", "catboost").lower()  # par défaut catboost

    try:
        threshold = float(threshold)
    except ValueError:
        threshold = DEFAULT_THRESHOLD

    combined_text = f"{title} {body}"
    normalized_text = normalize_text(combined_text, languages_frameworks)

    if model_type == "catboost":
        if model is None or vectorizer is None or binarizer is None:
            return jsonify({"error": "Modèle CatBoost ou ses artefacts non chargés"}), 500
        try:
            X = vectorizer.transform([normalized_text])
            proba = model.predict_proba(X)[0]  # probabilités multilabel
            classes = model.classes_


            # Récupère les indices des 5 plus fortes probabilités
            top_indices = np.argsort(proba)[::-1][:5]
            predicted_tags = [binarizer.classes_[i] for i in top_indices]
            scores = {binarizer.classes_[i]: float(proba[i]) for i in top_indices}

            # Calcul des métriques supervisées si true_tags fournis
            coverage = None
            precision_at_3 = None
            if true_tags is not None and isinstance(true_tags, list) and len(true_tags) > 0:
                coverage = coverage_score_true_pred([true_tags], [predicted_tags])
                precision_at_3 = precision_at_k_true_pred([true_tags], [predicted_tags], k=3)

            
        except Exception as e:
            app.logger.error(f"Erreur prédiction CatBoost: {e}")
            return jsonify({"error": "Erreur interne lors de la prédiction CatBoost."}), 500
        
        response = {
            "predicted_tags": predicted_tags,
            "scores": scores,
            "threshold": threshold,
            "model_type": model_type,
            "coverage": coverage,
            "precision_at_3": precision_at_3
        }

    elif model_type == "nmf":
        if nmf_model is None or tfidf_vectorizer is None or H is None or feature_names is None:
            return jsonify({"error": "Modèle NMF ou ses artefacts non chargés"}), 500
        try:
            X_tfidf = tfidf_vectorizer.transform([normalized_text])
            app.logger.info(f"TF-IDF shape: {X_tfidf.shape}")
            
            topic_probs = nmf_model.transform(X_tfidf)  # shape (1, n_topics)
            app.logger.info(f"Topic probs: {topic_probs}")

            if topic_probs.shape[1] != H.shape[0]:
                raise ValueError(f"Dimension mismatch: topic_probs={topic_probs.shape}, H={H.shape}")

            if topic_probs.sum() == 0:
                raise ValueError("Aucune probabilité de topic non nulle — texte peut-être trop vide ou inconnu du vocabulaire.")



            top_topic_id = topic_probs[0].argmax()
            top_word_indices = H[top_topic_id].argsort()[::-1][:5]
            predicted_tags = [feature_names[i] for i in top_word_indices]
            scores = {tag: float(topic_probs[0][top_topic_id]) for tag in predicted_tags}

            
            threshold = None


        except Exception as e:
            import traceback
            app.logger.error("Erreur prédiction NMF:")
            app.logger.error(traceback.format_exc())  # Affiche la stack trace complète
            return jsonify({"error": "Erreur interne lors de la prédiction NMF."}), 500
        
        response = {
            "predicted_tags": predicted_tags,
            "scores": scores,
            "threshold": threshold,
            "model_type": model_type
        }

    else:
        return jsonify({"error": f"Type de modèle inconnu : {model_type}"}), 400

    return jsonify(response)

if __name__ == "__main__":
    if os.environ.get("FLASK_ENV") != "testing":
        load_artifacts()
    logging.basicConfig(level=logging.INFO)
    logging.info("🚀 API Flask démarée sur http://0.0.0.0:5001")
    app.run(host="0.0.0.0", port=5001, debug=True)
