from data_loader import load_edges
from algorithms import (
    baseline_edge_scan_bfs,
    build_adjacency_list,
    optimized_adjacency_bfs,
    verify_same_result,
    path_length
)


def main():
    edges, nodes = load_edges(limit=10000)

    print("\nALGORITHM TEST")
    print("-" * 60)
    print(f"Loaded edges: {len(edges)}")
    print(f"Loaded nodes: {len(nodes)}")

    # Use nodes that are likely connected in the first 10,000 edges
    start = 0
    goal = 385

    print(f"\nStart node: {start}")
    print(f"Goal node: {goal}")

    baseline_path = baseline_edge_scan_bfs(edges, start, goal)

    graph = build_adjacency_list(edges)
    optimized_path = optimized_adjacency_bfs(graph, start, goal)

    print("\nBASELINE BFS PATH")
    print("-" * 60)
    print(baseline_path)
    print(f"Path length: {path_length(baseline_path)}")

    print("\nOPTIMIZED BFS PATH")
    print("-" * 60)
    print(optimized_path)
    print(f"Path length: {path_length(optimized_path)}")

    print("\nCORRECTNESS CHECK")
    print("-" * 60)
    print("Same shortest path length:", verify_same_result(baseline_path, optimized_path))


if __name__ == "__main__":
    main()