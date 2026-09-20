from decimal import Decimal
from pathlib import Path

import pytest

from voice_bench.controller.budget import release, reserve, reserve_grading
from voice_bench.settings import load_config


def config():
    settings = load_config(Path("configs/local.toml"))
    return settings.model_copy(
        update={
            "limits": settings.limits.model_copy(
                update={"max_spend_inr": Decimal(2), "max_total_call_minutes": 20}
            ),
            "runtime": settings.runtime.model_copy(
                update={
                    "rate_card_version": "test-only",
                    "cost_ceiling_inr_per_attempt": Decimal(1),
                }
            ),
            "judge": settings.judge.model_copy(update={"cost_ceiling_inr": Decimal(1)}),
        }
    )


def test_unknown_termination_holds_concurrency_and_spend_is_cumulative(store, prepared):
    plans, (first, second) = prepared
    settings = config()
    reserve(store, plans[0].batch_id, first, settings)
    release(store, first, False)
    with pytest.raises(ValueError, match="Concurrency"):
        reserve(store, plans[0].batch_id, second, settings)
    release(store, first, True)
    reserve(store, plans[0].batch_id, second, settings)
    assert (
        sum(Decimal(r["cost"]) for r in store.batch(plans[0].batch_id)["reservations"].values())
        == 2
    )


def test_grading_respects_frozen_funding_and_does_not_repeat_versions(store, prepared):
    plans, (run_id, _) = prepared
    batch_id = plans[0].batch_id
    with store.locked_batch(batch_id) as (_, batch):
        batch["limits"]["max_spend_inr"] = "1"
    reserve_grading(store, batch_id, run_id, "v1", config())
    with pytest.raises(ValueError, match="already dispatched"):
        reserve_grading(store, batch_id, run_id, "v1", config())
    with pytest.raises(ValueError, match="funded"):
        reserve_grading(store, batch_id, run_id, "v2", config())
