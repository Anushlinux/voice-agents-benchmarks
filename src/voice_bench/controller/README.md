# Attempt controller

`runner.py` creates fresh state, reserves limits, persists dispatch intent, runs the conversation and always enters finalization. Confirmed termination releases active concurrency; unknown termination retains it. `budget.py` keeps cumulative cost/minute reservations, including separate model-grading reservations. Recovery never redials automatically.
