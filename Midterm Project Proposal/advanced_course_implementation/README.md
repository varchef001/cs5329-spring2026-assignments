# Advanced Course Planner Using Graphs

## Team Members
- Varshith Gandra
- Raja Brahmendra

## Overview
This project builds a course planning system using graph algorithms. It helps students choose courses based on program, concentration, and electives, then generates a valid order for taking those courses while satisfying prerequisite constraints.

The system supports:
- multiple programs
- multiple concentrations
- core courses
- required concentration courses
- elective selection
- automatic prerequisite inclusion
- cycle detection

## Problem
Students often know their program and concentration, but they get confused about:
- which courses are mandatory
- which courses are electives
- the correct order to take courses

This project solves that problem by first identifying the relevant courses and then scheduling them in a valid prerequisite-respecting order.

## Algorithms Used

### Baseline: Repeated Linear Scan
This method repeatedly scans unscheduled courses and adds the ones whose prerequisites are already completed.

- **Time Complexity:** O(n²)
- **Space Complexity:** O(n)

### Optimized: Graph + Kahn’s Topological Sort
This method models courses as a directed graph and generates a valid order using topological sorting.

- **Time Complexity:** O(V + E)
- **Space Complexity:** O(V + E)

## Dataset Format
Each course is stored in JSON format:

json
{
  "course_id": "CS301",
  "course_name": "Machine Learning",
  "program": "Computer Science",
  "concentration": "AI & ML",
  "category": "Required",
  "prerequisites": ["AI301", "DS301"]
}
`

## Project Structure

text
Midterm Project Proposal/
├── README.md
├── advanced_course_implementation/
│   ├── main.py
│   ├── benchmark.py
│   └── src/
│       ├── baseline.py
│       ├── optimized.py
│       ├── validator.py
│       └── catalog_utils.py
├── datasets2/
│   ├── courses_advanced_catalog.json
│   ├── courses_advanced_cycle.json
│   ├── courses_cs_ai_ml_path.json
│   ├── courses_cs_data_science_path.json
│   ├── courses_large_100_advanced.json
│   ├── courses_large_500_advanced.json
│   └── README_advanced_datasets.md
└── advanced_course_planner_report.docx


## Features

* program selection
* concentration selection
* elective selection
* prerequisite validation
* cycle detection
* runtime and memory benchmarking

## How to Run

### Run the planner

bash
python3 main.py


Example dataset path:

text
../datasets2/courses_advanced_catalog.json


### Run the benchmark

bash
python3 benchmark.py


## Current Progress

* Baseline repeated linear scan algorithm implemented
* Optimized graph-based topological sort implemented
* Validation logic checks correctness of generated schedules
* Benchmarking harness measures runtime and peak memory usage
* Advanced datasets support program, concentration, and elective-based planning
* Cycle detection tested successfully

## Benchmark Summary

| Dataset              | # Courses | Baseline Time (s) | Baseline Memory (KB) | Optimized Time (s) | Optimized Memory (KB) | Speedup | Valid Output |
| -------------------- | --------: | ----------------: | -------------------: | -----------------: | --------------------: | ------: | ------------ |
| CS AI & ML Path      |        18 |        0.00027433 |                 5.22 |         0.00022408 |                  3.82 |   1.22x | Yes          |
| CS Data Science Path |        17 |        0.00014483 |                 5.01 |         0.00014492 |                  3.77 |   1.00x | Yes          |
| Large 100            |       100 |        0.00041129 |                33.02 |         0.00043208 |                 25.13 |   0.95x | Yes          |
| Large 500            |       500 |        0.00174533 |               151.70 |         0.00160029 |                101.77 |   1.09x | Yes          |

## Result Summary

Both algorithms produced valid schedules on the tested datasets. On small datasets, performance was very close. On larger datasets, the optimized graph-based approach began to show better runtime and lower memory usage. This supports the conclusion that the graph-based method is more suitable and scalable for prerequisite scheduling.

## Conclusion

This project shows how graph algorithms can solve a realistic course planning problem. The optimized topological sort approach is more natural for prerequisite relationships and scales better than the baseline repeated scan method.



