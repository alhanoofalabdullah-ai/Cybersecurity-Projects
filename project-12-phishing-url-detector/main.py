from urllib.parse import urlparse

suspicious_keywords = [
    "login",
    "verify",
    "update",
    "secure",
    "account",
    "bank",
    "password",
    "confirm"
]


def analyze_url(url):
    score = 0
    reasons = []

    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()

    if parsed_url.scheme != "https":
        score += 2
        reasons.append("URL does not use HTTPS")

    if len(url) > 75:
        score += 1
        reasons.append("URL is unusually long")

    if url.count("-") > 3:
        score += 1
        reasons.append("URL contains many hyphens")

    if url.count(".") > 4:
        score += 1
        reasons.append("URL contains many dots")

    for keyword in suspicious_keywords:
        if keyword in url.lower():
            score += 1
            reasons.append(f"Suspicious keyword found: {keyword}")

    if "@" in url:
        score += 2
        reasons.append("URL contains @ symbol")

    if domain.count(".") > 3:
        score += 1
        reasons.append("Domain has multiple subdomains")

    return score, reasons


def get_risk_level(score):
    if score >= 5:
        return "High Risk"
    if score >= 3:
        return "Medium Risk"
    return "Low Risk"


def main():
    url = input("Enter URL to analyze: ").strip()

    if not url:
        print("URL is required.")
        return

    score, reasons = analyze_url(url)
    risk_level = get_risk_level(score)

    print("\n===== Phishing URL Analysis =====")
    print(f"URL: {url}")
    print(f"Risk Score: {score}")
    print(f"Risk Level: {risk_level}")

    if reasons:
        print("\nReasons:")
        for reason in reasons:
            print(f"- {reason}")
    else:
        print("\nNo suspicious indicators found.")


if __name__ == "__main__":
    main()
