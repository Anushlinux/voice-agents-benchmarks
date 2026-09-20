# Scope and role decisions

## Current direction

The user relayed the Rumik team's direction on 2026-09-20: evaluate Rumik acting on someone's behalf in Indian settings. Examples include booking, cancellation, negotiation, delivery coordination and conversations with drivers or support representatives. Long conversations and tasks spanning multiple interactions belong to the intended product scope.

This supersedes the earlier inbound business-agent framing. These are project requirements relayed by the user, not independently verified provider feature claims.

## Roles

| Component | Responsibility |
| --- | --- |
| Hosted Rumik target | Follow the user's assignment, constraints and permissions; converse and act on their behalf. |
| OpenAI counterpart | Play the other person, follow their assigned facts/business rules, and use only that role's tools. |
| Business environment | Validate actions and hold isolated synthetic records. A counterpart's words cannot invent a successful state change. |
| Evaluator | Check user outcomes, action permissions, conversation behavior and simulator validity using saved evidence. |

OpenAI is test infrastructure, not a second ranked agent. A separate optional OpenAI judge evaluates saved evidence; that is distinct from the live counterpart. Both sides do not need to use Rumik.

## Implemented scope and gaps

Schema 2 separates `user_task`, `counterpart`, role-specific tool grants, private business state, and grading criteria. The user's task is returned only through a correlated, authenticated Rumik before-call request. The controller waits for that response to be served before starting the counterpart. Hosted consumption of the task still needs live qualification.

`single_call` plus `harness_connected` is the only executable combination. The browser bridge connects one conversation; the Plivo adapter dials the Rumik-connected number. This can exercise a personal-assistant conversation but does not prove Rumik can initiate an outbound call.

`rumik_outbound` and `multi_call` can be represented and planned, but execution rejects them before provider activity. They require additional integration: target-originated dialing, task-level state across calls, destination selection, user approval exchanges, and task-level finalization. App actions in District or Uber also require an explicit app/tool environment; no app control is implemented here.

Long single-call scenarios can use a larger funded duration limit. Domain-specific holds, transfers, negotiation rules, permissions and scoring need authored workflows and scenarios. No coverage is inferred from the synthetic note-changing fixture.

## Dataset design boundaries

Each case needs the user's goal and permissions, the counterpart's role and visible facts, business rules and initial state, and observable acceptable outcomes. Do not give the counterpart the user's private budget or fallback preference unless Rumik reveals it or the scenario legitimately makes it known. Do not give Rumik the counterpart's hidden rules or expected grading answer.

Restaurant reservations belong to restaurant tools. A user's own calendar or legitimate booking API can belong to Rumik when explicitly modeled. Neither side has unrestricted access to the database. Grading must reject invented simulator concessions and separate simulator errors from target failures.

Dataset counts, real domain workflows, repetitions, model/voice choices, grading thresholds and paid run budgets remain to be supplied. Competitor ranking, a public leaderboard, production integrations, model training and automatic agent tuning are outside this change.
