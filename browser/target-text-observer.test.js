import test from 'node:test';
import assert from 'node:assert/strict';
import {observeTargetText} from './target-text-observer.js';

test('preserves partial/final distinction, source identity and client audio clock', () => {
  const handlers = {}, observations = [];
  const events = {TranscriptionReceived: 'transcription', DataReceived: 'data'};
  observeTargetText({on: (key, fn) => handlers[key] = fn}, events,
    {currentTime: 4.25}, event => observations.push(event), new Set(['target']));
  handlers.transcription([{id: 'response-1', text: 'Hello', final: false}],
    {identity: 'target'}, {trackSid: 'audio-1'});
  handlers.transcription([{id: 'response-1', text: 'Hello there', final: true}],
    {identity: 'unknown'});
  assert.equal(observations[0].audio_context_seconds, 4.25);
  assert.equal(observations[0].final, false);
  assert.equal(observations[1].final, true);
  assert.equal(observations[0].remote_audio_participant, true);
  assert.equal(observations[1].remote_audio_participant, false);
  assert.equal(observations[0].boundary, 'client_event_received_not_provider_generation');
});

test('bounds telemetry without stopping audio or treating data as generated tokens', () => {
  const handlers = {}, observations = [];
  observeTargetText({on: (key, fn) => handlers[key] = fn},
    {TranscriptionReceived: 'transcription', DataReceived: 'data'},
    {currentTime: 0}, event => observations.push(event), new Set());
  handlers.data(new Uint8Array(20000), {identity: 'other'}, null, 'large');
  for (let i = 0; i < 600; i++) handlers.data(new TextEncoder().encode('hello'), null);
  assert.equal(observations.length, 513);
  assert.equal(observations[0].kind, 'data_packet_omitted');
  assert.equal(observations[1].kind, 'data_packet');
  assert.equal(observations.at(-1).kind, 'capture_limit');
});

test('records streaming chunks at reception instead of waiting for final text', async () => {
  let handler;
  const observations = [], clock = {currentTime: 1};
  observeTargetText({on() {}, registerTextStreamHandler(topic, fn) {
    assert.equal(topic, 'lk.transcription'); handler = fn;
  }}, {}, clock, event => observations.push(event), new Set(['target']));
  const reader = {info: {id: 'stream-1', attributes: {origin: 'provider'}},
    async *[Symbol.asyncIterator]() {
      yield 'First';
      clock.currentTime = 3;
      yield ' second';
    }};
  await handler(reader, {identity: 'target'});
  assert.deepEqual(observations.map(e => e.audio_context_seconds), [1, 3]);
  assert.deepEqual(observations.map(e => e.text), ['First', ' second']);
  assert.ok(observations.every(e => e.kind === 'transcription_stream_chunk'));
});

test('transcript exhaustion cannot hide final target generation usage or stop', () => {
  const handlers = {}, observations = [];
  observeTargetText({on: (key, fn) => handlers[key] = fn},
    {TranscriptionReceived: 'transcription', DataReceived: 'data'},
    {currentTime: 12}, event => observations.push(event), new Set(['target']));
  const send = (packet, identity = 'target') => handlers.data(
    new TextEncoder().encode(JSON.stringify(packet)), {identity});
  for (let i = 0; i < 600; i++) send({label: 'rtvi-ai', type: 'user-transcription'});
  const usage = {label: 'rtvi-ai', type: 'metrics',
    data: {tokens: [{completion_tokens: 400, reasoning_tokens: 397}]}};
  send(usage, 'other'); // Unknown participants cannot consume the reserved lane.
  send(usage);
  send({label: 'rtvi-ai', type: 'bot-llm-stopped'});
  const generation = observations.filter(e => e.lane === 'generation');
  assert.equal(generation.length, 2);
  assert.deepEqual(JSON.parse(generation[0].text), usage);
  assert.equal(JSON.parse(generation[1].text).type, 'bot-llm-stopped');
  for (const type of ['user-llm-text', 'bot-tts-started', 'bot-tts-stopped',
    'user-mute-started', 'user-mute-stopped']) {
    send({label: 'rtvi-ai', type, data: {text: 'The actual received question'}});
    assert.equal(observations.at(-1).lane, 'generation');
    assert.equal(JSON.parse(observations.at(-1).text).type, type);
  }
  for (let i = 0; i < 2100; i++) send(usage);
  assert.equal(observations.filter(e => e.lane === 'generation').length, 2049);
  assert.equal(observations.at(-1).kind, 'capture_limit');
  assert.equal(observations.at(-1).lane, 'generation');
});
