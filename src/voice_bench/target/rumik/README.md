# Rumik hosted target

Implement a narrow HTTP client here, with explicit calls rather than network
activity during imports or configuration validation.

Responsibilities:

- Inspect and snapshot the deployed agent, tools and variables before a batch.
- Check voice/language compatibility, account access and available capacity.
- Register browser calls before before-call tools execute, then obtain room access.
- Inspect call status and retrieve available transcripts and recordings.
- Copy recording bytes to the evidence store before signed URLs expire.

Browser and phone runs must use equivalent frozen target configurations. Confirm
the selected engine supports both; do not silently compare browser-only speech
to speech with a different phone engine. Tools and variables need their own
snapshots; an agent version alone does not freeze account-wide resources.

No live credentials, agent, telephone number, or account capabilities have been
verified by this scaffold. Do not rebuild Rumik's agent using its standalone TTS.

References (research context from 2026-09-20; recheck during implementation):

- https://docs.rumik.ai/manage-agents
- https://docs.rumik.ai/register-call
- https://docs.rumik.ai/web-call
- https://docs.rumik.ai/variables-and-tools
- https://docs.rumik.ai/outbound-calls
- https://docs.rumik.ai/voices
