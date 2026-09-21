// Preserve every audio event, amortizing bridge/storage work when events accumulate.
export class EventQueue {
  constructor(send, fail, now = () => performance.now()) {
    this.send = send; this.fail = fail; this.now = now;
    this.pending = []; this.running = false; this.failed = false;
    this.enqueued = 0; this.completed = 0; this.waiters = [];
  }
  emit(event) {
    if (this.failed) return;
    if (this.enqueued - this.completed >= 250) {
      this.abort('event_queue_overflow'); return;
    }
    this.pending.push({event, observed: this.now(), sequence: ++this.enqueued});
    if (!this.running) void this.pump();
  }
  async pump() {
    this.running = true;
    try {
      while (this.pending.length && !this.failed) {
        const batch = this.pending.splice(0, 8);
        await this.send({type: 'batch', events: batch.map(({event, observed}) => ({
          ...event, bridge_delay_ms: this.now() - observed,
        }))});
        this.completed = batch.at(-1).sequence;
        this.settle();
      }
    } catch { this.abort('event_delivery_failed'); }
    finally { this.running = false; }
  }
  abort(reason) {
    if (this.failed) return;
    this.failed = true;
    this.settle();
    this.fail(reason);
  }
  settle() {
    this.waiters = this.waiters.filter(waiter => {
      if (this.failed) waiter.reject(new Error('Audio evidence delivery failed'));
      else if (waiter.sequence <= this.completed) waiter.resolve();
      else return true;
      return false;
    });
  }
  drain() {
    return new Promise((resolve, reject) => {
      this.waiters.push({sequence: this.enqueued, resolve, reject});
      this.settle();
    });
  }
}
