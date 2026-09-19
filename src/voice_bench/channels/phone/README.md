# Telephone channel

Planned initial direction: synthetic customer calls the Rumik-connected number.

Caller → our audio bridge → Plivo number A → telephone network → Rumik number B.
Speech flows both ways. The remote speech received through Plivo goes to the
caller; internal Rumik transcripts never substitute for it.

Implement Plivo call creation, answer instructions, bidirectional media streaming,
status callbacks, playback checkpoints, codec conversion, and explicit hangup.
Record carrier and Rumik IDs, number route, codec, timestamps, and stop reasons.
Validate callback authentication before exposing endpoints outside local development.

Before dialing, reserve an unambiguous run mapping using the target agent and
the caller number. Bind the Rumik call ID from the before-call tool request.
Begin with one call per number/agent mapping; reject ambiguous mapping instead
of guessing. A phone number is a routing key, not business identity verification.

Verify India provisioning, media routing, caller ID and account eligibility.
Rumik outbound calls to the simulator are an alternative direction; record that
as a different call-path configuration. Do not assume register-call supports PSTN.

Playback acknowledgment receipt is not an exact remote acoustic timestamp.
Never silence the target locally to make an interruption appear successful.
