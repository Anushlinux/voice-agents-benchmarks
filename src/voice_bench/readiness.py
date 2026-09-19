"""Explicit scaffold status. This is not an account access or network probe."""


def scaffold_status() -> dict[str, object]:
    return {
        "stage": "scaffold",
        "live_calls_supported": False,
        "integrations": {
            "controller": "not_implemented",
            "caller": "not_implemented",
            "browser": "not_implemented",
            "phone": "not_implemented",
            "rumik": "not_implemented",
            "business": "not_implemented",
            "evidence": "not_implemented",
            "evaluation": "not_implemented",
        },
    }
