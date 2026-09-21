import {Room, RoomEvent, Track, LocalAudioTrack} from 'livekit-client';
import {EventQueue} from './event-queue.js';
import {TransportDiagnostics} from './transport-diagnostics.js';

const room = new Room({adaptiveStream: false, dynacast: false});
const context = new AudioContext({sampleRate: 48000});
let microphone;
let delivered = {};
let pendingSamples = 0;
const events = new EventQueue(event => window.benchEvent(event), reason => {
  void window.benchEvent({type: 'bridge_error', reason});
  void room.disconnect();
});
const clears = new Map();
const captureElements = [];
const audioParticipants = new Set();

function emit(event) {
  events.emit(event);
}

const diagnostics = new TransportDiagnostics(emit, context);
context.addEventListener('statechange', () => diagnostics.event('audio_context_state_changed'));
room.on(RoomEvent.ConnectionStateChanged, state => diagnostics.event('connection_state', {state}));
room.on(RoomEvent.Reconnecting, () => diagnostics.event('reconnecting'));
room.on(RoomEvent.Reconnected, () => diagnostics.event('reconnected'));
for (const [event, name] of [[RoomEvent.TrackMuted, 'track_muted'],
  [RoomEvent.TrackUnmuted, 'track_unmuted']]) {
  room.on(event, publication => diagnostics.event(name, {track_id: publication.trackSid}));
}
room.on(RoomEvent.TrackUnsubscribed, (track, publication) => {
  if (track.kind === Track.Kind.Audio) diagnostics.remove(publication.trackSid);
});

await context.audioWorklet.addModule('/audio-worklet.js');
microphone = new AudioWorkletNode(context, 'benchmark-audio', {
  processorOptions: {mode: 'play'}, outputChannelCount: [1]});
microphone.port.onmessage = ({data}) => {
  if (data.type === 'cleared') {
    pendingSamples = 0;
    clears.get(data.id)?.();
    clears.delete(data.id);
  } else if (data.type === 'rendered_audio') {
    for (const progress of data.progress || []) {
      delivered[progress.item] = (delivered[progress.item] || 0) + progress.samples;
      pendingSamples -= progress.samples;
    }
    emit(data);
  } else emit(data);
};
const destination = context.createMediaStreamDestination();
microphone.connect(destination);

async function captureStream(stream) {
  for (const track of stream.getAudioTracks()) {
    for (const name of ['mute', 'unmute', 'ended']) {
      track.addEventListener(name, () => diagnostics.event('media_track_' + name, {track_id: track.id}));
    }
  }
  // Chromium needs a playing media element to activate remote WebRTC audio,
  // even when samples are consumed through Web Audio rather than speakers.
  const element = document.createElement('audio');
  element.srcObject = stream;
  element.volume = 0;
  document.body.appendChild(element);
  captureElements.push(element);
  try { await element.play(); }
  catch { emit({type: 'bridge_error', reason: 'capture_playback_failed'}); return; }
  const source = context.createMediaStreamSource(stream);
  const capture = new AudioWorkletNode(context, 'benchmark-audio', {
    processorOptions: {mode: 'capture'}, outputChannelCount: [1]});
  capture.port.onmessage = ({data}) => emit(data);
  const muted = context.createGain();
  muted.gain.value = 0;
  source.connect(capture).connect(muted).connect(context.destination);
}
room.on(RoomEvent.TrackSubscribed, (track, publication, participant) => {
  if (track.kind !== Track.Kind.Audio) return;
  diagnostics.add(publication.trackSid, track, 'incoming');
  diagnostics.event('track_subscribed', {track_id: publication.trackSid,
    media_track_id: track.mediaStreamTrack.id});
  audioParticipants.add(participant.identity);
  captureStream(new MediaStream([track.mediaStreamTrack]));
});
room.on(RoomEvent.ParticipantDisconnected, (participant) => {
  if (audioParticipants.delete(participant.identity) && audioParticipants.size === 0)
    emit({type: 'target_left'});
});
room.on(RoomEvent.Disconnected, reason => {
  diagnostics.event('disconnected', {reason});
  emit({type: 'disconnected'});
});

window.bridge = {
  async join(call) {
    diagnostics.start();
    await context.resume();
    await room.connect(call.host, call.token);
    const track = new LocalAudioTrack(destination.stream.getAudioTracks()[0]);
    const publication = await room.localParticipant.publishTrack(track,
      {source: Track.Source.Microphone});
    diagnostics.add(publication.trackSid, track, 'outgoing');
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
    await events.drain();
    return Object.fromEntries(Object.entries(delivered).map(([k, v]) => [k, Math.floor(v / 48)]));
  },
  async drain() {
    while (pendingSamples > 0) await new Promise(resolve => setTimeout(resolve, 20));
    await events.drain();
  },
  async close() {
    diagnostics.event('cleanup_started');
    try { await this.clear(); }
    finally {
      try { await room.disconnect(); }
      finally {
        for (const element of captureElements) {
          element.pause(); element.srcObject = null; element.remove();
        }
        captureElements.length = 0;
        await context.close();
        await diagnostics.stop();
        await events.drain();
      }
    }
  },
  // Local validation bypasses room signaling but uses the real browser audio worklet.
  async testStart() { diagnostics.start(); await context.resume(); microphone.connect(context.destination); },
  testObserveTrack(id, track, direction) { diagnostics.add(id, track, direction); },
  testCaptureStream(stream) { captureStream(stream); },
  testInput() {
    const oscillator = context.createOscillator();
    const stream = context.createMediaStreamDestination();
    oscillator.frequency.value = 440;
    oscillator.connect(stream);
    captureStream(stream.stream);
    oscillator.start();
  },
};
