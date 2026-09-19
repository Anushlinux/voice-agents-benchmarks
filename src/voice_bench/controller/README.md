# Run controller

Implement the lifecycle here: prepared → connecting → in_conversation →
finalizing → grading → reviewed, with explicit failure records.

The controller composes the caller, channel, Rumik client, business environment,
and evidence store. It does not perform speech recognition or grade outcomes.

Before dialing, prepare isolated state and correlate the provider call ID with
the run. Enforce budgets, concurrency and maximum duration at runtime, including
failed attempts. Reserve capacity before dispatch. Do not retry an uncertain
call-start request until its original outcome is reconciled.

Never resume a broken conversation as the same attempt. Save its evidence and
create a fresh attempt if the configured policy permits one. A successful
hangup is not finalization: collect evidence and final state before grading.
