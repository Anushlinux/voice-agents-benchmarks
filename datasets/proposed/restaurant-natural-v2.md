# Restaurant dataset v2: natural conversations and meaningful decisions

**Ten proposed synthetic cases; zero newly executable cases; zero live attempts;
human conversation review pending.** This is dataset design only. Naturalness
and difficulty have not been demonstrated by calls or human recordings.

The authoritative specifications are in
[restaurant-natural-v2.json](restaurant-natural-v2.json). That catalog contains
the complete user requests, permissions, employee facts, business options and
grading requirements. This guide explains how to review it; it does not prescribe
dialogue or duplicate the individual specifications.

## What the ten cases cover

All ten are single-call situations in one restaurant task family. Names, dates,
businesses, availability, kitchen policies and prices are fictional. They are
original synthetic designs, not additional observations from Taskmaster.

| ID suffix | Type | Situation | Acceptable result |
| --- | --- | --- | --- |
| 01 | Everyday | Requested Aundh table is available | Book the requested table directly |
| 02 | Everyday | Indiranagar is full; Domlur is authorized | Book Domlur at the original time |
| 03 | Everyday | Adyar has two times inside the permitted window | Either 18:45 or 19:30 is correct |
| 04 | Everyday | Two guests need neither onion nor garlic | Book and retain the kitchen commitment for two guests |
| 05 | Trade-off | Earlier time outranks a preferred branch | Choose Banjara Hills at 19:00 |
| 06 | Trade-off | Full menu exceeds the budget | Choose the smaller menu without losing required inclusions |
| 07 | Trade-off | The cheaper promotion requires a deposit | Choose the permitted package without an advance |
| 08 | No booking | Every available time is outside the allowed window | Leave bookings empty and report the actual alternatives |
| 09 | No booking | Even the restaurant's minimum price exceeds the cap | Decline and accurately explain the price mismatch |
| 10 | No booking | Vegetarian food cannot meet both exclusions | Decline and explain the kitchen limitation |

The balance is four everyday situations, three trade-offs and three justified
no-booking outcomes. The cases do not measure ten distinct task families, and
these author-visible examples are not a held-out evaluation set.

## How conversations should work

Rumik receives the customer's ordinary request, constraints and permissions.
The employee receives only its own facts, business policies and permitted tool
results. The evaluator can inspect both sides. Never send the entire catalog,
an evaluation answer or the customer's private budget to the employee. A budget
the caller actually says aloud can legitimately become known during the call.

The employee answers relevant questions, asks for genuinely missing information
and offers useful alternatives. Business facts stay fixed. Neither actor is
given expected lines, a required conversation length or deliberately injected
errors. Natural Hinglish has no prescribed language ratio or accent imitation.

Before saving, the employee confirms the material agreement in context. A name
or detail already clearly established need not be recited again. Any changed
terms and all financial obligations need agreement. This relaxes a procedural
recital, not the requirement for real consent or a successful business action.

The employee delivers one actual reference naturally and clarifies it when
needed. Routine spelling and caller readback are not required. This proposed
policy is different from the current runtime and must be explicitly implemented
and versioned before use.

Table-only cases have no reservation fee; meals are ordered and paid for later.
That does not mean the meals are free. Package cases specify the total for the
entire party, all inclusions and any deposit. A deposit is part of the total, not
an extra amount. Dietary capacity is a business limit, not the number of dietary
meals the customer requested. Neither onion nor garlic is a food requirement
here; no allergy or cross-contact guarantee is implied.

## How to review the cases

1. Read the user request without the answer. Confirm that it supplies every
   permission, limit and preference needed to decide the task; the structured
   constraints must not add a private requirement missing from that request.
2. Inspect every business option. Compare date, time, branch, seating, price,
   inclusions, deposit and kitchen capacity against the customer's instructions.
   Apply preferences only after checking hard requirements. Accept every equally
   valid result, including both times in case 03.
3. Check the actual decision, commitments and persisted state. A spoken booking
   claim is insufficient. For a no-booking case, require an empty booking state
   and an evidence-supported explanation. A generic refusal in a solvable case
   is not successful completion. Retain forbidden attempts and later recovery.
4. Check Rumik's actual user report for accuracy. A booking has exactly one
   issued reference; a refusal does not have a reference. Do not substitute the
   employee's statement or a harness-written report for Rumik's report.
5. Assess employee compliance separately. Invented concessions, hidden relevant
   availability or unaccepted mutations can invalidate a simulation. Do not
   exclude a valid Rumik failure simply because its outcome is inconvenient.
6. In a future authorized pilot, listen to the audio for naturalness, pacing,
   repair and closing. Transcript formatting cannot prove these properties.
   Missing evidence remains unresolved. No listening review has happened for
   these proposed cases.

There are no model conversations to imitate, and a short successful exchange is
acceptable. Human role-play and listening should inform a later revision without
rewriting saved evidence or turning observed conversations into mandatory scripts.

## What must be implemented before execution

The JSON is a **design catalog, not an execution input**. Its design version is
separate from the runner's `ExecutionCase` schema version. Do not pass it to
`restaurant prepare`, `prepare-hard` or `batch run`.

| Dependency | Why the current runner cannot simply consume the new design |
| --- | --- |
| General case preparation | Existing importers require historical case IDs and specific input shapes |
| Natural confirmation | Prompts, tool descriptions, consent evidence handling and rubrics must agree on material-term consent without a full recital |
| Natural reference delivery | Current business results and runtime require spelling and requested readback |
| Alternative outcomes and preferences | Grading must accept a set of valid choices and enforce the actual customer preference order |
| Conditional menu offers | Menus, mutually exclusive packages, deposits and their conditions need explicit business support |
| No-booking and kitchen limitations | Grading must support an empty booking state and a truthful refusal without expecting `bookings[0]` or a reference |

The catalog identifies dependencies per case. These are future requirements,
not changes delivered here. Freeze case, business-policy, counterpart and grading
versions before a future batch. Live runs require a separate explicit request
and funded limits. This revision makes no provider calls and changes no runtime,
transport, completion protocol or provider configuration.

## Preservation and validation

The four existing executable cases remain regression inputs with their original
bytes and rubrics. The [earlier cross-domain designs](indian-assistant-v2.md) remain
separate proposals; this catalog does not implement or replace those workflows.
Source attribution, archives, saved conversations and reports are preserved.

Authoring validation checks JSON structure, unique identities, the 4/3/3 case
mix, price arithmetic, complete option accounting, constraint feasibility and
agreement between allowed outcomes and customer preferences. It also checks
actor separation and document links. Those checks establish design consistency,
not runnable integration or natural conversation quality.

Checked locally on 21 September 2026: all ten designs and 18 business options
passed these checks. An independent constraint calculation reproduced every
acceptable option set, including the two equally valid times and all three
no-booking outcomes. All eight local links in the updated entry guide and this
guide resolve. SHA-256 checks confirmed that all 550 pre-existing protected
dataset, evidence, report, output and ignore files remained unchanged; the
dataset entry README is the one intentionally edited existing file. Whitespace
checks passed. No runtime code changed, so no integration or provider test was
run for this design-only revision.

The files remain local: this revision does not stage, commit or publish datasets.
