# Phishing & Social Engineering Email Detection

A cybersecurity-focused email classification system designed to identify
phishing, impersonation, and social-engineering attempts rather than
treating spam detection as a purely lexical text-filtering task.

## Security features

- Inspects SPF, DKIM, and DMARC authentication outcomes and missing-header cases.
- Extracts URL count, suspicious URL structure, and obfuscated URL indicators.
- Measures phishing language and urgency indicators.
- Uses a reproducible preprocessing and feature pipeline for both training and inference.
- Includes adversarial-evasion evaluation scenarios for character insertion,
  obfuscated URL syntax, and removed authentication evidence.

## Run locally

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python train_model.py
python app.py
```

Open `http://127.0.0.1:5000`.

## Evaluation

```powershell
python evaluate_adversarial.py
```

The adversarial script reports precision, recall, F1-score, and support for
plain and evasion-modified samples. Use it to document model degradation and
driven remediation work.

## Dataset and ethics

`emails.csv` may contain real-world email content. Publish or redistribute it
only according to the original dataset license, and remove sensitive or
personally identifiable content when preparing a public demo.
