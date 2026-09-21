// Passive observations only: these events never enter the counterpart's hearing.
export function observeTargetText(room, roomEvent, context, emit, audioParticipants) {
  // Partial transcripts can consume the text budget early in a call. Reserve a
  // separate bounded lane for recognized input and generation/synthesis lifecycle.
  const budgets = {
    text: {count: 0, bytes: 0, capped: false, limit: 512},
    generation: {count: 0, bytes: 0, capped: false, limit: 2048},
  };
  const observe = (kind, participant, payload, lane = 'text') => {
    const budget = budgets[lane];
    const size = JSON.stringify(payload).length;
    if (budget.count >= budget.limit || budget.bytes + size > 1024 * 1024) {
      if (!budget.capped) emit({type: 'target_text_observation', kind: 'capture_limit', lane,
        audio_context_seconds: context.currentTime, performance_ms: performance.now()});
      budget.capped = true;
      return;
    }
    budget.count++;
    budget.bytes += size;
    emit({type: 'target_text_observation', kind, lane, ...payload,
      participant_identity: participant?.identity ?? null,
      remote_audio_participant: audioParticipants.has(participant?.identity),
      audio_context_seconds: context.currentTime, performance_ms: performance.now(),
      boundary: 'client_event_received_not_provider_generation'});
  };
  room.on(roomEvent.TranscriptionReceived, (segments, participant, publication) => {
    for (const segment of segments) observe('transcription_segment', participant, {
      segment_id: segment.id, text: segment.text, final: segment.final,
      track_id: publication?.trackSid ?? null,
    });
  });
  room.on(roomEvent.DataReceived, (data, participant, kind, topic) => {
    if (data.length > 16384) {
      observe('data_packet_omitted', participant, {bytes: data.length, topic});
      return;
    }
    // Preserve the original envelope. This routes diagnostic events only; it
    // neither triggers a response nor sends text to the counterpart.
    const text = new TextDecoder().decode(data);
    let lane = 'text';
    try {
      const packet = JSON.parse(text);
      const lifecycle = new Set(['bot-llm-started', 'bot-llm-stopped',
        'user-llm-text', 'bot-tts-started', 'bot-tts-stopped',
        'user-mute-started', 'user-mute-stopped',
        'bot-started-speaking', 'bot-stopped-speaking', 'bot-interrupted',
        'user-started-speaking', 'user-stopped-speaking']);
      if (audioParticipants.has(participant?.identity) && packet?.label === 'rtvi-ai' &&
          (lifecycle.has(packet.type) || (packet.type === 'metrics' &&
            (Array.isArray(packet.data?.tokens) || Array.isArray(packet.data?.ttfb)))))
        lane = 'generation';
    } catch { /* Unknown packets remain raw text observations. */ }
    observe('data_packet', participant, {text, topic}, lane);
  });
  // Newer LiveKit agents can publish text streams instead of legacy segments.
  room.registerTextStreamHandler?.('lk.transcription', async (reader, participant) => {
    try {
      for await (const text of reader) observe('transcription_stream_chunk', participant, {
        stream_id: reader.info.id, text,
        attributes: reader.info.attributes ?? {}, topic: 'lk.transcription',
      });
    } catch {
      observe('transcription_stream_error', participant, {stream_id: reader.info.id});
    }
  });
}
