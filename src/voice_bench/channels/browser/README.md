# Browser channel

Planned implementation: Playwright-controlled Chromium with `livekit-client`
and a virtual microphone carrying the caller's generated audio.

1. Register a Rumik call and bind its call ID to the prepared run.
2. Redeem the registration token to obtain the web-call room credentials.
3. Join the room, publish caller audio, and subscribe to the target audio.
4. Capture outgoing and received audio independently, with named clocks and
   sample offsets. Listen continuously during playback.
5. Disconnect on completion or the controller's duration limit.

Keep long-lived API credentials out of the page. Rumik hosts the target and its
LiveKit room; we do not create a replacement agent or our own target room.

A native LiveKit client and Rumik's direct PCM WebSocket are possible diagnostic
adapters later, but neither should be labeled an actual Chromium browser test.
Native microphone hardware and room acoustics are outside this virtual-input path.

No browser runtime, JavaScript project, or browser binaries are installed yet.
Add and lock them when implementing this adapter.
