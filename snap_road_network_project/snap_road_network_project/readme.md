
# Road Network Shortest Path Analysis Using SNAP Dataset

## Project Overview

This project analyzes shortest-path search on a large real-world road network dataset. The dataset used is the SNAP roadNet-CA dataset, which represents the California road network.

In this project:

- Nodes represent road intersections or road endpoints.
- Edges represent road connections between intersections.
- The goal is to find the shortest path between two intersections.

The main purpose of this project is to compare a naive baseline graph traversal approach with an optimized graph traversal approach and measure the performance difference at scale.

## Dataset

Dataset used:

```text
SNAP Road Network: roadNet-CA
````

Dataset file location:

```text
data/roadNet-CA.txt
```

Each line in the dataset contains two node IDs:

```text
source_node destination_node
```

Example:

```text
0 1
0 2
1 385
```

This means:

* Node `0` is connected to node `1`
* Node `0` is connected to node `2`
* Node `1` is connected to node `385`

The dataset does not include road names, distance, speed, or travel time. Because of that, this project treats the graph as unweighted and uses BFS to find the shortest path by number of road segments.

## Problem Statement

Given a large road network graph, find the shortest path between two road intersections and compare two approaches:

1. A baseline edge-list BFS approach
2. An optimized adjacency-list BFS approach

The goal is to show how choosing the right data structure improves graph traversal performance at scale.

## Project Structure

```text
snap_road_network_project/
│
├── data_loader.py
├── algorithms.py
├── benchmark.py
├── main.py
├── road_closure_analysis.py
├── test_algorithms.py
├── README.md
│
├── data/
│   └── roadNet-CA.txt
│
└── results/
    └── benchmark_results.csv
```

## File Descriptions

### data_loader.py

Loads and parses the SNAP road network dataset.

It:

* Reads `data/roadNet-CA.txt`
* Skips comment lines
* Extracts source and destination node IDs
* Returns an edge list and a set of unique nodes
* Supports loading limited input sizes for benchmarking

### algorithms.py

Contains the main algorithm implementations.

It includes:

* `baseline_edge_scan_bfs()`
* `build_adjacency_list()`
* `optimized_adjacency_bfs()`
* `path_length()`
* `verify_same_result()`

### test_algorithms.py

Tests whether the baseline and optimized algorithms return the same shortest path length.

This file is useful for quick correctness testing before running the full benchmark.

### main.py

Main entry point for the project.

It:

* Loads part of the SNAP dataset
* Runs baseline BFS
* Runs optimized BFS
* Prints both shortest paths
* Checks correctness
* Prints Big-O complexity summary

### benchmark.py

Runs performance testing across multiple input sizes.

It measures:

* Runtime
* Memory usage
* Speedup
* Correctness

Benchmark results are saved to:

```text
results/benchmark_results.csv
```

### road_closure_analysis.py

Extra feature for road network rerouting.

It simulates:

* Closing an intersection/node
* Closing a road/edge

Then it reruns BFS to check whether an alternate route exists.

## Algorithms Implemented

## 1. Baseline Approach: Edge-List BFS

The baseline approach uses BFS directly on the edge list.

For every visited node, it scans the entire edge list to find neighbors.

This is simple but inefficient for large graphs.

### Baseline Time Complexity

```text
O(V * E)
```

Where:

```text
V = number of visited nodes
E = number of edges
```

The baseline becomes slow because it repeatedly scans the full edge list.

## 2. Optimized Approach: Adjacency-List BFS

The optimized approach first builds an adjacency list.

Example:

```text
0: [1, 2, 469]
1: [0, 6, 385]
```

With an adjacency list, the algorithm can directly access a node’s neighbors instead of scanning the full edge list.

### Optimized Time Complexity

Building the adjacency list:

```text
O(E)
```

Running BFS:

```text
O(V + E)
```

Overall:

```text
O(V + E)
```

The main optimization is faster neighbor lookup.

## Correctness Verification

Both algorithms are checked by comparing their shortest path lengths.

The exact path may differ if multiple shortest paths exist, so the project compares path length instead of requiring the same exact node sequence.

Example output:

```text
Baseline BFS path: [0, 1, 385]
Optimized BFS path: [0, 1, 385]
Same shortest path length: True
```

## Main Program Output

Example `main.py` output:

```text
SNAP ROAD NETWORK SHORTEST PATH DEMO
======================================================================
Loading first 100000 edges from roadNet-CA dataset...

DATASET SUMMARY
----------------------------------------------------------------------
Edges loaded: 100000
Unique nodes loaded: 35539

ROUTE QUERY
----------------------------------------------------------------------
Start node: 0
Goal node: 385

BASELINE EDGE-LIST BFS RESULT
----------------------------------------------------------------------
0 -> 1 -> 385
Path length: 2 road segments

OPTIMIZED ADJACENCY-LIST BFS RESULT
----------------------------------------------------------------------
0 -> 1 -> 385
Path length: 2 road segments

CORRECTNESS CHECK
----------------------------------------------------------------------
Same shortest path length: True
```

This confirms that both algorithms return the same shortest path length.

## Benchmarking

The benchmark uses five input sizes:

```text
10,000 edges
50,000 edges
100,000 edges
500,000 edges
1,000,000 edges
```

Each input size runs 100 route queries.

The benchmark measures:

* Baseline runtime
* Optimized runtime
* Baseline memory usage
* Optimized memory usage
* Speedup
* Correctness

## Benchmark Results

|     Edges |   Nodes | Queries | Baseline Time | Optimized Time | Speedup | Correct |
| --------: | ------: | ------: | ------------: | -------------: | ------: | ------- |
|    10,000 |   4,478 |     100 |      27.10 ms |        2.43 ms |  11.14x | True    |
|    50,000 |  17,572 |     100 |     116.57 ms |        5.78 ms |  20.18x | True    |
|   100,000 |  35,539 |     100 |     223.26 ms |       11.87 ms |  18.82x | True    |
|   500,000 | 183,395 |     100 |    1116.88 ms |       82.62 ms |  13.52x | True    |
| 1,000,000 | 361,835 |     100 |    2383.67 ms |      132.91 ms |  17.93x | True    |

At 1,000,000 edges, the optimized adjacency-list BFS was about 17.93 times faster than the baseline edge-list BFS.

## Memory Usage

The optimized approach uses more memory than the baseline because it builds and stores an adjacency list.

This is expected.

The project shows a clear time-memory tradeoff:

* Baseline approach uses less memory but is slower.
* Optimized approach uses more memory but is much faster.

For large-scale graph problems, this tradeoff is useful because faster neighbor lookup gives better runtime performance.

## Theory vs Practice Summary

The theoretical analysis matches the benchmark results.

The baseline approach is slower because it repeatedly scans the edge list. As the input size grows, this repeated scanning becomes expensive.

The optimized approach builds an adjacency list once and then uses direct neighbor lookup. This improves runtime significantly, especially at larger input sizes.

The benchmark confirms that the optimized approach scales better in practice.

## Extra Feature: Road Closure Analysis

The file `road_closure_analysis.py` adds a practical extension.

It allows the user to simulate:

* Closing an intersection
* Closing a road segment

The program then reruns BFS and checks whether an alternate route exists.

This can represent real-world situations such as:

* Road construction
* Accidents
* Flooded roads
* Emergency detours

## How to Run the Project

### 1. Test Dataset Loader

```bash
python3 data_loader.py
```

### 2. Test Algorithms

```bash
python3 test_algorithms.py
```

### 3. Run Main Program

```bash
python3 main.py
```

### 4. Run Benchmark

```bash
python3 benchmark.py
```

Benchmark results will be saved to:

```text
results/benchmark_results.csv
```

### 5. Run Road Closure Analysis

```bash
python3 road_closure_analysis.py
```

## Conclusion

This project demonstrates how graph algorithms behave at scale using a real-world road network dataset.

The baseline edge-list BFS is simple but inefficient because it repeatedly scans the full edge list.

The optimized adjacency-list BFS is much faster because it stores neighbors directly.

The benchmark results show that the optimized approach provides a clear performance improvement while still producing the correct shortest path length.

```
```
