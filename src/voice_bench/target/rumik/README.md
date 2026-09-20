# Hosted Rumik target

`client.py` reads target configuration, registers browser calls, redeems single-use tokens and retrieves call records/recordings. Registration is bound to the attempt before redemption. No target deployment or custom Rumik-TTS agent is created.

The target must represent the user and consume the private `user_task` returned by the authenticated before-call endpoint. This callback contract is implemented locally; hosted consumption is unqualified. Target business tools are denied unless granted in `target_tools`. No Rumik outbound-call endpoint is implemented.
