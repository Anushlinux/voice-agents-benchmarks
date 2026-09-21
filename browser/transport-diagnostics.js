// Metadata only: never export tokens, candidate addresses, or participant identities.
const fields = [
  'timestamp', 'ssrc', 'packetsReceived', 'packetsSent', 'packetsLost',
  'bytesReceived', 'bytesSent', 'jitter', 'jitterBufferDelay',
  'jitterBufferEmittedCount', 'concealedSamples', 'silentConcealedSamples',
  'totalSamplesReceived', 'totalSamplesDuration', 'totalAudioEnergy', 'audioLevel',
];

export function audioStats(report) {
  const result = [];
  report?.forEach(row => {
    if (!['inbound-rtp', 'outbound-rtp'].includes(row.type)) return;
    if ((row.kind || row.mediaType) !== 'audio') return;
    const clean = {type: row.type};
    for (const key of fields) {
      if (typeof row[key] === 'number' && Number.isFinite(row[key])) clean[key] = row[key];
    }
    result.push(clean);
  });
  return result;
}

export class TransportDiagnostics {
  constructor(emit, context) {
    this.emit = emit;
    this.context = context;
    this.tracks = new Map();
    this.active = true;
    this.pending = null;
    this.timer = null;
  }

  event(name, details = {}) {
    if (!this.active) return;
    this.emit({type: 'transport_observation', name, ...details,
      performance_ms: performance.now(), audio_context_seconds: this.context.currentTime,
      audio_context_state: this.context.state, audio_context_rate: this.context.sampleRate,
      stats_timestamp_clock: 'browser-rtc-stats'});
  }

  add(id, track, direction) {
    this.tracks.set(id, {track, direction});
    this.event('track_observed', {track_id: id, direction});
  }

  remove(id) {
    this.tracks.delete(id);
    this.event('track_removed', {track_id: id});
  }

  start() {
    if (this.timer || !this.active) return;
    this.event('diagnostics_started');
    this.timer = setInterval(() => { void this.sample(); }, 1000);
  }

  async sample() {
    if (!this.active || this.pending) return;
    this.pending = this.collect();
    try { await this.pending; } finally { this.pending = null; }
  }

  async collect() {
    await Promise.all([...this.tracks].map(async ([id, {track, direction}]) => {
      let timeout;
      try {
        const report = await Promise.race([
          track.getRTCStatsReport(),
          new Promise((_, reject) => { timeout = setTimeout(() => reject(new Error()), 750); }),
        ]);
        const rows = audioStats(report);
        const media = track.mediaStreamTrack;
        this.event('audio_transport_stats', {track_id: id, direction,
          status: rows.length ? 'available' : 'unavailable', rows,
          media_state: media?.readyState ?? null, muted: media?.muted ?? null,
          enabled: media?.enabled ?? null});
      } catch {
        this.event('audio_transport_stats', {track_id: id, direction,
          status: 'unavailable', reason: 'stats_failed_or_timed_out', rows: []});
      } finally { clearTimeout(timeout); }
    }));
  }

  async stop() {
    clearInterval(this.timer);
    this.timer = null;
    await this.pending;
    this.event('diagnostics_stopped');
    this.active = false;
    this.tracks.clear();
  }
}
