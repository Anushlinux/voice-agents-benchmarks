import {Room, RoomEvent, Track, LocalAudioTrack} from 'livekit-client';
import {EventQueue} from './event-queue.js';
import {TransportDiagnostics} from './transport-diagnostics.js';
import {observeTargetText} from './target-text-observer.js';

const room = new Room({adaptiveStream: false, dynacast: false});
// Render against Chromium's silent clock, not the desktop's physical audio
// device. A muted gain alone still depends on that device starting correctly.
const context = new AudioContext({sampleRate: 48000, sinkId: {type: 'none'}});
let microphone;
let delivered = {};
let pendingSamples = 0;
let playbackGeneration = 0;
const events = new EventQueue(event => window.benchEvent(event), reason => {
  void window.benchEvent({type: 'bridge_error', reason});
  void room.disconnect();
});
const clears = new Map();
const captureElements = [];
const audioParticipants = new Set();
const nativeCaptures = [];
observeTargetText(room, RoomEvent, context, emit, audioParticipants);

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
// The worklet's mono output does not change MediaStreamDestination's default
// stereo format. Keep the actual track and LiveKit publication explicitly mono.
const destination = new MediaStreamAudioDestinationNode(context,
  {channelCount: 1, channelCountMode: 'explicit'});
microphone.connect(destination);
// A MediaStream destination alone can leave Chromium's graph at time zero
// despite context.state === 'running', until a consumer attaches. Publication
// needs the rendered track format first, so keep the graph pulled by a silent
// device-output branch. The published microphone still has only one audio path.
const microphoneClock = context.createGain();
microphoneClock.gain.value = 0;
microphone.connect(microphoneClock).connect(context.destination);

async function prepareMicrophone() {
  if (context.sinkId?.type !== 'none')
    throw new Error('Chromium silent audio output is required');
  await context.resume();
  // Chromium initially reports the destination's default stereo track even
  // after requesting mono. Its settings update when the graph first renders.
  // Wait before LiveKit reads the format and creates the publication.
  const deadline = performance.now() + 1000;
  while (destination.stream.getAudioTracks()[0].getSettings().channelCount !== 1 ||
      context.currentTime === 0) {
    if (performance.now() >= deadline) {
      diagnostics.event('microphone_not_ready', {
        channels: destination.stream.getAudioTracks()[0].getSettings().channelCount,
        silent_sink: context.sinkId?.type === 'none'});
      throw new Error('Synthetic microphone clock or format not ready');
    }
    await new Promise(resolve => setTimeout(resolve, 10));
  }
}

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
  // Independently retain the received track before Web Audio processing. This
  // does not feed the simulator and has its own recorder/clock boundary.
  if (MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) {
    const captureId = nativeCaptures.length;
    const recorder = new MediaRecorder(stream, {mimeType: 'audio/webm;codecs=opus'});
    let writes = Promise.resolve();
    let sequence = 0;
    const stopped = new Promise(resolve => {
      recorder.ondataavailable = event => {
        writes = writes.then(async () => {
          const bytes = new Uint8Array(await event.data.arrayBuffer());
          if (!bytes.length) return;
          let binary = '';
          for (let i = 0; i < bytes.length; i += 8192)
            binary += String.fromCharCode(...bytes.subarray(i, i + 8192));
          emit({type: 'native_audio', capture_id: captureId, sequence: sequence++,
            data: btoa(binary), bytes: bytes.length});
        });
      };
      recorder.onstop = () => writes.then(resolve, () => {
        diagnostics.event('native_capture_error', {capture_id: captureId});
        resolve();
      });
      recorder.onerror = () => diagnostics.event('native_capture_error', {capture_id: captureId});
    });
    nativeCaptures.push({recorder, stopped});
    diagnostics.event('native_capture_started', {capture_id: captureId,
      boundary: 'received_media_stream_before_web_audio'});
    recorder.start(1000);
  } else diagnostics.event('native_capture_unavailable');
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
  async prepare() {
    diagnostics.start();
    await prepareMicrophone();
    diagnostics.event('microphone_ready', {
      channels: destination.stream.getAudioTracks()[0].getSettings().channelCount,
      silent_sink: context.sinkId?.type === 'none'});
  },
  async join(call) {
    await prepareMicrophone();
    await room.connect(call.host, call.token);
    const track = new LocalAudioTrack(destination.stream.getAudioTracks()[0]);
    const publication = await room.localParticipant.publishTrack(track,
      {source: Track.Source.Microphone, forceStereo: false, dtx: true});
    const settings = track.mediaStreamTrack.getSettings();
    diagnostics.event('outgoing_audio_format', {channels: settings.channelCount,
      sample_rate_hz: settings.sampleRate, force_stereo: false, dtx: true});
    diagnostics.add(publication.trackSid, track, 'outgoing');
  },
  push(pcm, item, generation = 0) {
    if (generation !== playbackGeneration) return 'cancelled';
    const binary = atob(pcm);
    if (binary.length / 2 > 48000 * 5)
      throw new Error('Browser playback frame exceeds limit');
    // The audio device owns pacing. Keep a bounded lookahead instead of sleeping
    // for each chunk in Python and adding bridge latency to every spoken chunk.
    if (pendingSamples > 48000 || pendingSamples + binary.length / 2 > 48000 * 5)
      return 'full';
    const bytes = Uint8Array.from(binary, c => c.charCodeAt(0));
    const view = new DataView(bytes.buffer);
    const samples = new Float32Array(bytes.length / 2);
    for (let i = 0; i < samples.length; i++) samples[i] = view.getInt16(i * 2, true) / 32768;
    pendingSamples += samples.length;
    microphone.port.postMessage({type: 'push', samples, item});
    return 'queued';
  },
  async clear() {
    playbackGeneration++;
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
      try {
        for (const capture of nativeCaptures) {
          if (capture.recorder.state !== 'inactive') capture.recorder.stop();
          await capture.stopped;
        }
        await room.disconnect();
      }
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
  microphoneSettings() { return destination.stream.getAudioTracks()[0].getSettings(); },
  async testStart() {
    await this.prepare();
  },
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
