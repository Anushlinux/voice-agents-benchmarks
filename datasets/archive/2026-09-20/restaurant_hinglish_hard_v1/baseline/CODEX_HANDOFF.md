# One Taskmaster-derived Hinglish restaurant-booking test

## Task for Codex

Implement and run **exactly one dataset case**, `tm1_restaurant_mumbai_hinglish_001`, using the existing project where possible. Do not build a larger benchmark, generate more cases, connect live businesses, or choose different datasets. The accompanying `case.json` is a custom specification, not the native Taskmaster or tau-bench schema.

Start with the dataset and role separation. Reuse the existing audio orchestration if it exists. If credentials or an audio adapter are absent, validate the fixture and describe the blocker; do not fabricate a run. A scripted fixture test or a text-only run is not a successful Rumik voice evaluation.

## Exact English source

- Dataset: Google's Taskmaster-1.
- File: `TM-1-2019/sample.json`.
- Conversation ID: `dlg-00055f4e-4a46-48bf-8d99-4e477663eb23`.
- Instruction ID: `restaurant-table-2`.
- Observed Git blob SHA: `21836935dbc399bf5ff5710d53d5326cc2d74ade`.
- Source: https://github.com/google-research-datasets/Taskmaster/blob/master/TM-1-2019/sample.json
- Raw source for retrieval: https://raw.githubusercontent.com/google-research-datasets/Taskmaster/master/TM-1-2019/sample.json
- Dataset methodology and copyright: https://github.com/google-research-datasets/Taskmaster/blob/master/TM-1-2019/README.md
- License notice: CC BY 4.0.

`source_transcript.json` preserves the original 20 utterance texts, speaker labels and indices from the verified GitHub response, but omits annotation spans and original formatting. It is not a byte-for-byte repository download. Keep the source immutable and preserve its attribution. If you retrieve the complete original, check the conversation ID before using it and record its actual hash; do not quietly replace the selected record.

Taskmaster is a human-created research dataset, not necessarily recorded commercial transactions. This sample alone does not establish whether this particular dialogue is from the self-dialogue or Wizard-of-Oz collection. Do not label it a real customer call.

## What the source actually says

Eight diners need Korean food at 7 p.m. in the New York/East Village area and refuse bar seating. Thursday Kitchen has no 7 p.m. availability; 5 p.m. and 8 p.m. are unacceptable. The customer proposes Boka, which can accept eight diners at 7 p.m., and authorizes booking through an existing account. The source ends with a promised phone confirmation; it does not contain an independently verified reservation, a reservation reference, a price or a full inventory.

## Exact adaptation

| Original | Change |
|---|---|
| English | Natural spoken Hinglish; keep numbers and dates semantically identical. |
| New York / East Village | Mumbai. |
| Thursday Kitchen, then Boka | Fictional Seoul Table Bandra, then Seoul Table Khar. |
| Two separate restaurants | Two branches managed by one central reservations desk so this is one conversation. This is an authored structural adaptation. |
| Tonight | Frozen test date: 25 September 2026, Asia/Kolkata. Do not derive the date from the machine's real clock. |
| Customer speaks to a booking assistant | Rumik speaks on the customer's behalf to the reservations desk. |
| Eight diners, 7 p.m., no bar; reject 5/8 p.m. | Preserve. |
| Fallback proposed mid-conversation | Customer preauthorizes Khar if Bandra fails, so no third live participant is needed. |
| Seating not otherwise specified | Explicitly require all eight at one regular table. This is added, not translated from the source. |
| No documented distractor inventory | Add physically available Khar bar seating and split tables, alongside the valid single table. |
| Existing account and promised phone confirmation | Fictional booking name Riya Rao; no payment, real account or SMS integration. The mock action returns a reference. |

Do not call this a pure translation. It is a source-derived test with documented extensions. All branch names, availability fixtures and operational rules are fictional and do not describe District or an actual restaurant.

## Agent roles and visibility

**Rumik is the assistant being evaluated, representing Riya.** Give it only `agent_brief` and live conversation context. It must not receive the inventory, expected option, source transcript or reference dialogue.

**The other voice agent is the restaurant employee simulator.** Give it `simulator_brief`, its inventory and mock action access. It is not another assistant representing the customer. It must not receive the evaluator's answer key. This fictional central desk is authorized to handle both branches.

**The harness/evaluator** holds the full fixture, conversation events and expected outcome. The JSON file has to be projected into separate contexts; never paste the whole file into both agents' prompts.

## Rumik's exact starting brief

You are a personal assistant making a simulated call on behalf of Riya Rao. You are speaking to the central reservations desk of Seoul Table, a fictional Korean restaurant with Bandra and Khar branches in Mumbai.
Book a table for eight people on 25 September 2026 at exactly 7 p.m. IST. Try Bandra first. If Bandra cannot satisfy every requirement, Khar is authorized as the fallback. Everyone must sit together at one regular table. Bar seating and splitting the party across tables are not acceptable. Neither 5 p.m. nor 8 p.m. is acceptable. Do not change the date or party size.
You may confirm one reservation, under Riya Rao, without contacting her again, but only if all requirements are met. You have no authority to agree to any charge or payment. This test is a free table reservation, not a meal purchase.
Speak naturally in Hinglish to the desk. Clearly distinguish aath log (eight people) from saat baje shaam (7 p.m.). Check the branch, date, time, party size and seating before authorizing the booking. Obtain the reservation reference. After the call, report the exact booked details to Riya; if you could not book, say so accurately.
Do not claim to operate District, send an SMS or charge a card. No real people or businesses are to be contacted.

## Fixed inventory visible only to the simulated restaurant

| Branch | Time | Arrangement | Why it matters |
|---|---|---|---|
| Bandra | 5 p.m. | One regular table for eight | Wrong time. |
| Bandra | 8 p.m. | One regular table for eight | Wrong time. |
| Khar | 7 p.m. | Eight bar seats | Bar seating forbidden. Added distractor. |
| Khar | 7 p.m. | Two regular tables of four | Party may not be split. Added distractor. |
| Khar | 7 p.m. | One regular table for eight | Meets all customer constraints. |

All entries are on 25 September 2026, IST. Reservations are free. No other slots exist in this fixture. All are physically bookable if accepted; the evaluator, not the booking API, enforces Riya's constraints.

Do not force the assistant to hear every alternative. An efficient assistant that asks precise questions may reach the valid choice quickly. Do not hide the correct option to inflate conversation length. This pilot tests constraint retention and fallback; it is not proof of advanced negotiation or long-horizon competence.

## Natural Hinglish

Use ordinary speech such as:

- “Bandra mein saat baje availability nahi hai; paanch ya aath baje table mil sakta hai.”
- “Time change nahi kar sakte. Khar branch mein aath logon ke liye ek hi table check kar dijiye.”
- “Do alag tables nahi chahiye; sabko saath baithna hai.”

These are illustrative authored lines, not a script. Keep the semantic distinction between **aath log** and **aath baje** clear. Do not inject a deliberately wrong time, random slang, background noise or interruption in this first case. Spoken output must be reviewed; a field saying `Hinglish` does not establish natural code-switching.

`reference_dialogue_hinglish.json` shows one possible valid conversation. Do not feed it to either live agent, replay it, or use exact transcript matching for grading. Do not reuse the original English character-offset annotations after rewriting text.

## Minimal observable booking state

Start with `bookings = []` for each run. Implement a mock `record_reservation` action owned by the simulated desk/harness. The action records an actually accepted inventory option and returns a run-specific reference. It must never contact a real booking platform.

Capture the proposed terms, caller's acceptance and booking event. Before a write, require an explicit acceptance following a full readback of the same slot. Store links to that evidence. The mock action checks physical availability and evidence of acceptance, not the evaluator's target option. Wrong-but-available accepted bookings must remain observable failures; do not silently autocorrect them.

If robust semantic confirmation checks are not implemented yet, retain the event evidence and mark that check as requiring human review. Do not let a simulator's self-reported `confirmed: true` prove consent. A deterministic tool result verifies the state write but does not by itself prove the speech matched the write.

The source did not provide this mock action, inventory model or rubric. They are authored additions to make the adapted task verifiable.

## Pass/fail for this one case

A valid passing run has exactly one reservation with:

```json
{
  "branch": "Khar",
  "date": "2026-09-25",
  "time": "19:00",
  "timezone": "Asia/Kolkata",
  "party_size": 8,
  "seating": "regular_table",
  "table_sizes": [
    8
  ],
  "booking_name": "Riya Rao",
  "reservation_charge_inr": 0
}
```

The saved reference is nonempty and allocated by the harness, and Rumik's final report must repeat that actual reference and correct booking details. Verify that Bandra was checked first, that the correct terms were accepted before commitment, and that no payment or external action occurred. The reference itself is not a pre-disclosed expected answer.

Fail a valid assistant run for the wrong branch/time/date/count/seating, split seating, an unauthorized commitment, no booking despite the discoverable valid option, or a false completion claim. Do not turn a correct final record into a pass if the assistant previously authorized an incorrect booking that was silently repaired.

Mark a run **invalid** if the simulator invents a slot, refuses to disclose a directly requested available option, records a booking the assistant never accepted, or infrastructure makes the interaction unreliable. Mark missing proof **inconclusive** rather than pass. Separately note language quality and observed turn timings; do not invent a latency threshold from the dataset.

## Scope and expected outputs

Use one live dialogue and one post-call user report. Reset state between retries; retries do not create additional dataset points. Deliver the final adapted fixture, run log or transcript, relevant audio where available, booking state, and evidence-backed verdict. A first run may fail, which is useful; do not tune the scenario to make it pass.

Do not add other domains, budget negotiation, payments, real District integration, a new dashboard, dozens of cases, or multi-call orchestration. This task contains exactly one adapted source datapoint. Do not report success percentages or general reliability from it.

## Current status of this package

The English source was inspected through the GitHub connector. The adaptation, inventory and reference dialogue were authored for this package. JSON structure, original utterance count, context-separation declarations and the existence of exactly one valid target option were checked locally. No human language review, live simulator trial or Rumik audio run has been completed.
