import re
from typing import Tuple


def validate_query(query: str) -> Tuple[bool, str]:
    """
    Guardrail validation for BFSI Assistant.
    Blocks:
    - Privacy violations (PII requests)
    - Account access attempts
    - Illegal activity
    - Fraud-related intent
    """

    q = query.lower().strip()

    # -----------------------------
    # PRIVACY / PII VIOLATIONS
    # -----------------------------
    privacy_patterns = [
        r"someone else'?s account",
        r"other customer'?s details",
        r"give me.*account number",
        r"share.*customer.*details",
        r"customer.*phone number",
        r"customer.*email",
        r"bank account number",
        r"credit card number",
        r"cvv",
        r"otp",
        r"password",
        r"fake interest rate",
    ]

    for pattern in privacy_patterns:
        if re.search(pattern, q):
            return False, (
                "For security and privacy reasons, we cannot share any "
                "customer account or personal information. "
                "Please contact official customer support with proper authentication."
            )

    # -----------------------------
    # ILLEGAL / FRAUD INTENT
    # -----------------------------
    illegal_keywords = [
        "hack",
        "bypass",
        "steal",
        "fraud",
        "scam",
        "phishing",
        "break into account",
        "unauthorized access",
        "fake"
    ]

    for word in illegal_keywords:
        if word in q:
            return False, (
                "This request violates banking security and compliance policies. "
                "We cannot assist with such activities."
            )

    # -----------------------------
    # Extremely Sensitive Data Pattern
    # -----------------------------
    # Block numeric patterns that look like account/card numbers
    if re.search(r"\b\d{12,16}\b", q):
        return False, (
            "Sensitive financial information cannot be processed or shared "
            "through this assistant."
        )

    # -----------------------------
    # If everything is safe
    # -----------------------------
    return True, None
