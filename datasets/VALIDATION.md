# Verification of the dataset review and reorganization

Checked locally on 20 September 2026. No runtime code, dependencies, existing
case contents, saved recordings or evaluation results were changed.

## Preservation and file checks

- All **59 original files** match their pre-move SHA-256 hashes in
  `archive/2026-09-20/SHA256SUMS`.
- All **seven selected active files** match their archived originals byte for
  byte: two authored inputs, two generated inputs, one source record, source
  README and attribution. Source documents retain their historical wording.
- All JSON files parse. Exactly **five JSON files** remain outside the archive.
- Individual old challenge files agree with the three entries in the authored
  variants list; the old four-case catalog agrees with baseline plus challenges.
- Both hard-package manifests verify fully. The original baseline manifest has
  three pre-existing missing handoff files; matching copies exist in the nested
  archived baseline. No present file has a manifest hash mismatch.
- Updated current guides use the new paths. Historical paths inside the archive
  and saved report remain historical; they were not rewritten.

## Offline generation and planning

The full shell example in `datasets/README.md` was executed successfully using
the installed environment with `UV_OFFLINE=1`, `UV_CACHE_DIR=.uv-cache` and
`--no-sync`. The importer verified the original source Git blob. Both preparation
commands produced new temporary files, and all four regenerated cases equal the
saved cases after loading through the current schema.

Byte comparison is intentionally a different check. New serialization includes
default fields missing from the old JSON, including `completion: counterpart`.
All twelve archived profile variants match a new generation after accounting for
one known difference: their saved source hash excludes that completion field.
Removing exactly that field reproduces every old hash. Nothing in those archived
files was rewritten. This is documented drift, not exact profile regeneration.

The four existing cases pass execution-schema validation and provider-free
planning: one baseline and three challenges. The challenge CLI plan explicitly
reports zero provider calls. Direct Python regeneration and profile comparisons
also ran with socket connections blocked.

For the review's offline plans only: planned 4; attempted 0; valid 0; invalid 0;
unresolved 0; passed 0; failed 0; not run 4. These are not updated totals for the
historical live benchmark. The eight new design cards have zero executable cases
and zero attempts; they are not included in that planning denominator.

## Repository checks

Commands used the existing installed environment:

```sh
UV_CACHE_DIR=.uv-cache UV_OFFLINE=1 uv run --locked --no-sync ruff check .
UV_CACHE_DIR=.uv-cache UV_OFFLINE=1 uv run --locked --no-sync ruff format --check .
UV_CACHE_DIR=.uv-cache UV_OFFLINE=1 uv run --locked --no-sync pytest \
  tests/test_reservations.py tests/test_restaurant_hard.py tests/test_benchmark_design.py
git diff --check
```

Results: lint passed; all 110 Python files already formatted; **90 tests passed,
2 skipped**, one existing `audioop` deprecation warning. The two PostgreSQL tests
were skipped because a test database was not configured. Whitespace checks passed.
New review-document links and active file references were checked locally.

The first plain `uv run --locked` attempts could not use the global cache in this
sandbox. Selecting the workspace cache then revealed that the offline cache lacked
`hatchling` for rebuilding the editable package. `--no-sync` reused the installed
environment successfully. No dependencies were downloaded or changed. These results
therefore do not claim a fresh locked-environment installation.

No database/browser integration run, container check, live provider run, human
listening review or empirical difficulty calibration was performed. No old result
was rescored. The user's existing `.gitignore` edit was preserved; datasets were
neither staged nor published.
