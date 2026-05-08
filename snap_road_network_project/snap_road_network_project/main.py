from data_loader import load_edges
from algorithms import (
    baseline_edge_scan_bfs,
    build_adjacency_list,
    optimized_adjacency_bfs,
    verify_same_result,
    path_length
)


EDGE_LIMIT = 100000


def print_path(title, path):
    print(f"\n{title}")
    print("-" * 70)

    if path:
        print(" -> ".join(str(node) for node in path))
        print(f"Path length: {path_length(path)} road segments")
    else:
        print("No path found.")


def main():
    print("\nSNAP ROAD NETWORK SHORTEST PATH DEMO")
    print("=" * 70)

    print(f"Loading first {EDGE_LIMIT} edges from roadNet-CA dataset...")

    edges, nodes = load_edges(limit=EDGE_LIMIT)

    print("\nDATASET SUMMARY")
    print("-" * 70)
    print(f"Edges loaded: {len(edges)}")
    print(f"Unique nodes loaded: {len(nodes)}")

    start = 0
    goal = 385

    print("\nROUTE QUERY")
    print("-" * 70)
    print(f"Start node: {start}")
    print(f"Goal node: {goal}")

    print("\nRunning baseline edge-list BFS...")
    baseline_path = baseline_edge_scan_bfs(edges, start, goal)

    print("Building adjacency list for optimized BFS...")
    graph = build_adjacency_list(edges)

    print("Running optimized adjacency-list BFS...")
    optimized_path = optimized_adjacency_bfs(graph, start, goal)

    print_path("BASELINE EDGE-LIST BFS RESULT", baseline_path)
    print_path("OPTIMIZED ADJACENCY-LIST BFS RESULT", optimized_path)

    print("\nCORRECTNESS CHECK")
    print("-" * 70)
    print("Same shortest path length:", verify_same_result(baseline_path, optimized_path))

    print("\nCOMPLEXITY SUMMARY")
    print("-" * 70)
    print("Baseline edge-list BFS: O(V * E)")
    print("Optimized adjacency-list BFS: O(V + E)")
    print("Adjacency list build cost: O(E)")

    print("\nINTERPRETATION")
    print("-" * 70)
    print(
        "Both algorithms find the same shortest path length, but the optimized "
        "approach is faster because it uses direct neighbor lookup through an "
        "adjacency list instead of scanning the full edge list repeatedly."
    )


if __name__ == "__main__":
    main()