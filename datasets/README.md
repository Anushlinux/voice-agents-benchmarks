# Dataset starting point

The executable collection is **one baseline and three restaurant challenge
variants**, all within one task family. It is a useful integration and regression
set, but it is not yet a difficult Indian personal-assistant benchmark.

For the new conversation design, start with the
[restaurant v2 guide](proposed/restaurant-natural-v2.md) and its
[authoritative design catalog](proposed/restaurant-natural-v2.json): **ten proposed
synthetic cases, zero newly executable cases, zero live attempts, human conversation
review pending**. The balance is four everyday bookings, three trade-offs and
three situations where not booking is correct. These are design specifications,
not execution inputs or saved conversations.

The [review](REVIEW.md) explains the existing dataset's limitations. The
[eight earlier Indian assistant task proposals](proposed/indian-assistant-v2.md)
remain a separate cross-domain design workstream; they have not been implemented
by this restaurant-only revision.

## Where to work

| Location | Purpose | Edit by hand? |
| --- | --- | --- |
| `authored/restaurant-baseline.json` | The existing baseline specification | Only as a new case version |
| `authored/restaurant-challenges.json` | The three existing challenge specifications | Only as a new case version |
| `generated/restaurant-baseline.json` | One existing execution input | No; regenerate |
| `generated/restaurant-challenges.json` | Three existing execution inputs | No; regenerate |
| `sources/taskmaster1/` | Original source record, source documentation and attribution | Preserve |
| `proposed/restaurant-natural-v2.json` | Authoritative ten-case natural restaurant design; not runnable | Yes; design work |
| `proposed/restaurant-natural-v2.md` | Case map, review rules and implementation dependencies | Yes; keep aligned with catalog |
| `proposed/indian-assistant-v2.md` | Earlier cross-domain task and grading proposals | Yes; separate design work |
| `archive/2026-09-20/` | All 59 original files, including profiles, plans and historical validation | Preserve |

There are **six JSON files outside the archive**: two authored inputs, two
generated inputs, one source record and the new proposed design catalog. Read
the two authored files to understand the four existing executable cases. The
three counterpart styles are variations of those same
tasks; they are not extra task coverage. Generate a style only when selecting an
experiment instead of keeping every expansion in the working set.

The existing executable files retain their original bytes, case IDs, versions,
permissions, expected outcomes and rubrics. Their classification here as baseline
and challenges does not change an old score. The restaurant v2 catalog has new
case identities but still needs preparation, business-policy, conversation and
grading support before execution. Its naturalness and difficulty have not been
measured. Do not pass the proposed catalog to the commands below.

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

This revision remains local and was not staged, committed or published. Inspection
on 21 September 2026 found that existing dataset files were already tracked in
Git; the earlier statement that the entire directory was untracked is no longer
current. Existing tracking and `.gitignore` were left unchanged. The new catalog
and guide must remain outside Git publication, consistent with the repository
rule against committing datasets and evidence.
