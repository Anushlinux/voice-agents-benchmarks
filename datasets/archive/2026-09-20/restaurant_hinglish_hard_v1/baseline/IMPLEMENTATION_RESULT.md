# Single restaurant case: implementation and offline verification

Implemented the reconstructed Taskmaster-derived case, counterpart-only mock reservation tools, trusted speech evidence anchors, case-specific state/history checks, and human review requirements. Wrong-but-available bookings remain observable. Missing consent or user-report proof cannot become a pass.

## Verification

- Exact source blob matches the handoff: 21836935dbc399bf5ff5710d53d5326cc2d74ade.
- Original 20 utterance extract matches the unchanged source.
- One case, five inventory options, exactly one valid expected option.
- One planned browser attempt, no live attempts, no provider calls.
- Ruff check and format check passed; git diff --check passed.
- Final provider-free suite: 113 passed, 0 failed, 0 skipped, 3 existing deprecation warnings. PostgreSQL and Chromium checks were enabled.
- Temporary PostgreSQL server stopped after testing. No container build or live qualification claimed.

## Live blockers

The local configuration remains unfunded. It still needs the intended Rumik agent/version, counterpart model/voice, funded ceilings/rate card, callback URL and exported runtime credentials. Local credentials were not sent to providers. Callback connectivity and hosted consumption of the task require live qualification. There is no dedicated Rumik post-call user-report delivery integration.

See pilot-blockers.json for the provider-free preflight result. The native report may be identified only if it actually exists in saved provider evidence; otherwise the corresponding check remains inconclusive. No conversation, pilot booking state, or report was fabricated.

## Files

The ZIP contains the reconstructed custom case, one execution-case array, unchanged source and notice, transcript extract, handoff, attribution, hashes, offline plan, blockers and validation. It also includes the implementation guide and an unfunded config. Dataset files and generated outputs remain ignored by Git; workflow code and tests are in the repository.
