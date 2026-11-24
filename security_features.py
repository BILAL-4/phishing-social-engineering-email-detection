import re
from urllib.parse import urlparse

URL_PATTERN = re.compile(r"https?://[^\s<>]+|www\.[^\s<>]+", re.IGNORECASE)

SUSPICIOUS_TERMS = (
    "verify", "urgent", "password", "login", "invoice", "payment",
    "account", "suspended", "click", "reset", "gift", "prize",
)


def extract_security_features(text):
    text = text or ""
    lowered = text.lower()
    urls = URL_PATTERN.findall(text)

    normalized_urls = []
    suspicious_url_count = 0
    for url in urls:
        normalized = url.lower().replace("\\", "/")
        normalized = re.sub(r"%(25)?3[ad]", ".", normalized)
        normalized = re.sub(r"h[\W_]*t[\W_]*t[\W_]*p[\W_]*s?", "http", normalized)
        normalized_urls.append(normalized)
        suspicious_url_count += int(
            any(mark in normalized for mark in ("@", "login", "verify", "secure", "account"))
            or url.count(".") >= 3
        )

    spf = re.search(r"\bspf\s*=\s*(pass|fail|softfail|neutral|none)\b", lowered)
    dkim = re.search(r"\bdkim\s*=\s*(pass|fail|none)\b", lowered)
    dmarc = re.search(r"\bdmarc\s*=\s*(pass|fail|none)\b", lowered)

    result = [
        f"spf_{spf.group(1) if spf else 'missing'}",
        f"dkim_{dkim.group(1) if dkim else 'missing'}",
        f"dmarc_{dmarc.group(1) if dmarc else 'missing'}",
        f"header_missing_count_{int(not spf) + int(not dkim) + int(not dmarc)}",
        f"suspicious_url_count_{suspicious_url_count}",
        f"url_count_{len(urls)}",
        f"url_obfuscated_{int(any(token in lowered for token in ('&#', 'percent', 'hxxp', 'www%2e')))}",
        f"suspicious_term_count_{sum(lowered.count(term) for term in SUSPICIOUS_TERMS)}",
    ]
    result.extend(normalized_urls[:10])
    return " ".join(result)
