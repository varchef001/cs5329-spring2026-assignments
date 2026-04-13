# Task Scheduling Assignment

## Project overview

This project is about scheduling tasks with three methods:

- greedy1
- greedy2
- brute force

Each task has a start time, end time, weight, resource value, and category.
The goal is to choose a set of tasks with high total weight while following the resource and category limits.

## Files in the project

- `scheduler.py` - main program
- `test_generator.py` - creates generated test files
- `testcases/` - input JSON files
- `results/` - output JSON files
- `analysis.md` - explanations, analysis, and reflection
- `readme.md` - instructions to run the code

## Python version

This project uses Python 3.8+ and only the standard library.

## How to generate test files

Run:

```bash
python test_generator.py --output-dir testcases
```

This creates the required scenario files and the small validation files.

## How to run the program

### Run greedy1

```bash
python scheduler.py solve --input testcases/sparse_10.json --strategy earliest_finish_resource_aware --output results/sparse_10_earliest_finish_resource_aware.json
```

### Run greedy2

```bash
python scheduler.py solve --input testcases/sparse_10.json --strategy highest_weight_to_resource_ratio --output results/sparse_10_highest_weight_to_resource_ratio.json
```

### Run brute force

```bash
python scheduler.py solve --input testcases/validation_sparse_8.json --strategy brute_force_optimal --output results/validation_sparse_8_brute_force_optimal.json
```

## Run all benchmarks

```bash
python scheduler.py benchmark --input-dir testcases --results-dir results
```

This writes all benchmark output JSON files and the summary file in `results/benchmark_summary.json`.

## Short explanation of the methods

- `greedy1` uses earliest finish time with feasibility checking
- `greedy2` uses weight per resource with feasibility checking
- `brute force` checks all valid subsets for small inputs

## Important note

Brute force should only be used for small inputs. It is not practical for large cases.

## Output

Each output JSON file includes:

- strategy name
- selected task ids
- total weight
- execution time
- utilization timeline
