# Hosted Rumik target

`client.py` reads target configuration, registers browser calls, redeems single-use tokens and retrieves call records/recordings. Registration is bound to the attempt before redemption. No target deployment or custom Rumik-TTS agent is created.

The target must represent the user and consume the private `user_task` returned by the authenticated before-call endpoint. This callback contract is implemented locally; hosted consumption is unqualified. Target business tools are denied unless granted in `target_tools`. The documented outbound client primitive is implemented with an explicit Plivo trunk and destination allowlist; it is not wired into execution. See [setup and remaining work](../../../../docs/RUMIK_PLIVO_SETUP.md).
