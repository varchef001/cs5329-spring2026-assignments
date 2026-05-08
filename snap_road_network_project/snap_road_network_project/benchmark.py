import csv
import time
import tracemalloc
from collections import defaultdict

from data_loader import load_edges
from algorithms import (
    baseline_edge_scan_bfs,
    build_adjacency_list,
    optimized_adjacency_bfs,
    verify_same_result,
    path_length
)


INPUT_SIZES = [
    10000,
    50000,
    100000,
    500000,
    1000000
]

QUERY_COUNT = 100
RESULT_FILE = "results/benchmark_results.csv"


def create_reachable_queries(edges, query_count):
    """
    Creates start-goal pairs from real edges.

    This avoids random disconnected node pairs that can make
    the baseline BFS extremely slow.

    Each query is guaranteed to have at least a direct edge:
    start -> goal
    """
    queries = []
    seen = set()

    step = max(1, len(edges) // query_count)

    for i in range(0, len(edges), step):
        if len(queries) >= query_count:
            break

        source, destination = edges[i]

        if source != destination and (source, destination) not in seen:
            queries.append((source, destination))
            seen.add((source, destination))

    return queries


def measure_baseline(edges, queries):
    """
    Measures baseline edge-scan BFS.

    Baseline approach:
    For every visited node, scan the full edge list to find neighbors.

    Approximate Time Complexity:
    O(V * E)
    """
    tracemalloc.start()
    start_time = time.perf_counter()

    paths = []

    for start, goal in queries:
        path = baseline_edge_scan_bfs(edges, start, goal)
        paths.append(path)

    end_time = time.perf_counter()
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    runtime_ms = (end_time - start_time) * 1000
    memory_kb = peak_memory / 1024

    return runtime_ms, memory_kb, paths


def measure_optimized(edges, queries):
    """
    Measures optimized adjacency-list BFS.

    Optimized approach:
    Build adjacency list once, then run BFS using direct neighbor lookup.

    Time Complexity:
    Building graph: O(E)
    BFS queries: O(V + E)
    """
    tracemalloc.start()
    start_time = time.perf_counter()

    graph = build_adjacency_list(edges)

    paths = []

    for start, goal in queries:
        path = optimized_adjacency_bfs(graph, start, goal)
        paths.append(path)

    end_time = time.perf_counter()
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    runtime_ms = (end_time - start_time) * 1000
    memory_kb = peak_memory / 1024

    return runtime_ms, memory_kb, paths


def check_correctness(baseline_paths, optimized_paths):
    """
    Verifies both algorithms produce the same shortest path length.

    Exact path may differ if multiple shortest paths exist,
    so path length is compared.
    """
    for baseline_path, optimized_path in zip(baseline_paths, optimized_paths):
        if not verify_same_result(baseline_path, optimized_path):
            return False

    return True


def average_path_length(paths):
    """
    Calculates average path length.
    """
    lengths = []

    for path in paths:
        length = path_length(path)

        if length is not None:
            lengths.append(length)

    if not lengths:
        return 0

    return sum(lengths) / len(lengths)


def save_results(results):
    """
    Saves benchmark results into results/benchmark_results.csv.
    """
    with open(RESULT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "input_edges",
            "unique_nodes",
            "queries",
            "baseline_time_ms",
            "optimized_time_ms",
            "baseline_memory_kb",
            "optimized_memory_kb",
            "speedup",
            "average_path_length",
            "same_result"
        ])

        writer.writerows(results)


def run_benchmark():
    print("\nSNAP ROAD NETWORK BENCHMARK")
    print("=" * 130)
    print(f"Queries per input size: {QUERY_COUNT}")

    results = []

    print("\nBENCHMARK RESULTS")
    print("-" * 130)
    print(
        f"{'Edges':<12}"
        f"{'Nodes':<10}"
        f"{'Queries':<10}"
        f"{'Baseline Time(ms)':<22}"
        f"{'Optimized Time(ms)':<24}"
        f"{'Baseline Mem(KB)':<20}"
        f"{'Optimized Mem(KB)':<22}"
        f"{'Speedup':<12}"
        f"{'Correct':<10}"
    )
    print("-" * 130)

    for size in INPUT_SIZES:
        print(f"\nLoading {size} edges...")

        edges, nodes = load_edges(limit=size)
        queries = create_reachable_queries(edges, QUERY_COUNT)

        print(f"Running baseline BFS for {size} edges...")
        baseline_time, baseline_memory, baseline_paths = measure_baseline(edges, queries)

        print(f"Running optimized BFS for {size} edges...")
        optimized_time, optimized_memory, optimized_paths = measure_optimized(edges, queries)

        same_result = check_correctness(baseline_paths, optimized_paths)
        avg_length = average_path_length(optimized_paths)

        if optimized_time > 0:
            speedup = baseline_time / optimized_time
        else:
            speedup = 0

        print(
            f"{size:<12}"
            f"{len(nodes):<10}"
            f"{len(queries):<10}"
            f"{baseline_time:<22.4f}"
            f"{optimized_time:<24.4f}"
            f"{baseline_memory:<20.2f}"
            f"{optimized_memory:<22.2f}"
            f"{speedup:<12.2f}"
            f"{str(same_result):<10}"
        )

        results.append([
            size,
            len(nodes),
            len(queries),
            baseline_time,
            optimized_time,
            baseline_memory,
            optimized_memory,
            speedup,
            avg_length,
            same_result
        ])

    save_results(results)

    print("\nBenchmark saved to:")
    print(RESULT_FILE)


if __name__ == "__main__":
    run_benchmark()
    