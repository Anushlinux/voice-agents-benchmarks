"""Explicit implementation status. This is not an account access or network probe."""


def scaffold_status() -> dict[str, object]:
    return {
        "stage": "personal_assistant_single_call_unqualified",
        "live_calls_supported": False,
        "explicit_live_command_available": True,
        "roles": {"target": "Rumik personal assistant", "counterpart": "simulated other person"},
        "execution_scope": "single_call_harness_connected",
        "unsupported_execution": ["rumik_outbound", "multi_call", "district_or_uber_app_control"],
        "qualification": "No live provider proof is recorded by this installation.",
        "integrations": {
            "controller": "implemented",
            "counterpart": "openai_realtime_with_scoped_business_tools_unqualified",
            "browser": "chromium_livekit_unqualified",
            "phone": "plivo_unqualified",
            "rumik": "hosted_target_unqualified",
            "business": "postgresql",
            "evidence": "local_and_s3",
            "evaluation": "rules_model_and_review",
            "jev": "saved_text_shadow_evaluator_unqualified",
            "rumik_setup": "offline_plan_and_snapshot_checks",
            "phone_carrier": "plivo_with_explicit_sip_trunk",
            "outbound": "client_primitive_only_no_executor",
        },
    }
