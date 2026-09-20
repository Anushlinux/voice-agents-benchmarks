# Dataset starting point

The executable collection is **one baseline and three restaurant challenge
variants**, all within one task family. It is a useful integration and regression
set, but it is not yet a difficult Indian personal-assistant benchmark.

Start with the [review](REVIEW.md) and the
[eight proposed Indian assistant tasks](proposed/indian-assistant-v2.md).
The proposals are authored specifications, not executable cases or live results.

## Where to work

| Location | Purpose | Edit by hand? |
| --- | --- | --- |
| `authored/restaurant-baseline.json` | The existing baseline specification | Only as a new case version |
| `authored/restaurant-challenges.json` | The three existing challenge specifications | Only as a new case version |
| `generated/restaurant-baseline.json` | One existing execution input | No; regenerate |
| `generated/restaurant-challenges.json` | Three existing execution inputs | No; regenerate |
| `sources/taskmaster1/` | Original source record, source documentation and attribution | Preserve |
| `proposed/indian-assistant-v2.md` | New tasks, business rules, decisions and grading requirements | Yes; design work |
| `archive/2026-09-20/` | All 59 original files, including profiles, plans and historical validation | Preserve |

There are **five JSON files outside the archive**: two authored inputs, two
generated inputs and one source record. Read the two authored files to understand
the executable cases. The three counterpart styles are variations of those same
tasks; they are not extra task coverage. Generate a style only when selecting an
experiment instead of keeping every expansion in the working set.

The existing executable files retain their original bytes, case IDs, versions,
permissions, expected outcomes and rubrics. Their classification here as baseline
and challenges does not change an old score. The more demanding v2 designs must
receive new identities and implemented business rules before execution.

## Regenerate and compare offline

Run from the repository root using the already installed environment (`--no-sync`
avoids dependency installation). The preparation commands refuse existing output
paths; the temporary directory below avoids overwriting saved inputs. Compare
loaded cases, since newer schema defaults and JSON formatting differ from the
preserved historical files.

```sh
dataset_check_dir=$(mktemp -d)
uv run --locked --no-sync voice-bench restaurant prepare \
  --case datasets/authored/restaurant-baseline.json \
  --source datasets/sources/taskmaster1/sample.json \
  --output "$dataset_check_dir/baseline.json"
uv run --locked --no-sync voice-bench restaurant prepare-hard \
  --baseline "$dataset_check_dir/baseline.json" \
  --variants datasets/authored/restaurant-challenges.json \
  --output "$dataset_check_dir/challenges.json"
uv run --locked --no-sync python - "$dataset_check_dir" <<'PY'
import sys
from pathlib import Path
from voice_bench.batches import load_cases

for name in ("baseline", "challenges"):
    regenerated = load_cases(Path(sys.argv[1]) / f"{name}.json")
    saved = load_cases(Path(f"datasets/generated/restaurant-{name}.json"))
    assert [c.model_dump() for c in regenerated] == [c.model_dump() for c in saved]
print("All four cases agree after applying current schema defaults.")
PY
uv run --locked --no-sync voice-bench batch plan \
  --config configs/restaurant-hard.local.toml \
  --cases datasets/generated/restaurant-challenges.json --repetitions 1
```

These commands prepare or plan; they do not run a conversation. A successful
comparison proves the saved inputs reproduce under the current schema, not that
the cases are difficult or that hosted Rumik succeeds. It is not a byte-for-byte
regeneration claim; original bytes are verified separately in the archive.
Baseline and challenges retain separate
duration/configuration limits. See [the pilot guide](../docs/RESTAURANT_PILOT.md)
and [challenge guide](../docs/RESTAURANT_HARD_CASES.md).

## Preservation and scope

The archive keeps each old package intact. Its `SHA256SUMS` records every file as
found before reorganization. Old paths inside historical documents and plans are
historical references; use the paths above for current work. Saved run evidence
under `artifacts/`, saved results under `reports/`, and `report.md` were not moved
or rescored. No provider calls were made for this review.

Dataset files remain local and were not staged or published. The existing user
edit removing `datasets/` from `.gitignore` was left unchanged; consequently Git
currently shows this directory as untracked, rather than ignored. This does not
change the repository rule against committing datasets and evidence.
