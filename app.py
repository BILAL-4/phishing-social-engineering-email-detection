from flask import Flask, render_template, request, jsonify
import pickle
import re
import nltk
from pathlib import Path
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from security_features import extract_security_features

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

BASE_DIR = Path(__file__).resolve().parent

# Load trained model & vectorizer
model_path = BASE_DIR / "model.pkl"
vectorizer_path = BASE_DIR / "vectorizer.pkl"
if not model_path.exists() or not vectorizer_path.exists():
    model = None
    vectorizer = None
else:
    with model_path.open("rb") as model_file:
        model = pickle.load(model_file)
    with vectorizer_path.open("rb") as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)

nltk.download("stopwords", quiet=True)
stemmer = PorterStemmer()
stop_words = set(stopwords.words("english"))

def preprocess_text(text):
    text = re.sub("[^A-Za-z]", " ", text)
    text = text.lower()
    processed = " ".join(
        stemmer.stem(word)
        for word in text.split()
        if word not in stop_words
    )
    return processed + " " + extract_security_features(text)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    if model is None or vectorizer is None:
        return jsonify(error="Model artifacts are absent. Run train_model.py before starting the app."), 503

    email_text = request.form.get("email", "").strip()
    if not email_text:
        return jsonify(error="Paste email headers or message body before analysis."), 400

    data = vectorizer.transform([preprocess_text(email_text)])
    result = model.predict(data)[0]
    prediction = "Spam Email" if result == 1 else "Not Spam (Ham)"

    return jsonify(prediction=prediction)

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
