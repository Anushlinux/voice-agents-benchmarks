import {Room, RoomEvent, Track, LocalAudioTrack} from 'livekit-client';

const room = new Room({adaptiveStream: false, dynacast: false});
const context = new AudioContext({sampleRate: 48000});
let microphone;
let delivered = {};
let pendingSamples = 0;
let eventChain = Promise.resolve();
let queuedEvents = 0;
let failed = false;
const clears = new Map();

function emit(event) {
  if (failed) return;
  if (queuedEvents >= 250) {
    failed = true;
    window.benchEvent({type: 'bridge_error', reason: 'event_queue_overflow'});
    room.disconnect();
    return;
  }
  queuedEvents++;
  const observed = performance.now();
  eventChain = eventChain.then(() => window.benchEvent({
    ...event, bridge_delay_ms: performance.now() - observed,
  })).finally(() => queuedEvents--);
  eventChain.catch(() => { failed = true; room.disconnect(); });
}

await context.audioWorklet.addModule('/audio-worklet.js');
microphone = new AudioWorkletNode(context, 'benchmark-audio', {
  processorOptions: {mode: 'play'}, outputChannelCount: [1]});
microphone.port.onmessage = ({data}) => {
  if (data.type === 'cleared') {
    pendingSamples = 0;
    clears.get(data.id)?.();
    clears.delete(data.id);
  } else if (data.type === 'played') {
    delivered[data.item] = (delivered[data.item] || 0) + data.samples;
    pendingSamples -= data.samples;
    emit(data);
  } else emit(data);
};
const destination = context.createMediaStreamDestination();
microphone.connect(destination);

function captureStream(stream) {
  const source = context.createMediaStreamSource(stream);
  const capture = new AudioWorkletNode(context, 'benchmark-audio', {
    processorOptions: {mode: 'capture'}, outputChannelCount: [1]});
  capture.port.onmessage = ({data}) => emit(data);
  const muted = context.createGain();
  muted.gain.value = 0;
  source.connect(capture).connect(muted).connect(context.destination);
}
room.on(RoomEvent.TrackSubscribed, (track) => {
  if (track.kind !== Track.Kind.Audio) return;
  captureStream(new MediaStream([track.mediaStreamTrack]));
});
room.on(RoomEvent.Disconnected, () => emit({type: 'disconnected'}));

window.bridge = {
  async join(call) {
    await context.resume();
    await room.connect(call.host, call.token);
    await room.localParticipant.publishTrack(new LocalAudioTrack(destination.stream.getAudioTracks()[0]),
      {source: Track.Source.Microphone});
  },
  push(pcm, item) {
    const binary = atob(pcm);
    if (pendingSamples + binary.length / 2 > 48000 * 5)
      throw new Error('Browser playback queue overflow');
    const bytes = Uint8Array.from(binary, c => c.charCodeAt(0));
    const view = new DataView(bytes.buffer);
    const samples = new Float32Array(bytes.length / 2);
    for (let i = 0; i < samples.length; i++) samples[i] = view.getInt16(i * 2, true) / 32768;
    pendingSamples += samples.length;
    microphone.port.postMessage({type: 'push', samples, item});
  },
  async clear() {
    const id = crypto.randomUUID();
    await new Promise(resolve => {
      clears.set(id, resolve);
      microphone.port.postMessage({type: 'clear', id});
    });
    await eventChain;
    return Object.fromEntries(Object.entries(delivered).map(([k, v]) => [k, Math.floor(v / 48)]));
  },
  async drain() {
    while (pendingSamples > 0) await new Promise(resolve => setTimeout(resolve, 20));
    await eventChain;
  },
  async close() { await this.clear(); await room.disconnect(); await context.close(); },
  // Local validation bypasses room signaling but uses the real browser audio worklet.
  async testStart() { await context.resume(); microphone.connect(context.destination); },
  testInput() {
    const oscillator = context.createOscillator();
    const stream = context.createMediaStreamDestination();
    oscillator.frequency.value = 440;
    oscillator.connect(stream);
    captureStream(stream.stream);
    oscillator.start();
  },
};
