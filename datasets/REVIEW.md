# Dataset review — 20 September 2026

The collection has more packaging than substantive task diversity. The baseline
is useful, and the three challenge variants test some real skills. But all four
follow essentially the same booking problem with one matching destination.
They do not support a claim of difficult, broad Indian personal assistance.

This is a local file and implementation review. No provider calls, new
transcription, rescoring or human listening were performed. Difficulty judgments
below are design assessments, not measured target failure rates.

## 1. What is actually present

Before reorganization: **59 files, 44 JSON files, 648,611 bytes**, across three
packages. There are **four underlying task specifications, one task family,
and twelve generated task/profile combinations**. The twelve combinations reuse
those same four tasks under three counterpart styles.

| Underlying task | Real additional demand | What stays fixed |
| --- | --- | --- |
| Baseline | Reject unsuitable Bandra times; request authorized Khar fallback | Riya, eight people, 25 September 2026, 19:00, one regular table |
| Challenge 1 | Correct two spoken slips: time, then seating | Same inventory and matching Khar answer; no actual schedule change |
| Challenge 2 | Negotiate INR 13,200 down to INR 12,000; correct a time slip | Same booking; restaurant minimum equals user maximum |
| Challenge 3 | Add two guests without onion and garlic; seating slip and birthday detour | Same booking and price; kitchen always has sufficient capacity |

Evidence: the two [authored inputs](authored/), the
[generated cases](generated/), and archived
[profile preparation inventory](archive/2026-09-20/restaurant_design_v1/preparation.json).
All three individual `hard-N.json` files match the corresponding entries in
`variants.json`. The old `all-cases.json` equals baseline plus challenges. All
twelve files in the original baseline directory also have byte-identical copies
inside the hard-case package.

## 2. Findings, in order of importance

### The task is mostly finding one permitted answer

There are five physical options, but every case has the same single matching
Khar table. The fallback is already authorized, and the restaurant must disclose
matching inventory directly. Once Rumik reaches Khar, there is little planning
left. Direct disclosure is good simulator behavior; forcing needless rejection
of every distractor would add artificial length, not difficulty.

**Change:** introduce genuine alternatives with interacting constraints, changes
to an existing arrangement, and legitimate no-booking outcomes. Keep this
baseline for integration checks. Do not use duration or turn count as difficulty.

### Negotiation has an unusually convenient answer

Both paid cases open at INR 13,200. The restaurant floor and the private user cap
are both INR 12,000. The business tool accepts any eligible counteroffer in range,
so one offer at the cap can complete negotiation. There is no choice between a
cheaper package and lost inclusions, no conditional concession and no mandatory
fee discovered after an initial headline price.

Evidence: `dining_policy` in
[restaurant-challenges.json](authored/restaurant-challenges.json), and the
`counteroffer` branch in [dining.py](../src/voice_bench/business/dining.py).

**Change:** separate user ceilings from business floors; state the full payable
total; require checking concession conditions. Include a floor above the cap,
where preserving authority and declining is success. Do not make random refusal
or unexplained bargaining persistence the source of difficulty.

### There is no genuine date-change task

All inventory is on one date. The declared mistakes concern time or table layout;
they explicitly do not change state. The workflow starts with empty bookings and
has no amendment or cancellation operation. A time misread cannot stand in for
rescheduling a booking or reconciling a midnight pickup date.

**Change:** model the existing booking, permitted new dates, amendment cost and
the rule for retaining the old booking if a change fails. A fresh booking plus a
spoken claim that the old one was cancelled is insufficient.

### The Indian setting is real but narrow

Mumbai branches, rupees, Hinglish and the onion/garlic distinction are relevant.
The Korean restaurant itself is not a problem. The gap is that Indian context
rarely changes the decision: one free booking or one simple package concession
still solves everything. There are no apartment access windows, landmark-based
handover constraints, date-bound overnight pickups or itemized local service fees.

**Change:** use those operational details when they alter the correct action.
Treat all proposed businesses and policies as fictional; do not imply any named
platform or real Indian business follows them. Avoid equating “Indian” with
unreliable staff, constant haggling or one accent.

### The prompts partly coach the skill being measured

Rumik's challenge briefs explicitly say to correct inaccurate readbacks
immediately and interrupt if necessary. That is appropriate for an instructed
correction test, but gives away the capability under examination. The dietary
event also tells the employee to explain the vegetarian/onion/garlic distinction.
If Rumik already stated both exclusions clearly, no unresolved ambiguity remains.

**Change:** give Rumik ordinary user goals and permissions. Put challenge triggers
only in the counterpart/event specification. Do not hide constraints the user
would naturally provide. Keep coached and uncoached variants separately labeled.

### Speech errors and interruption are different measurements

The six declared events across the challenges comprise four misreads, one dietary
clarification and one birthday distraction. They create correction opportunities;
they do not prove any overlapping speech occurred. All actual business inventory
stays fixed. Some triggers depend on successful negotiation/dietary tools, so a
branch that never reaches those tools may never receive its planned event.

The existing audio-proof distinction is good: missing delivery is untested;
correction after the employee finishes is not observed interruption. An agent
can complete a task without interrupting. A birthday question can test whether
an unrelated answer is misused as consent, but it is a small detour rather than
a difficult planning problem.

**Change:** use meaningful correction opportunities and counterpart interruptions
of Rumik as separately labeled conditions. Record eligibility, trigger, audible
delivery, overlap, yielding and recovery. Judge interruption from aligned audio
and listening, never transcript order. Report reached and unreached opportunities
so early failures cannot quietly disappear from the coverage denominator.

### Helpful reference delivery is a separate test condition

The current [reservation tool](../src/voice_bench/business/reservations.py) returns
`single-reference-readback-v1`: identify one code, spell all characters, request
readback and repair it. The [counterpart runtime](../src/voice_bench/caller/openai_realtime.py)
also explicitly enforces that delivery. A different JSON brief alone will not
reliably create a naturally chunked, target-initiated clarification condition.

**Change:** preserve this as a clear-delivery control. A future version must select
and freeze either clear delivery or natural chunking. In the latter, the employee
answers clarification requests truthfully but does not automatically coach the
caller through a readback. Do not deliberately invent ambiguity where the issued
code is already clear. Exact identifier count and identity still matter.

This is a design dependency, not proof that a later run falsely passed. The saved
`report.md` referenced by this historical review describes five baseline attempts and no live hard-case
or profile results in its inventory. That report is historical evidence, not a
fresh provider query or a new survey of every possible result directory.

### Consent is tied to a long procedural recital

The challenge counterpart must read branch, date, time, timezone, party size,
table sizes, name, dining total, dietary terms and several zero fees. After a
correction or unrelated question it must prepare another full readback. The tool
description also demands every term. This creates repeated, formal speech even
when most terms have already been established.

**Change for new versions:** distinguish material final terms, facts established
earlier, and contextual metadata. Require fresh agreement to changes and all
financial obligations; preserve a booking name established earlier. Local
Asia/Kolkata metadata need not be spoken unless time-zone ambiguity matters.
Separate semantic agreement from adherence to an authored recital. Do not change
the old run's rubric or resolve its judge disagreement without the required review.

### A useful refusal is not represented as a successful case

The current importer requires exactly one matching slot. The challenge converter
requires a feasible expected booking and generates exact `bookings[0]` assertions.
It also accepts exactly the three existing case IDs. This is a dedicated fixture
builder, not a general personal-assistant dataset compiler.

Evidence: [restaurant_case.py](../src/voice_bench/restaurant_case.py) and
[restaurant_hard_cases.py](../src/voice_bench/restaurant_hard_cases.py).

**Change:** new outcome rules must accept authorized completion, a justified
no-action decision, or explicitly pending user approval, as appropriate to the
case. Reporting a blocker is not the same as getting approval. New task designs
cannot simply be appended to the current three-variant input.

## 3. Which JSON is useful and where it belongs

| Content | Decision | Reason |
| --- | --- | --- |
| Authored baseline and three variant specs | Two active authoring files | These define the actual tasks |
| Expanded execution inputs | Two active generated files | Required by the current runner; not another editing surface |
| Taskmaster record and attribution | One active source directory | Preserve origin and license, not a runtime script |
| Individual hard-1/2/3 specs, combined catalog | Archive | Duplicate views of the same cases |
| Twelve profile variants and six plans | Archive; generate on selection | Useful experiment outputs, not independent tasks |
| Blocker/preparation/validation JSON | Archive | Historical diagnostics, not current readiness or dataset content |
| Hashes, manifests, original transcript and copied baseline | Preserve in archive | Audit/provenance material; do not discard it as noise |

The original packages were archived intact. Active files are exact copies of
their selected sources; existing raw evidence and results remain untouched.
The working set now has five JSON files. This is a reduction in navigation noise,
not a claim that disk usage decreased: the archive intentionally retains history.

The original baseline manifest already references three absent handoff documents.
All present bytes match it; the matching documents exist in the archived hard-case
baseline. Both manifests in the hard-case package verify completely. This is a
packaging inconsistency, not evidence of altered conversation data.

There is also pre-existing generated-file drift. The current schema adds
`completion: counterpart` when loading these old cases. Regeneration has the same
loaded case contents but different bytes/default fields. All twelve archived
profile variants differ from a fresh generation in their recorded source hash:
the old hash excludes that completion field. Removing exactly that field
reproduces each old source hash, and all other loaded profile contents agree.
Preserve those snapshots instead of silently replacing their hashes. Freeze code
revision as well as case/profile version for reproducible experiments; a matching
version label alone does not establish an identical configuration.

## 4. Replacement design and implementation order

The [eight new case cards](proposed/indian-assistant-v2.md) specify private user
requests, counterpart facts, business options, meaningful changes, permissions
and acceptable outcomes. They are proposals, with zero executable new cases and
zero attempts. Several require business operations the current runner lacks.

Start with price/condition reasoning and truthful no-booking outcomes. Then add
atomic reservation amendment: either the new arrangement replaces the old one,
or the old one survives unchanged. Next implement the selected delivery, taxi or
service workflow. Defer the one multi-call design until task coordination and
approval delivery exist. Do not build all workflows just to claim eight examples.

Before a reported batch, freeze task version, business-policy version, target
configuration, counterpart instructions/model/voice, reference delivery, report
protocol, event rules and grading. Keep development examples separate from held-out
evaluation families; a profile or renamed city is not an independent held-out task.
Reject impossible or underspecified cases before dialing.

Report planned, attempted, valid, invalid, unresolved, passed, failed and not-run
counts separately, with a declared denominator. Also report task families and
event coverage. Judge simulator compliance independently from Rumik behavior.
Do not describe any of these new designs as empirically hard until they have been
implemented, reviewed and exercised in an explicitly authorized run.

## 5. Verification of this reorganization

See [VALIDATION.md](VALIDATION.md) for the checks run after moving the files.
Old validation documents in the archive retain their original dates and claims.

For current published results, use the [web-call](../reports/webcall/README.md) and [telephony](../reports/telephony/README.md) reports. The local root report snapshot has been preserved at `reports/archive/local-webcall-2026-09-21.md` (excluded from Git).
