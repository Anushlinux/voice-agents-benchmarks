"""Explicit implementation status. This is not an account access or network probe."""


def scaffold_status() -> dict[str, object]:
    return {
        "stage": "implemented_unqualified",
        "live_calls_supported": False,
        "explicit_live_command_available": True,
        "qualification": "No live provider proof is recorded by this installation.",
        "integrations": {
            "controller": "implemented",
            "caller": "openai_realtime_unqualified",
            "browser": "chromium_livekit_unqualified",
            "phone": "plivo_unqualified",
            "rumik": "hosted_target_unqualified",
            "business": "postgresql",
            "evidence": "local_and_s3",
            "evaluation": "rules_model_and_review",
        },
    }
