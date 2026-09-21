from types import SimpleNamespace

from voice_bench.evaluation.speech_support import SpeechClaim, support_issue


def test_wrong_speaker_cannot_invalidate_employee():
    windows = [
        dict(source_id="speech-window-1", speaker="target", text="Reference FE7C5C5"),
        dict(source_id="speech-window-2", speaker="counterpart", text="Reference SIM-6DDFE7C5C5"),
    ]
    metric = SimpleNamespace(
        name="counterpart_validity",
        status="not_met",
        evidence=("speech-window-1", "speech-window-2"),
    )
    claim = SpeechClaim(source_id="speech-window-1", speaker="counterpart", quote="FE7C5C5")
    assert "wrong speaker" in support_issue(metric, [claim], windows)
    assert "assessed counterpart" in support_issue(
        metric, [claim.model_copy(update={"speaker": "target"})], windows
    )
    claim = SpeechClaim(source_id="speech-window-2", speaker="counterpart", quote="SIM-6DDFE7C5C5")
    assert support_issue(metric, [claim], windows) is None
    assert "does not occur" in support_issue(
        metric, [claim.model_copy(update={"quote": "XY123"})], windows
    )
    assert "No quoted speech" in support_issue(metric, [], windows)
    metric.status = "uncertain"
    assert support_issue(metric, [], windows) is None


def test_asr_punctuation_does_not_change_quote_support():
    windows = [dict(source_id="speech-window-1", speaker="target", text="नमस्ते.")]
    metric = SimpleNamespace(
        name="target_role_fidelity", status="met", evidence=("speech-window-1",)
    )
    claim = SpeechClaim(source_id="speech-window-1", speaker="target", quote="नमस्ते।")
    assert support_issue(metric, [claim], windows) is None
    assert support_issue(metric, [claim.model_copy(update={"quote": "Namaste"})], windows)
