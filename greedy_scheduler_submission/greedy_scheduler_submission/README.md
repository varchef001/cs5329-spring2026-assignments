# Multi-Constraint Greedy Resource Scheduler

This project has two greedy methods and one brute-force baseline for the scheduling problem in the assignment. I kept it in plain Python with only standard library modules.

## Files

- `scheduler.py` - main code
- `test_generator.py` - makes the required test files
- `test_cases/` - generated input JSON files
- `results/` - output JSON files from runs and benchmarks
- `analysis.md` - writeup for the greedy ideas, analysis, and reflection
- `README.md` - how to run everything

## Python version

- Python 3.8 or higher
- standard library only

## Generate the test cases

```bash
python test_generator.py --output-dir test_cases
```

This generates:
- 4 required scenario types: `sparse`, `dense`, `category_heavy`, `adversarial`
- sizes `10, 50, 100, 500, 1000`
- 5 small validation cases for brute-force checking
- edge cases: empty input, single task, identical-style overlap case, and capacity 1

## Solve one input file

Earliest-finish greedy:

```bash
python scheduler.py solve \
  --input test_cases/dense_10.json \
  --strategy earliest_finish_resource_aware \
  --output results/dense_10_earliest_finish_resource_aware.json
```

Weight/resource greedy:

```bash
python scheduler.py solve \
  --input test_cases/dense_10.json \
  --strategy highest_weight_to_resource_ratio \
  --output results/dense_10_highest_weight_to_resource_ratio.json
```

Brute force for a small case:

```bash
python scheduler.py solve \
  --input test_cases/validation_sparse_8.json \
  --strategy brute_force_optimal \
  --output results/validation_sparse_8_brute_force_optimal.json
```

The program prints the result to stdout and also writes a JSON file.

## Run benchmarks

```bash
python scheduler.py benchmark --input-dir test_cases --results-dir results
```

This writes:
- JSON result files for the main benchmark scenarios
- JSON result files for the 5 validation cases
- `results/benchmark_summary.json`

## What each strategy does

### `earliest_finish_resource_aware`
Sort by earliest finish time first. Then only take the task if it still keeps the schedule valid under resource capacity and category overlap rules.

### `highest_weight_to_resource_ratio`
Sort by higher `weight / resource` first. Then only take the task if it is still feasible.

### `brute_force_optimal`
Checks every subset and keeps the best feasible one. This is only for `n <= 15`.

## Important detail

I treated time intervals as half-open: `[start, end)`. So if one task ends at time 5 and another starts at time 5, I do not count that as overlap.

## Edge cases covered

The code was checked on:
- empty input
- single task
- all tasks overlapping
- identical values / repeated structure
- resource capacity = 1

## Usual order to run

1. `python test_generator.py --output-dir test_cases`
2. `python scheduler.py benchmark --input-dir test_cases --results-dir results`
3. read `analysis.md`
