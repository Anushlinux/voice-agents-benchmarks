import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import test from 'node:test';

function setup(mode) {
  const messages = [];
  let Processor;
  const runtime = vm.createContext({sampleRate: 48000, currentFrame: 0,
    AudioWorkletProcessor: class {
      constructor() { this.port = {postMessage: message => messages.push(structuredClone(message))}; }
    }, registerProcessor: (_, value) => { Processor = value; }});
  vm.runInContext(readFileSync(new URL('./audio-worklet.js', import.meta.url), 'utf8'), runtime);
  const processor = new Processor({processorOptions: {mode}});
  return {processor, messages, step(input = new Float32Array(128)) {
    const output = new Float32Array(128);
    processor.process([[input]], [[output]]);
    runtime.currentFrame += 128;
    return output;
  }};
}

test('one second preserves every rendered sample with fewer than 50 progress messages', () => {
  const {processor, messages, step} = setup('play');
  processor.port.onmessage({data: {type: 'push', item: 'one', samples: new Float32Array(24000).fill(0.25)}});
  processor.port.onmessage({data: {type: 'push', item: 'two', samples: new Float32Array(24000).fill(0.5)}});
  for (let i = 0; i < 375; i++) step();
  processor.port.onmessage({data: {type: 'clear', id: 'cancel'}});
  assert.equal(messages.at(-1).type, 'cleared');
  const blocks = messages.filter(message => message.type === 'rendered_audio');
  assert.equal(blocks.length, 47); // Former path sent an additional 375 played messages.
  const rendered = blocks.flatMap(block => block.samples);
  assert.equal(rendered.length, 48000);
  assert.ok(rendered.slice(0, 24000).every(sample => sample === 0.25));
  assert.ok(rendered.slice(24000).every(sample => sample === 0.5));
  const totals = {};
  for (const [index, block] of blocks.entries()) {
    assert.equal(block.sample, index * 1024);
    for (const progress of block.progress) totals[progress.item] = (totals[progress.item] || 0) + progress.samples;
  }
  assert.deepEqual(totals, {one: 24000, two: 24000});
});

test('cancellation flushes partial progress before acknowledging and never plays queued remainder', () => {
  const {processor, messages, step} = setup('play');
  processor.port.onmessage({data: {type: 'push', item: 'cut', samples: new Float32Array(48000).fill(0.5)}});
  for (let i = 0; i < 3; i++) step();
  assert.equal(messages.length, 0);
  processor.port.onmessage({data: {type: 'clear', id: 'cancel'}});
  assert.equal(messages[0].samples.length, 384);
  assert.equal(messages[0].progress[0].samples, 384);
  assert.equal(messages[1].type, 'cleared');
  assert.ok(step().every(sample => sample === 0));
});

test('capture retains sample offsets and remains independent of playback', () => {
  const {messages, step} = setup('capture');
  for (let i = 0; i < 375; i++) step(new Float32Array(128).fill(0.125));
  assert.equal(messages.length, 50);
  for (const [index, message] of messages.entries()) {
    assert.equal(message.sample, index * 960);
    assert.equal(message.samples.length, 960);
    assert.ok(message.samples.every(sample => sample === 0.125));
  }
});
