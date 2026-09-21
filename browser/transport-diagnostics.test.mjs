import {test} from 'node:test';
import assert from 'node:assert/strict';
import {audioStats, TransportDiagnostics} from './transport-diagnostics.js';

const context = {currentTime: 7, state: 'running', sampleRate: 48000};

test('exports only audio counters, excluding credentials and network addresses', () => {
  const rows = new Map([
    ['a', {type: 'inbound-rtp', kind: 'audio', packetsReceived: 100, timestamp: 123,
      address: 'private-address', token: 'private-token'}],
    ['b', {type: 'local-candidate', address: 'private-address'}],
    ['c', {type: 'outbound-rtp', kind: 'video', bytesSent: 900}],
  ]);
  assert.deepEqual(audioStats(rows), [{type: 'inbound-rtp', timestamp: 123, packetsReceived: 100}]);
});

test('records unavailable statistics without turning them into a bridge failure', async () => {
  const events = [];
  const diagnostics = new TransportDiagnostics(e => events.push(e), context);
  diagnostics.add('incoming', {getRTCStatsReport: async () => { throw new Error('secret'); }}, 'incoming');
  await diagnostics.sample();
  const sample = events.find(e => e.name === 'audio_transport_stats');
  assert.equal(sample.status, 'unavailable');
  assert.equal(sample.audio_context_seconds, 7);
  assert.equal(JSON.stringify(events).includes('secret'), false);
  await diagnostics.stop();
});

test('overlapping samples coalesce and shutdown prevents late observations', async () => {
  let resolve;
  let reads = 0;
  const events = [];
  const diagnostics = new TransportDiagnostics(e => events.push(e), context);
  diagnostics.add('a', {getRTCStatsReport() {
    reads += 1; return new Promise(r => { resolve = r; });
  }}, 'incoming');
  const first = diagnostics.sample();
  await diagnostics.sample();
  assert.equal(reads, 1);
  const stopped = diagnostics.stop();
  resolve(undefined);
  await first;
  await stopped;
  const count = events.length;
  await diagnostics.sample();
  diagnostics.event('late');
  assert.equal(events.length, count);
});
