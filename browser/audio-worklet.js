class BenchmarkAudio extends AudioWorkletProcessor {
  constructor(options) {
    super();
    this.mode = options.processorOptions.mode;
    this.queue = [];
    this.pending = [];
    this.renderPending = [];
    this.progress = [];
    this.renderStart = null;
    this.port.onmessage = ({data}) => {
      if (data.type === 'push') this.queue.push({...data, offset: 0});
      if (data.type === 'clear') {
        // Publish already rendered samples before acknowledging the clear.
        this.flushRendered();
        this.queue = [];
        this.port.postMessage({type: 'cleared', id: data.id});
      }
    };
  }
  flushRendered() {
    if (!this.renderPending.length) return;
    this.port.postMessage({type: 'rendered_audio', samples: this.renderPending,
      sample: this.renderStart, rate: sampleRate, progress: this.progress});
    this.renderPending = [];
    this.progress = [];
    this.renderStart = null;
  }
  process(inputs, outputs) {
    const out = outputs[0][0];
    if (this.mode === 'capture') {
      const input = inputs[0]?.[0];
      if (input) this.pending.push(...input);
      if (this.pending.length >= 960) {
        this.port.postMessage({type: 'received', samples: this.pending.splice(0, 960),
          sample: currentFrame + out.length - this.pending.length - 960, rate: sampleRate});
      }
    } else {
      if (this.renderStart === null) this.renderStart = currentFrame;
      let position = 0;
      while (position < out.length && this.queue.length) {
        const head = this.queue[0];
        const count = Math.min(out.length - position, head.samples.length - head.offset);
        out.set(head.samples.subarray(head.offset, head.offset + count), position);
        head.offset += count;
        position += count;
        const sample = currentFrame + position - count;
        const previous = this.progress[this.progress.length - 1];
        if (previous && previous.item === head.item && previous.sample + previous.samples === sample)
          previous.samples += count;
        else this.progress.push({item: head.item, samples: count, sample, rate: sampleRate});
        if (head.offset === head.samples.length) this.queue.shift();
      }
      this.renderPending.push(...out);
      if (this.renderPending.length >= 960) this.flushRendered();
    }
    return true;
  }
}
registerProcessor('benchmark-audio', BenchmarkAudio);
