# Preserved dataset snapshot

All 59 files from the three original dataset directories were moved here on
20 September 2026 without changing their contents. `SHA256SUMS` records their
pre-move hashes, relative to this directory. No duplicate was deleted.

The current working files live in `../../authored/`, `../../generated/` and
`../../sources/`. They are exact copies of the selected archived inputs. The
snapshot is a historical reference, not another independently maintained dataset.

The original `tm1_restaurant_mumbai_hinglish_001/package-manifest.json` already
listed three absent files: `CODEX_HANDOFF.md`, `IMPLEMENTATION_RESULT.md` and
`RUNNING_PILOT.md`. Matching copies exist in
`restaurant_hinglish_hard_v1/baseline/`. The original manifest was not rewritten
to conceal those pre-existing absences. All present files match that manifest;
the hard-case package and its nested baseline match their complete manifests.

Historical preparation counts, validation results, source paths and live blockers
describe their original preparation. They are not fresh runtime status checks.
