from flask import Flask, render_template, request
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
    prediction = ""
    error = ""

    if request.method == "POST":
        if model is None or vectorizer is None:
            error = "Model artifacts are absent. Run train_model.py before starting the app."
            return render_template("index.html", prediction=prediction, error=error)
        email_text = request.form["email"]

        # Convert text to vector
        data = vectorizer.transform([preprocess_text(email_text)])

        # Predict
        result = model.predict(data)[0]

        if result == 1:
            prediction = "Spam Email"
        else:
            prediction = "Not Spam (Ham)"

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
