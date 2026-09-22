# Plivo channel

`adapter.py` owns carrier dialing, 8 kHz mu-law media, playback checkpoints and hangup. The API validates provider signatures and an attempt-specific stream token. Route reservations and both providers' call IDs are persisted in PostgreSQL. No number is provisioned by this adapter.

This route dials into Rumik and is labeled `harness_connected`. OpenAI plays the other person while Rumik represents the user. It tests one conversation; it does not prove Rumik can select or dial a destination. `rumik_outbound` cases are rejected before dispatch.

When `runtime.target_sip_uri` is set, the carrier leg dials that SIP address directly instead of a rented number; the registered trunk number stays in `target_number`. Callback numbers are matched by subscriber digits, and stream start or failure details are retained as evidence.
