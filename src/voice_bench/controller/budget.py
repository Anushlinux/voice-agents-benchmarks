"""Conservative reservations; unknown spend never becomes free capacity."""

from decimal import Decimal


def reserve(store, batch_id, run_id, config):
    limits = config.limits
    cost = config.runtime.cost_ceiling_inr_per_attempt
    seconds = limits.max_call_seconds + config.runtime.setup_timeout_seconds
    if limits.max_total_call_minutes <= 0 or limits.max_spend_inr <= 0 or cost <= 0:
        raise ValueError(
            "Live execution requires positive minute and spend budgets and cost ceiling"
        )
    if not config.runtime.rate_card_version:
        raise ValueError("A versioned conservative rate card is required")
    with store.locked_batch(batch_id) as (conn, batch):
        conn.execute("SELECT pg_advisory_xact_lock(81203500)")
        rows = conn.execute("SELECT id,data FROM vb_runs FOR UPDATE").fetchall()
        active = sum(bool(r["data"].get("reservation", {}).get("active")) for r in rows)
        reservations = batch.setdefault("reservations", {})
        if str(run_id) in reservations:
            raise ValueError("This attempt has already reserved capacity")
        used_seconds = sum(r["seconds"] for r in reservations.values())
        used_cost = sum((Decimal(r["cost"]) for r in reservations.values()), Decimal(0))
        if active >= limits.max_concurrent_calls:
            raise ValueError("Concurrency limit reached")
        if used_seconds + seconds > limits.max_total_call_minutes * 60:
            raise ValueError("Total minute budget exhausted")
        if used_cost + cost > limits.max_spend_inr:
            raise ValueError("Spending reservation exceeds budget")
        reservation = {
            "active": True,
            "seconds": seconds,
            "cost": str(cost),
            "components": {
                k: str(v) for k, v in config.runtime.cost_components_inr_per_attempt.items()
            },
        }
        reservations[str(run_id)] = reservation
        run = next(r["data"] for r in rows if str(r["id"]) == str(run_id))
        run["reservation"] = reservation
        conn.execute("UPDATE vb_runs SET data=%s WHERE id=%s", (store.json(run), run_id))


def release(store, run_id, confirmed):
    if confirmed:
        with store.locked_run(run_id) as run:
            if "reservation" in run:
                run["reservation"]["active"] = False
    # Keep cumulative minute and cost reservations: actual billing may arrive later.


def reserve_grading(store, batch_id, run_id, version, config):
    cost = config.judge.cost_ceiling_inr
    if cost <= 0 or config.limits.max_spend_inr <= 0 or not config.runtime.rate_card_version:
        raise ValueError("Model grading needs a positive cost ceiling and versioned rate card")
    key = f"grading/{run_id}/{version}"
    with store.locked_batch(batch_id) as (_, batch):
        reservations = batch.setdefault("reservations", {})
        if key in reservations:
            raise ValueError("This grading version was already dispatched; use a new version")
        total = sum((Decimal(r["cost"]) for r in reservations.values()), Decimal(0))
        frozen_limit = Decimal(batch["limits"].get("max_spend_inr", "0"))
        if total + cost > min(config.limits.max_spend_inr, frozen_limit):
            raise ValueError("Grading would exceed the funded spending budget")
        reservations[key] = {"cost": str(cost), "seconds": 0, "active": False}
