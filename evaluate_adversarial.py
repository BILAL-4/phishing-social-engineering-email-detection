import pickle
import re
from security_features import extract_security_features
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.metrics import classification_report

ATTACKS = [
    ("plain", lambda text: text),
    ("character-insertion", lambda text: re.sub(r"(verify|password|urgent)", r"v-e-r-i-f-y", text, flags=re.I)),
    ("obfuscated-url", lambda text: text.replace("https://", "hxxps://").replace(".com", ".c0m")),
    ("missing-authentication", lambda text: re.sub(r"(?im)^.*(spf|dkim|dmarc).*$", "", text)),
]


def preprocess(text):
    text = re.sub("[^A-Za-z]", " ", text)
    text = text.lower()
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words("english"))
    return " ".join(
        stemmer.stem(word) for word in text.split() if word not in stop_words
    ) + " " + extract_security_features(text)


def evaluate(samples):
    with open("model.pkl", "rb") as model_file:
        model = pickle.load(model_file)
    with open("vectorizer.pkl", "rb") as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)

    for name, attack in ATTACKS:
        texts = [attack(text) for text, _ in samples]
        labels = [label for _, label in samples]
        predictions = model.predict(vectorizer.transform([preprocess(text) for text in texts]))
        print(f"\nAttack scenario: {name}")
        print(classification_report(labels, predictions, digits=3, zero_division=0))


if __name__ == "__main__":
    evaluate([
        ("URGENT verify your account password at https://secure-login.example.com", 1),
        ("Meeting notes and the quarterly project update are attached", 0),
    ])
