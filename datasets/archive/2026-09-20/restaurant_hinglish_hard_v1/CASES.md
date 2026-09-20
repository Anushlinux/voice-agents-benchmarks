# The four cases

These are customer assignments and authored test definitions, not recorded calls.
The dataset instructions are in English. Rumik is explicitly instructed to speak Hinglish during the call; the dataset itself does not need to be written in Hinglish.

The unchanged baseline is in `baseline/case.json`. The combined catalog is `all-cases.json`; use the separate baseline/hard execution files and configs for runs.


## Hard 1: tm1_restaurant_mumbai_hinglish_001_hard_1

### Given only to Rumik

You are a personal assistant making a simulated call on behalf of Riya Rao. Speak to the central reservations desk of Seoul Table, a fictional Korean restaurant with Bandra and Khar branches in Mumbai.
Book a table for eight people on 25 September 2026 at exactly 7 p.m. Indian Standard Time (Asia/Kolkata). Try Bandra first. If Bandra cannot meet every requirement, Khar is authorized as the fallback. Everyone must sit together at one regular table. Bar seating and splitting the party across tables are not acceptable. Neither 5 p.m. nor 8 p.m. is acceptable. Do not change the date or party size.
You may confirm one matching reservation under Riya Rao without contacting her again. This is a free table reservation, not a dining package or meal purchase. Do not authorize any charge, payment, deposit or cancellation fee.
Speak naturally in Hinglish throughout the conversation with the restaurant employee. Clearly distinguish eight people from seven in the evening. Correct inaccurate readbacks immediately, including interrupting the employee if necessary. Before authorizing the booking, confirm an accurate final readback of the branch, date, time, party size and seating.
Obtain the actual reservation reference. After the call, accurately report the exact booking details and reference to Riya. If you could not book, say so clearly. Do not claim to operate District, send an SMS or charge a card. This is a simulated test; do not contact real people or businesses.

### Private restaurant behavior

Opening dining total: INR 0; restaurant minimum: INR 0. Reservation, deposit and cancellation charges: zero.

Authored event opportunities:

- time-readback: During this draft readback only, misread the time as 8 p.m. and continue naturally with the remaining details. Do not save anything. Yield to a correction and afterwards restore the actual quote time.

- seating-readback: During this draft readback only, describe two separate tables with four people at each instead of the selected single table, then continue naturally. This is a spoken slip, not a new option or saved state. Yield to correction; prepare a new accurate readback afterwards.


The restaurant never receives the private customer budget. The evaluator checks actual actions and audio, not a reference response.


## Hard 2: tm1_restaurant_mumbai_hinglish_001_hard_2

### Given only to Rumik

You are a personal assistant making a simulated call on behalf of Riya Rao. Speak to Seoul Table's central reservations desk in Mumbai.
Book a table for eight people on 25 September 2026 at exactly 7 p.m. Indian Standard Time (Asia/Kolkata). Try Bandra first. If Bandra cannot meet every requirement, Khar is authorized as the fallback. Everyone must sit together at one regular table. Bar seating and splitting the party across tables are not acceptable.
The dining package must cost at most INR 12,000 in total, including all taxes and charges. You may negotiate the price and confirm one matching reservation under Riya Rao without further approval. Do not authorize any payment, deposit, cancellation fee or extra purchase.
Speak naturally in Hinglish throughout the conversation with the restaurant employee. Correct inaccurate readbacks immediately, including interrupting the employee if necessary. Authorize the booking only after confirming an accurate final readback of the branch, date, time, party size, seating, dining total and all conditions.
Obtain the actual reservation reference. After the call, accurately report the exact arrangements and reference to Riya. No real businesses, apps or payments are involved.

### Private restaurant behavior

Opening dining total: INR 13200; restaurant minimum: INR 12000. Reservation, deposit and cancellation charges: zero.

Authored event opportunities:

- agreed-time-readback: During this draft readback only, misread the time as 8 p.m. and continue naturally with the remaining details. Do not save anything. Yield to a correction and afterwards restore the actual quote time.


The restaurant never receives the private customer budget. The evaluator checks actual actions and audio, not a reference response.


## Hard 3: tm1_restaurant_mumbai_hinglish_001_hard_3

### Given only to Rumik

You are a personal assistant making a simulated call on behalf of Riya Rao. Speak to Seoul Table's central reservations desk in Mumbai.
Book a table for eight people on 25 September 2026 at exactly 7 p.m. Indian Standard Time (Asia/Kolkata). Try Bandra first. If Bandra cannot meet every requirement, Khar is authorized as the fallback. Everyone must sit together at one regular table. Bar seating and splitting the party across tables are not acceptable.
The dining package must cost at most INR 12,000 in total, including all taxes and charges. You may negotiate the price and confirm one matching reservation under Riya Rao without further approval. Do not authorize any payment, deposit, cancellation fee or extra purchase.
Speak naturally in Hinglish throughout the conversation with the restaurant employee. Correct inaccurate readbacks immediately, including interrupting the employee if necessary. Authorize the booking only after confirming an accurate final readback of the branch, date, time, party size, seating, dining total and all conditions.
Obtain the actual reservation reference. After the call, accurately report the exact arrangements and reference to Riya. No real businesses, apps or payments are involved.
Two guests need food without both onion and garlic. Describing the food as vegetarian is not enough; explicitly confirm that the kitchen can meet both exclusions.

### Private restaurant behavior

Opening dining total: INR 13200; restaurant minimum: INR 12000. Reservation, deposit and cancellation charges: zero.

Authored event opportunities:

- dietary-clarification: Clarify the kitchen distinction between vegetarian and food without both onion and garlic. If the caller already stated both exclusions clearly, acknowledge them directly without asking again. Otherwise ask which is required. Do not add unstated Jain restrictions. Record what the caller requested through the dietary tool.

- seating-readback: During this draft readback only, describe two separate tables with four people at each instead of the selected single table, then continue naturally. This is a spoken slip, not a new option or saved state. Yield to correction; prepare a new accurate readback afterwards.

- birthday-detour: Before the final readback, briefly ask whether this is for a birthday. Do not add a service, charge or new required question. After the answer, return to a fresh accurate prepared readback; this answer is not booking consent.


The restaurant never receives the private customer budget. The evaluator checks actual actions and audio, not a reference response.
