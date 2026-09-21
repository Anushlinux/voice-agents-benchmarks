import assert from 'node:assert/strict';
import test from 'node:test';
import {EventQueue} from './event-queue.js';

test('slow delivery batches without losing order and drain waits for acknowledgement', async () => {
  const batches = [], acknowledgements = [];
  const queue = new EventQueue(async batch => {
    batches.push(batch.events);
    await new Promise(resolve => acknowledgements.push(resolve));
  }, () => assert.fail('Unexpected delivery failure'), () => 100);
  for (let sample = 0; sample < 20; sample++) queue.emit({type: 'received', sample});
  let drained = false;
  const drain = queue.drain().then(() => { drained = true; });
  assert.equal(batches.length, 1);
  assert.equal(drained, false);
  for (let count = 0; count < 4; count++) {
    acknowledgements.shift()();
    await new Promise(resolve => setImmediate(resolve));
  }
  await drain;
  assert.deepEqual(batches.map(b => b.length), [1, 8, 8, 3]);
  assert.deepEqual(batches.flat().map(e => e.sample), Array.from({length: 20}, (_, i) => i));
});

test('overflow and delivery errors fail drain instead of silently dropping evidence', async () => {
  for (const failure of ['overflow', 'delivery']) {
    const reasons = [];
    const queue = new EventQueue(() => failure === 'overflow'
      ? new Promise(() => {}) : Promise.reject(new Error('Synthetic sink failure')),
    reason => reasons.push(reason));
    queue.emit({type: 'received'});
    if (failure === 'overflow') for (let i = 0; i < 250; i++) queue.emit({type: 'received'});
    await assert.rejects(queue.drain(), /evidence delivery failed/);
    assert.deepEqual(reasons, [failure === 'overflow' ? 'event_queue_overflow' : 'event_delivery_failed']);
  }
});
