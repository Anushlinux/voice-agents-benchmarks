# Chromium channel

`adapter.py` launches Chromium and serves the locally bundled LiveKit bridge from a loopback HTTP server. Build it with `npm --prefix browser ci --ignore-scripts` and `npm --prefix browser run build`. Local audio tests use the real worklets without contacting LiveKit or Rumik. See `docs/RUNNING.md` for live qualification.
