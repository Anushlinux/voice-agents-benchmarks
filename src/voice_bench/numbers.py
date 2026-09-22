"""Carrier endpoint comparison. Providers format the same subscriber differently."""

import re


def endpoint_digits(value):
    """Return the digits of a phone number or of a SIP URI's user part; empty if none."""
    if not value:
        return ""
    text = str(value).strip()
    if text.lower().startswith(("sip:", "sips:")):
        text = text.split(":", 1)[1].split("@", 1)[0].split(";", 1)[0]
    return re.sub(r"\D", "", text)


def same_endpoint(observed, expected):
    """Digits must exist and match exactly; only a plus sign, spacing or SIP wrapper may differ."""
    digits = endpoint_digits(observed)
    return bool(digits) and digits == endpoint_digits(expected)
