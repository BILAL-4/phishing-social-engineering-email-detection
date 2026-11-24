# PhishGuard

**PhishGuard** is a local phishing and social-engineering email analysis console built with Python, Flask, and scikit-learn. It inspects email text and security-related metadata, extracts authentication and URL features, and classifies suspicious messages with a Naive Bayes model.

## 

### 1. Threat Analysis Console


- **Description:** Provides a focused interface for submitting raw email headers or message bodies and displaying whether the payload is likely to be phishing or legitimate email.


<img width="1822" height="872" alt="image" src="https://github.com/user-attachments/assets/636edabb-00ea-46b7-8fe3-1896cddf2c58" />




### 2. Email Security Feature Extraction


- **Description:** Extracts SPF, DKIM, and DMARC outcomes, missing authentication headers, suspicious URL patterns, urgency language, and obfuscated URL indicators.


### 3. Adversarial Evaluation Module


- **Description:** Re-evaluates the classifier under character insertion, obfuscated URL, and missing-authentication scenarios to measure resistance to common evasions.


### 4. Model Training Pipeline


- **Description:** Loads the source dataset, removes duplicates, preprocesses text, creates a stratified train/test split, trains a Naive Bayes classifier, and exports reusable model artifacts.


##  Core Features


- **Authentication Header Analysis:** Flags missing or failed SPF, DKIM, and DMARC evidence.
- **URL Inspection:** Detects suspicious, obfuscated, and unusually structured links.
- **Social-Engineering Indicators:** Measures urgency and phishing language such as account verification, password reset, or payment threats.
- **Train/Test Separation:** Uses a reproducible, stratified split for model evaluation.
- **Adversarial Testing:** Measures classifier behavior under three phishing-evasion scenarios.
- **Local Flask Interface:** Runs entirely locally for private email analysis.


##  Prerequisites


Before setting up **PhishGuard**, make sure you have:

- **Python:** 3.10 or higher
- **Pip:** Available in your Python environment
- **Dataset:** A two-column CSV containing email text and a binary label


##  Installation & Setup


### Step 1: Clone the Repository


```bash
git clone https://github.com/BILAL-4/phishing-social-engineering-email-detection.git
cd phishing-social-engineering-email-detection
```


### Step 2: Create a Virtual Environment


```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```


### Step 3: Install Dependencies


```bash
pip install -r requirements.txt
python train_model.py
```

The training script creates `model.pkl` and `vectorizer.pkl` locally. These generated model artifacts are intentionally excluded from Git.


### Step 4: Start the Application


```bash
python app.py
```


### Step 5: Analyze an Email


Open `http://127.0.0.1:5000`, paste the email headers or body, and run the threat analysis.


### Optional: Run Adversarial Evaluation


```bash
python evaluate_adversarial.py
```


##  Evaluation


The repository is designed to report accuracy, precision, recall, F1-score, and confusion-matrix results. The adversarial module also separates plain, character-inserted, obfuscated-URL, and missing-authentication scenarios.


##  Dataset and Responsible Use


The public repository does not include `emails.csv` or generated model artifacts. Add only datasets you are licensed to distribute and remove sensitive or personally identifiable email content.


##  Author


**Muhammad Bilal**

- BS Cyber Security Undergraduate

