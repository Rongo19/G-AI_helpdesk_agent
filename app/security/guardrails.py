import re


# ----------------------------------
# 1. Prompt Injection Detection
# ----------------------------------

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(all\s+)?system\s+instructions",
    r"reveal\s+(your\s+)?system\s+prompt",
    r"show\s+(me\s+)?your\s+system\s+prompt",
    r"reveal\s+(your\s+)?hidden\s+instructions",
    r"bypass\s+(your\s+)?(security|guardrails|restrictions)",
    r"disregard\s+(all\s+)?(previous|above)\s+instructions",
    r"act\s+as\s+(an?\s+)?unrestricted",
    r"developer\s+mode",
    r"print\s+(the\s+)?api\s+key",
    r"reveal\s+(the\s+)?api\s+key",
]

COMPILED_INJECTION_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in INJECTION_PATTERNS
]


def detect_prompt_injection(text: str) -> bool:
    """
    Detect common prompt injection attempts.
    """

    return any(
        pattern.search(text)
        for pattern in COMPILED_INJECTION_PATTERNS
    )


# ----------------------------------
# 2. HR/IT Scope Detection
# ----------------------------------

HR_IT_KEYWORDS = [
    "human resources",
    "employee",
    "employees",
    "leave",
    "vacation",
    "sick leave",
    "casual leave",
    "annual leave",
    "payroll",
    "salary",
    "payslip",
    "benefits",
    "onboarding",
    "offboarding",
    "attendance",
    "working hours",
    "work from home",
    "remote work",
    "holiday",
    "holidays",
    "resignation",
    "recruitment",
    "handbook",
    "company policy",
    "it support",
    "technical support",
    "password",
    "vpn",
    "phishing",
    "malware",
    "cybersecurity",
    "security incident",
    "laptop",
    "computer",
    "software",
    "hardware",
    "network",
    "email",
    "account access",
    "printer",
    "wifi",
    "wi-fi",
    "employee id",
    "human resources",
    "hr policy",
    "hr policies",
    "hr department",
    "it policy",
    "it policies",
    "it department",
    "it helpdesk",
    "it help desk",
    "information technology",
]

EMPLOYEE_ID_PATTERN = re.compile(
    r"\bE\d{3}\b",
    re.IGNORECASE
)


def is_hr_it_related(text: str) -> bool:
    """
    Check whether the question belongs to HR or IT.
    """

    normalized_text = text.lower()

    if EMPLOYEE_ID_PATTERN.search(text):
        return True

    return any(
        keyword in normalized_text
        for keyword in HR_IT_KEYWORDS
    )


# ----------------------------------
# 3. Input Validation
# ----------------------------------

def validate_user_input(text: str) -> str | None:
    """
    Validate employee input before invoking the agent.

    Returns:
        None if input is allowed.
        Rejection message if input is blocked.
    """

    if not text or not text.strip():
        return "Please enter a question."

    if len(text) > 2000:
        return "Your question is too long. Please shorten it."

    if detect_prompt_injection(text):
        return (
            "I cannot process requests that attempt to override "
            "my security instructions."
        )

    if not is_hr_it_related(text):
        return (
            "I can only assist with GoAified HR and IT-related "
            "questions."
        )

    return None


# ----------------------------------
# 4. PII Detection and Redaction
# ----------------------------------

PII_PATTERNS = {

    "EMAIL": re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    ),

    "PHONE": re.compile(
        r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)"
    ),

    "AADHAAR": re.compile(
        r"(?<!\d)\d{4}\s?\d{4}\s?\d{4}(?!\d)"
    ),

    "PAN": re.compile(
        r"\b[A-Z]{5}\d{4}[A-Z]\b",
        re.IGNORECASE
    ),
}


def redact_pii(text: str) -> str:
    """
    Redact common sensitive personal identifiers.
    """

    for pii_type, pattern in PII_PATTERNS.items():

        text = pattern.sub(
            f"[REDACTED_{pii_type}]",
            text
        )

    return text