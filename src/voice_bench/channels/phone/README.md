# Plivo channel

`adapter.py` owns carrier dialing, 8 kHz mu-law media, playback checkpoints and hangup. The API validates provider signatures and an attempt-specific stream token. Route reservations and both providers' call IDs are persisted in PostgreSQL. No number is provisioned by this adapter.
