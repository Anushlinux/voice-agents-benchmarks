# Repairing the conversation benchmark

## September 22: full ten-case cohorts on Mulberry 1.5 and 1.6 with prompt v8

Both Mulberry agents ran all ten natural restaurant cases once under prompt
`natural-caller-v8`, workflow 6 and the compact numeric reference. Nineteen of twenty
conversations completed with a private report; the pre-repair Mulberry batches managed
three of eleven. Formal outcomes under the frozen `natural-restaurant-full-v3` rubric:
1.5 passed 2, failed 4, unresolved 4 (2 invalid simulations); 1.6 passed 4, failed 2,
unresolved 4 (4 invalid simulations). The single inactivity timeout carried the old
signature, a first-turn generation of 400 tokens with 397 reasoning. Invalid simulations
now come mostly from `gpt-realtime` employee slips; Rumik's own failures are content
errors such as an ignored branch preference or an omitted term in the report.

Measurements now include time to first token, computed from the `rtvi-ai` lifecycle
packets Rumik publishes into the room and the browser stamps with its own clocks
(`evaluation/target_timing.py`, `full-cohort-metrics-v4-ttft`). Two views are reported:
per employee turn on the audio clock, directly comparable with TTFS, and per Rumik
generation from its own end-of-speech decision. Both include network transit. Per-attempt
reports were regenerated as `full-report-v2` without changing any grade. TTFS p50 was
2.2 s (1.5) and 2.4 s (1.6); TTFT per employee turn p50 1.6 s and 1.4 s; provider LLM
first byte 0.32 s on both.

The 1.6 cohort stopped itself after eight calls when Rumik's dashboard created an empty
draft identical to the active version; the worker treats any snapshot change as drift.
The two skipped cases ran as a supplementary batch under identical settings. Both agents,
both callback tools and their descriptions were restored and verified; temporary services
were stopped. The comparison, per-case tables, judge and Jev answers, findings and
evidence pointers are in `reports/p0-cohort-mulberry-20260922/README.md`.

## September 22: shrinking what Rumik must process per turn

Rumik publishes its own usage telemetry into the call room after every generation.
Across the eleven connected attempts that captured it, 9 of 30 generations stopped at
exactly 400 completion tokens; no generation ever exceeded 400. Seven of those nine had
3 or 4 visible tokens after 396 or 397 reasoning tokens, and each was followed by a
silent target turn. Every inactivity-timeout call whose capture did not overflow ended
on such a generation, including two that stalled on Rumik's first substantive turn.
Turns with up to 265 reasoning tokens always produced speech. The connected Mulberry
call flipped from four spoken turns (101–165 reasoning tokens) to three silent ones
(396–397) at the moment the phonetically spelled reference arrived as eight fragments
and the report had to be planned. The cap itself is hosted configuration that the
public agent schema does not expose; the harness can only reduce what each turn asks
the model to reason about. This is a mitigation, not a repair of the hosted limit.

Changes in this working tree:

- Workflow version `6` issues a six-digit reference (`SIM-482913`) derived from the
  same attempt/operation identity, and `natural-reference-v3` asks the employee to say
  it once in one short sentence as digit pairs. No phonetic alphabet, no per-character
  pauses. Versions 1–5 and all saved evidence keep their references and contracts.
  Evaluation reconstructs the reference by workflow version.
- Newly prepared cases are version `10` on workflow 6. A zero dietary count is no
  longer rendered as a constraint; nonzero counts are unchanged.
- The target prompt candidate `natural-caller-v7` is about 1,700 characters instead of
  3,000: one role block, five rules, six flow steps. The report step and the report tool
  ask for one or two sentences. Bindings, acknowledgement-before-report ordering,
  `report_saved` and `{{end_call}}` are unchanged. It is undeployed; deploying it means
  a new hosted version, an updated `target.prompt_sha256`, and updating the deployed
  report tool's descriptions to match `setup_plan`.
- The counterpart playbook states the reference once in one sentence and avoids lists,
  because the target's endpointer treats pauses of roughly a quarter second as turn ends.
- The interruption check tolerates the 1 ms resampling shortfall, so a fully played
  item is no longer labelled interrupted or truncated when Rumik speaks next.
- Generation diagnostics report the highest completion count seen and how many samples
  sat at it, so a live rerun can show whether any turn touched the ceiling.

None of this changes grades or historical results. In parallel, ask Rumik to raise the
completion limit or lower reasoning effort for this agent; that is the actual fix.

### Live result, one authorized call

The original Aditi Shah case ran once under this configuration with prompt
`natural-caller-v7` deployed temporarily (batch `a69330e8-6b2d-473a-9f29-08e19e92e912`).
Rumik stated the request, agreed to the offered terms, heard the reference spoken once,
filed the private report with the exact reference `SIM-441311`, said goodbye and hung up
itself; the harness confirmed termination. Duration 66 seconds, zero silence follow-ups.
Rumik's five generations used 342, 211, 211, 134 and 12 completion tokens; none reached
400 and none was reasoning-dominated. The employee turn carrying the reference lasted 7.9
seconds and became three target turns, against 19.5 seconds and eight turns before.

The automated grade is valid / failed for one reason: `user_report_accuracy`, because the
two-sentence report omitted date, time, name, party size and terms. That is a direct
consequence of the v7 wording. `natural-caller-v8` keeps the short shape but names the
booked terms; it is undeployed. The reference-clause grammar is now v2 so a report of the
form "reference SIM-441311" resolves. One call is not reliability proof; the ten-case set
has not been rerun. Details, counts, comparison and cleanup proof are in
`reports/p0-turn-budget-live-20260922/README.md`. Original version, callbacks and tool
descriptions were restored and verified; temporary services were stopped.

## September 22: Mulberry silence investigation

The saved ten-attempt Mulberry batch had seven inactivity timeouts, one browser
queue failure, one cancellation and one normal no-booking conclusion. Four calls
saved bookings, but only one delivered a private report. Three captured hosted
generations reported 400 completion tokens with 397 reasoning tokens before
silence. That suggests output-budget exhaustion, but the actual hosted limit and
finish reason are unavailable. Five calls exhausted the old diagnostic capture
budget. These observations do not establish a single cause for every call.

The counterpart now receives a structured, role-scoped playbook with explicit
lookup, offer, agreement, booking, acknowledgement and finish steps. The target
setup candidate `natural-caller-v6` makes acknowledgement, private reporting and
hangup explicit. It remains undeployed. Restaurant validation now permits the
existing bounded silence-recovery mechanism; the example enables one ten-second
follow-up. Exhausting recovery still fails to complete the conversation.

Target generation events have a separate bounded diagnostic allowance so partial
transcripts cannot hide final token usage. New diagnostics report the observed
reasoning-heavy signature without changing grades or claiming a confirmed cause.
Chromium tests also exposed a mono-track initialization race: publication now
waits for the requested mono format to become observable after rendering begins.

Validation: 335 Python tests passed with isolated PostgreSQL and real Chromium;
12 JavaScript tests passed. No new hosted call or paid evaluation was run. The
saved evidence audit, full prompt candidates and proposed one-call acceptance
gate are in `reports/p0-conversation-repair-20260922/README.md`. The P0 remains
open until a funded, explicitly authorized live conversation completes correctly.

## Latest investigation: transport evidence, not another prompt patch

Browser calls now record connection state, track lifecycle, audio-context state
and available incoming/outgoing audio packet statistics once per second. Statistics
are restricted to audio counters; credentials, network addresses and participant
identities are excluded. Unavailable statistics remain unavailable, without
changing audio delivery or inferring a target failure. Worker observation time,
browser performance time, audio sample time and statistics timestamps remain
separate. Sampling is bounded and stops during cleanup.

Full reports now include `diagnostics-v1.json`: observed task completion,
simulation validity, original automated outcome, established failure owner,
event anchors, audio references and remaining uncertainty. A missing report stays
visible even when the internal cause is unknown. These diagnostics do not rewrite
historical grades or infer remote hearing from local playback.

The first authorized Priya call used the same task, hosted prompt version 6 and
semantic turn detection as the previous rerun. Rumik said its greeting but did not
state the user's request. The employee's complete greeting appears in the hosted
transcript. Its playback passed integrity checks. Received packets continued,
the track stayed live and unmuted, and no bridge error was recorded. Nevertheless,
the browser recording contains 16.815 seconds of mutual silence before cleanup.
No reservation or private report was produced. All evaluation stages completed;
conversation acceptance failed and the original formal outcome remains unresolved.

This does not identify the internal hosted failure. The current documented Rumik
API exposes call records but no internal turn, generation or speech-synthesis
traces. No evidence-supported hosted setting change was found. The investigation
therefore stopped after one call rather than spending on unchanged repetitions.
INR 155 was reserved from the authorized INR 465 ceiling; reservations are not
invoices. The diagnostic package, evidence links, counts, costs and shutdown proof
are in `reports/conversation-foundation-20260921/`.

The dispatch source archive includes the dirty working tree. Future batches also
freeze an explicit source-file inventory and `source-snapshot.tar.gz`, including
the built browser JavaScript, in the batch artifacts. This automatic archive
addition was locally tested after the live call; it does not claim another live
qualification. Only source and dependency files are allowlisted for that archive.

## Priya call: turn-taking and ending repair

The saved Priya call exposed harness defects. A sub-second interruption was
committed as a complete turn under the 500 ms pause rule, and GPT repeated its
menu explanation. After Rumik's complete booking request, an internal offer
preparation timestamp forced a second agreement even though the employee had
already quoted those exact terms. Finally, explicit employee completion did not
end the browser call, leaving the silence watchdog to close it.

New cases use workflow 5 and case version 8. Exact unchanged terms exposed by a
recorded availability result may be accepted before the internal offer tool runs.
Full employee playback followed by caller speech remains required. Changed
prices, new dietary commitments, stale offers and missing evidence still fail.
The grader independently reconstructs the earlier quote from its tool operation
and event sequence; model arguments cannot supply this evidence. Structural
speech ordering does not prove the meaning of agreement, so semantic review remains.
Workflows 1–4 and historical evidence keep their original rules.

The shared audio harness waits for committed input, rechecks pending speech before
sending a response, and suppresses late audio/tools from interrupted responses.
A caller interruption during closing playback withdraws the finish action.
The new completion policy ends only after the report, explicit drained finish and
trailing quiet, with provider termination still verified. Tests specifically
requiring Rumik's own hangup retain their strict policy. Semantic turn detection
with low eagerness is required for new natural cases, preventing reuse of the old
500 ms profile. This can wait longer when an utterance sounds incomplete.

The browser stress test also exposed cumulative evidence-delivery backlog. Queued
audio observations now travel in small ordered batches, retaining every sample
timestamp and playback boundary. The original 20 ms audio blocks are unchanged;
there is no deliberate batching delay or enlarged overflow allowance.

See `reports/end-of-call-debug-20260921/README.md` for the trace and verification.
These changes have local regression proof, not a new live conversation result.
No hosted prompt was changed, no remote evaluation was run, and the Priya result
has not been retroactively relabeled as passing.

## Latest rerun outcome

The Aditi Shah rerun created one reservation and ended normally. The employee
explained separate paid meals; Rumik accepted the free table reservation. The full
offer, confirmation and clarification rendered, with no incomplete response or
unexplained cutoff and no mutual silence of ten seconds. Both judges completed.
The overall automated result is **failed**: the private report omitted `F` from
the reference. Independent employee-audio transcription and the hosted transcript
also omit it, so simulator pronunciation is a concern; exact acoustic attribution
still needs listening. A new workflow 4/case 7 pronunciation guide is locally
implemented but has not received another live run. See
`reports/harness-repair-rerun-20260921/README.md` for evidence and limits.

## Shared safeguards added after the Aditi Shah cutoff

The task renderer now keeps two kinds of financial obligation separate: a table
reservation charge and a dining-package price. Restaurant workflow 3 includes
explicit pricing scope in availability, offers and saved reservations. For a table
booking, the later meal bill is unknown, not zero. New zero-priced dining packages
and table-only options containing a purchased menu are rejected before a call.
Workflow versions 1 and 2 and historical evidence retain their original meaning.

The renderer also preserves the condition on the no-booking fallback. Previously,
`when_no_authorized_option_exists` lost its condition when converted to English,
so the assignment could simultaneously allow booking and say "Do not book."
New case version 6 says "Only if no authorized option exists" explicitly.

The shared caller prompt `natural-caller-v5` distinguishes availability, permission,
confirmed business action and private report delivery. It tells Rumik to hear the
complete terms, request the actual booking and reference, and finish the exchange
before reporting. These instructions cannot guarantee hosted model behavior.

The existing post-report inactivity fix is covered for both speakers and continuous
silent audio frames. Every new counterpart session saves per-item generated and
played durations. Full evaluation rejects conversation acceptance for unexplained
unplayed speech, incomplete generation or missing final playback evidence. Genuine
target interruptions are retained separately and still need semantic review. This
checks local rendering, not whether the remote service heard every word.

The authorized one-call rerun and its frozen synthetic meal estimate are recorded
under `reports/harness-repair-rerun-20260921/`. Earlier evidence is unchanged.

## Earlier functional test

Hosted version 5 (`natural-caller-v4`) was deployed and the Aditi Shah case ran once
with a 15-second silence limit. Rumik responded after about 3.91 seconds and sent
a private report, but no booking was made. The generated task wrongly scoped a
zero booking-charge limit as zero total spending, causing a refusal over later meal
payment. An absolute post-report hangup timer then cut off the employee's ongoing
clarification. Both judges completed; the simulation is invalid and the task outcome
is unresolved. This is not functional success. Evidence and recording are linked from
`reports/functional-run-20260921/README.md`.

Local corrections after that call scope table-only charges to the reservation in
newly prepared case version 5 and make the post-report deadline measure inactivity,
reset by received speech or actual employee playback. Continuous silent frames do
not reset it. These corrections passed 75 local checks but have not been run live.
The single-call limit was respected and all temporary infrastructure was stopped.

## Local follow-up: dietary-question stall

The September 21 call was inspected without another provider call. Rumik's assignment
already said zero guests needed food without onion/garlic, and the hosted transcript
contains the complete employee question. All 15.5 seconds of that question rendered.
The browser then captured about 46.6 seconds of near-digital silence (PCM16 peak 2),
without a later response cancellation or bridge error. Local audio capture does not
prove that remote audio packets continued arriving. The saved API record does not
expose hosted turn detection, generation or speech-synthesis events, so the internal
cause remains unproven. See `reports/dietary-stall-debug-20260921/README.md`.

Newly prepared cases now use restaurant workflow version 2: a dietary count is
optional and means requested accommodation, not personal diet. A table-only booking
does not require a dietary survey. Offer and rejected-booking results explain that
the employee must communicate the offer and obtain agreement. The existing consent
guard is retained. Version 1 and all saved evidence keep their original semantics.

The local `natural-caller-v4` prompt candidate distinguishes a question from a changed
offer, tells Rumik to answer known facts, and gives an honest path for unknown or
unrelated details. It has not been deployed or live-qualified. The previously tested
hosted version 4 still uses `natural-caller-v3`; these are different version labels.

## Current repair: explicit caller role and full evaluation

The caller profile is now `natural-caller-v3`. It restores explicit customer-assistant
behavior without scripting dialogue. Natural qualification requires the reviewed
prompt's SHA-256 in `target.prompt_sha256`, matching the deployed snapshot and the
existing authenticated task/report bindings. Generated constraints and permissions
are English statements; unknown authority fields are rejected rather than omitted.

Natural qualification disables silence nudges. Realtime voice activity detection
commits received speech, while one response coordinator handles response creation
and cancellation. Audio capture continues during tools, report submission and
closing playback. The 45-second inactivity boundary is a failure stop, not recovery.

`restaurant prepare-natural --automated-rubric` produces the separately versioned
`natural-restaurant-auto-v2` rubric. Text-supported checks may resolve through the
configured judge; acoustic naturalness and output-integrity listening remain separate
diagnostics. Historical `natural-restaurant-v1` retains its original human-review gate.

`batch run --live --with-evaluation --jev-rubric configs/restaurant-jev-rubric.json`
requires funded OpenAI and Jev stages before dialing. It reserves call, transcription/
Luna and Jev ceilings atomically, then runs rules → transcription/Luna → Jev → report
after termination and sealing. Each stage records failure without automatic retries.
Reports appear under `<artifact_root>/<batch_id>/full-report/README.md`; they contain
both judges, a recording, transcripts, business state, the private report and timing.
Browser silence measurements include both speakers and terminal silence, with no
ten-second censoring of long response gaps. Acoustic activity is not semantic turn
annotation. A ten-second unexplained silence prevents conversation-repair acceptance.

## September 21 single-call result

The frozen candidate was deployed as hosted Rumik version 4 and tested once with
the original Aditi Shah task. Rules, independent transcription, `gpt-5.6-luna` and
OpenRouter `typesafe/jev-1.13` all completed. The conversation did not qualify:
there was a 47.064-second mutual-silence interval, no committed reservation and no
private report. The 45-second inactivity stop fired and provider termination was
confirmed. The INR 155 reservation included every stage; no call was retried.

The independent transcript and the provider's transcript both show Rumik stating
the customer request. This attempt therefore gives evidence of correct initial
role behavior, not proof of a reliable conversation. The employee attempted to
book before communicating the offer; the business tool rejected that attempt.
Luna marked the simulation invalid. Jev's independent answers disagreed with
several Luna decisions, including role fidelity. Both answers remain in the report.
The hosted transcript contains the employee's complete final question, but cannot
establish why Rumik then stopped responding. Human listening remains pending.

The diagnostic report and recovery patch are in
`reports/repair-implementation-20260921T103008Z/`. The complete recording, both
judges, metrics, transcript and timing are in
`artifacts/21f9f199-11f5-4a41-a991-3b99b4f7b118/full-report/`.
Temporary Cloudflare and PostgreSQL infrastructure was stopped after evidence
and database archival. The deployed version remains recorded; its temporary
callback address is no longer running. Another call requires fresh authorization,
funding and configuration verification.

The earlier sections below document the preceding repair and its failed live probes.

The repair removes causes of artificial conversations that we control: cut-off
simulator speech, excessive browser bookkeeping, ungrounded injected mistakes,
scripted booking procedures, and grading that confuses one actor's evidence with
another's. It also supplies a revised Rumik prompt and private report-tool setup.
The hosted assistant still needs a newly authorized, funded qualification call.
Local tests cannot establish that its internal self-talk or silence has stopped.

The September 21 audit covered all ten saved live attempts, including three with
only setup or greeting evidence. Seven had two-sided conversation evidence. Two
infrastructure fixtures were accounted for separately. The local audit is at
`reports/conversation-root-cause-audit-20260921/README.md`. Raw recordings, sealed
cases, manifests, original transcripts and past grades remain unchanged.

## What changed and why

| Observed problem | Repair | What remains to verify |
| --- | --- | --- |
| Seven saved responses ended incomplete at exactly 512 output tokens, including six substantive challenge readbacks | Default counterpart limit is 2,048. New natural cases reject smaller limits. Any incomplete response records its details and ends as an invalid simulator attempt; proposed tools from that response never execute. | 2,048 is headroom, not a guarantee. Confirm completed responses and intelligible speech live. |
| Each challenge employee selected an early slot before establishing requested availability | A new workflow separates lookup, offer and booking. Lookup returns matching times separately from alternatives and does not select anything. Offers must come from a previous lookup. | The employee can still mishear or choose badly. Review its requests and speech independently. |
| Tool-count triggers injected a false time without establishing that the true time had been heard or agreed | Cases with `conversation_events` are now rejected before live execution. Historical parsing, evidence review and event-driver tests remain available. Natural cases use no injected speech. | Deliberate interruption/correction research needs a separately qualified design; this repair does not claim that coverage. |
| Playback progress created approximately 375 extra browser messages each second, on top of audio capture/render messages | The audio worklet combines exact per-item progress with rendered audio blocks. Python appends each block and its progress in one durable write. Cancellation flushes partial progress before acknowledging. | Local rendering is still not proof of remote perception. Slow or failing storage still stops an attempt rather than silently discarding evidence. |
| Calls remained silent for minutes | A 45-second configurable inactivity watchdog ends an idle conversation after generated speech has finished rendering. It records **unknown attribution**. | This bounds the failure; it does not diagnose or fix a hosted Rumik stall. Active tools/generation and queued playback remain governed by the outer attempt deadline. |
| The employee was pushed into recitals, compulsory spelling/readback and repeated confirmations | Natural briefs ask for truthful, relevant answers. Tools require current terms and observed speech ordering, but no prescribed words or full-field recital. One actual reference is delivered naturally; clarification is conditional. | Structural speech events cannot prove the meaning of consent. Human review remains required. |
| “Wait for user” was spoken in target audio | The reviewable Rumik prompt explicitly separates private reasoning from conversation, preserves constraints and changed terms, and requests brief clarification/recovery. A new listening check flags audible internal instructions. | The audit did not find that phrase in local prompts or datasets. The hosted cause remains unproven; the candidate must be deployed and tested. |
| Grading blamed Rumik for employee behavior or undisclosed facts | Judge instructions distinguish assignment, heard speech, tool facts and private inventory. Both evaluation paths now receive actual event anchors, report evidence and execution status. | Model assessments remain provisional. Human listening must check simulator consistency, consent, language and target speech. |
| Missing reports, transliterated names, and no-booking outcomes were mishandled | Natural scoring separates report presence from accuracy, routes uncertain name identity to review, supports useful refusal, and checks issued references independently. Reviews cannot override deterministic state checks or turn invalid execution into a target verdict. | An absent report on an interrupted call does not establish who caused the interruption. Unfamiliar reference prose still needs review. |
| The dataset strongly preferred one scripted path | The compiler accepts all equally valid outcomes, checks structured user preferences against physical inventory, and supports seven solvable and three no-booking cases. No minimum turns, mandatory bargaining, or artificial distractions. | These are ten authored restaurant scenarios, not representative real-world coverage or ten new results. |

## New conversation and business flow

Rumik receives the private user request, constraints and permissions through the
existing authenticated callback. The employee gets its own brief and restaurant
policies. It does not get the customer's hidden budget, task or grading answers.
The full inventory stays in the business environment until a scoped lookup exposes
relevant options. The grader can inspect all sides after the attempt.

1. `check_availability` takes the branches, date, party size and time range heard
   from the caller. It returns matching options and other-time alternatives in
   separate lists. The response never commits a booking.
2. `offer_reservation` returns the exact terms of a previously exposed option and
   the requested dietary count. An unavailable dietary commitment is rejected.
   Conditional menu/price options are exposed only when the employee reports that
   a relevant request was heard; this is auditable, not a semantic hearing detector.
3. The employee explains the relevant offer. Established facts can carry forward.
   A new offer replaces the previous offer; fresh speech evidence must follow it.
4. `record_reservation` saves the current offer and name after observed playback
   and a subsequent target response. It issues one reference. The tool does not
   consult private grading constraints: an erroneous but physically possible
   commitment is preserved so it can be detected, not silently corrected.
5. Rumik privately submits the outcome and material user requirements. The saved
   report is authenticated to the call and delivered task. A truthful no-booking
   report needs a supported reason, not a fabricated reference.

This remains a single harness-connected browser call to hosted Rumik. It is not
outbound dialing, a multi-call agent, a real restaurant booking or a training run.
No model weights were changed. The dataset supplies test situations and prompts.

## Versioning and preparation

The new workflow is `mock_restaurant_natural`, version `1`, with the
`natural-restaurant-v1` rubric. Old reservation workflow versions remain readable.
Old event-driven challenges cannot run. The original proposed catalog remains
untouched; a local derivative adds explicit business offer conditions and user
preference rankings instead of inferring executable rules from prose.

Current prepared local artifacts:

- `reports/restaurant-repair-20260921/catalog-v3.json`: authored source with
  structured conditions and preference order.
- `reports/restaurant-repair-20260921/cases-v3.json`: ten executable cases,
  prepared offline, zero live attempts.
- `reports/restaurant-repair-20260921/qualification.toml`: unfunded candidate
  configuration; uses saved target identity and callback address, which need a
  fresh check. The deployed version is deliberately unset.
- `reports/restaurant-repair-20260921/rumik-setup-plan.json`: concrete prompt and
  authenticated before-call/private-report tool contracts, without secrets.
- `reports/restaurant-repair-20260921/rumik-system-instructions.txt`: readable
  prompt candidate.

The older `catalog.json` and `cases.json` in that repair directory are intermediate
preparation artifacts, not the current run inputs. Historical live evidence lives
elsewhere and is unaffected.

Preparation never connects to providers and refuses to overwrite its output:

```sh
uv run --locked voice-bench restaurant prepare-natural \
  --catalog reports/restaurant-repair-20260921/catalog-v3.json \
  --output /absolute/new/path/natural-cases.json

uv run --locked voice-bench restaurant preflight \
  --config configs/restaurant-natural.example.toml \
  --cases reports/restaurant-repair-20260921/cases-v3.json
```

The example deliberately fails funding checks. Static preflight is not permission
to spend and is not a live qualification. Natural dispatch also checks that the
saved target snapshot has the exact revised prompt and the correctly scoped
private report tool. A stale deployed prompt or missing report tool blocks dispatch.
Changing the prompt candidate intentionally requires updating that check and
qualifying the new version.

## Verification and limits

Tests cover incomplete responses without mutations, unattributed idle timeout,
lookup/offer ordering, dietary limits, conditional offers, stale consent, duplicate
writes, independent PostgreSQL state, role isolation, multiple acceptable outcomes,
name uncertainty, absent reports, immutable review boundaries and event visibility.
Audio tests compare every sample and cancellation boundary. The local Chromium
stress test keeps full-duplex audio running for ten seconds with an added six
milliseconds of evidence delay per event. This would overload the previous event
rate; the repaired path must drain completely without a bridge error.

The WebRTC regression test uses two real peer connections with loopback candidate
addresses. This avoids depending on the machine's VPN/LAN/multicast behavior.
Loopback allowance is test-only; production networking is unchanged. The test
requires a connected peer and nonzero received PCM, not just a created track.

The current near-silence transcription guard is retained and tested. Samples with
peak amplitude at or below 2 on the PCM16 scale are not sent for transcription.
Saved historical transcription mistakes remain visible as historical evidence.

Final check results and raw-evidence preservation are recorded in the local
`reports/restaurant-repair-20260921/README.md` and `validation.json`.
No fresh transcription, remote evaluator, paid call, hosted prompt update or
production deployment is part of the local test proof.

## Remaining live acceptance

After explicit authorization and funded limits, deploy the reviewed target setup,
verify its deployed version and account-wide tool bindings, and qualify one simple
case. Require actual task delivery, completed simulator responses, understandable
two-sided audio, a consistent employee, truthful saved state, the private report,
confirmed termination and human listening. Then exercise fallback, flexible time,
dietary requirements, price/menu alternatives and useful refusal under the same
frozen configuration. Stop on simulator or transport faults; do not count them as
Rumik task failures. A supported target error in a valid conversation stays a failure.

If internal self-talk or silence survives a clean run, escalate with the exact
received-audio window, provider call ID, frozen prompt, response completion and
playback evidence. That isolates the hosted behavior without asserting access to
Rumik's private memory or internal model state.

## Full-conversation acceptance and silence recovery

A greeting-only attempt is not a completed dataset conversation. The first repaired
live attempt on September 21 stalled after greetings: the provider logged receipt
of the employee greeting, but the target recording contained only its opening.
The 45-second inactivity watchdog bounded that failure; it did not repair it.

The natural configuration now offers an explicit silence-recovery option. After
10 seconds without received speech, and only after generated speech has rendered,
the counterpart may make a brief follow-up using its own conversational context.
There are at most two such prompts without a new target speech event. The prompt
contains no private target assignment, invented reply or prescribed business outcome,
and disables tools for that recovery response. Each request is recorded as
`silence_recovery_requested`. The feature is off in the generic configuration;
both its interval and allowance must be enabled explicitly. Generation, business
tools, queued audio and active target speech suppress recovery and idle expiry.
The outer funded deadline still bounds a stuck provider or unfinished action.

Acceptance requires substantive task discussion, a supported business outcome
(which may be a legitimate no-booking outcome), the target's final report and
confirmed termination. Ending a transport session, receiving a greeting or exhausting
a recovery allowance is not acceptance. Recovery can expose or overcome a missed
turn; it does not prove that hosted task loading or response delivery is correct.

A subsequent live check exposed a separate completion defect: receiving the final
report cancelled the counterpart and allowed only two seconds to drain playback.
The employee had generated 10.35 seconds but only 9.037 seconds rendered before
shutdown. `target_report_then_hangup` now waits for the target's native hangup while
keeping both audio paths active. Browser observation also recognizes the departure
of the subscribed audio participant. A missing hangup after the configurable
30-second post-report allowance is an explicit incomplete execution, never success.
Regression checks cover a report arriving mid-turn and a three-second browser
closing turn. This changes completion semantics; historical results stay unchanged.

The same check revealed that the counterpart supplied year 2022 when the captured
request said only October 2. The next local case derivative supplies the current
local date and timezone as ordinary calendar context in the employee brief. It does
not expose the private requested date or expected outcome. This is a recorded case
version change, not a retroactive correction to the old transcript or lookup.

## Full natural restaurant batch, 2026-09-21

The separately authorized full batch ran all ten current executable natural restaurant
cases once, under an additional INR 1,550 ceiling. GPT completed ten evaluations;
Jev returned ten responses, of which nine passed the frozen response validator.
One probability set summed to 0.99. No paid request was retried. Formal outcomes
were zero passed, two failed and eight unresolved; simulation validity was six
valid, two invalid and two unresolved. Six private reports were missing. The four
received reports disagreed with the recorded business outcome. These observations
do not establish the provider-internal cause of every failure.

The local report is
`reports/full-dataset-preflight-20260921/final-report-v2/README.md`, with raw evidence
under batch `6d9d1de1-0e50-4908-ba9f-0b7eb25e4119`. It retains judge disagreements,
wrong-speaker attribution in one judge explanation, pending listening review and
all original results. The worker, callback tunnel and database were stopped;
all ten call terminations and the provider's idle state were verified.

`evaluation/cohort_metrics.py` computes browser speech-response timing by completed
employee playback item, with nearest-rank p50/p90/p95 and explicit unanswered and
overlapping observations. Its v2 correction was made after the live batch: a late
interruption flag does not exclude an item that was completely played. The original
v1 report remains available. Word error rate is an explicitly provisional comparison
between two machine transcripts, not a human-reviewed recognition score. True Rumik
time to first token and endpointing accuracy remain unavailable without provider
token/endpoint events and reference turn labels. Employee-side turn events cannot
stand in for the target's events. No hosted reliability repair is claimed.

## One-case Mulberry verification, 2026-09-22

The new harness and counterpart prompt did not pass the authorized one-case live
verification. A correct synthetic booking was recorded, but Rumik did not acknowledge
the reference or return its private report. One silence follow-up received no reply,
and the call ended on inactivity. Local playback completeness passed; it does not
prove remote hearing. The deployed target prompt was unchanged.

The counterpart also attempted booking before fresh confirmation; the business tool
rejected it. Consequently the formal result is invalid simulation and unresolved
outcome, not a clean target-only failure. All three evaluation stages completed.
Generation telemetry captured three unanswered-period samples with 400 completion
tokens and 396–397 reasoning tokens. This supports the output-budget hypothesis,
but does not expose the configured limit or generation finish reason. The P0 remains
unresolved. See `reports/p0-mulberry-verification-20260922-live/README.md` for the
recording, transcript, exact counts and evidence. Call termination, restored callback
settings and stopped temporary services were verified; no automatic live retry ran.
