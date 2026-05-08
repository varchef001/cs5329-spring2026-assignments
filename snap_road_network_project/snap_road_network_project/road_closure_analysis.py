from collections import deque
from data_loader import load_edges
from algorithms import build_adjacency_list, optimized_adjacency_bfs, path_length


# Use 100,000 edges for live demo speed.
# You can change this to 1000000 if you want to test larger input.
EDGE_LIMIT = 100000


def bfs_with_blocked_node(graph, start, goal, blocked_node):
    """
    Finds shortest path while avoiding one closed intersection.

    blocked_node = intersection that is unavailable.

    Example:
    If blocked_node = 1, then the route cannot pass through node 1.
    """
    if start == blocked_node or goal == blocked_node:
        return None

    queue = deque([(start, [start])])
    visited = set()

    while queue:
        current, path = queue.popleft()

        if current == goal:
            return path

        if current in visited:
            continue

        visited.add(current)

        for neighbor in graph[current]:
            if neighbor == blocked_node:
                continue

            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))

    return None


def bfs_with_blocked_edge(graph, start, goal, blocked_source, blocked_destination):
    """
    Finds shortest path while avoiding one closed road segment.

    blocked edge = blocked_source -> blocked_destination

    Example:
    If road 0 -> 1 is closed, the algorithm avoids that road.
    """
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        current, path = queue.popleft()

        if current == goal:
            return path

        if current in visited:
            continue

        visited.add(current)

        for neighbor in graph[current]:
            if current == blocked_source and neighbor == blocked_destination:
                continue

            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))

    return None


def print_path(title, path):
    print(f"\n{title}")
    print("-" * 80)

    if path:
        print(" -> ".join(str(node) for node in path))
        print(f"Path length: {path_length(path)} road segments")
    else:
        print("No available route found.")


def compare_paths(original_path, new_path):
    print("\nIMPACT ANALYSIS")
    print("-" * 80)

    if original_path is None:
        print("Original route was not found.")
        return

    if new_path is None:
        print("The closure blocked the available route.")
        print("No alternate route was found within the loaded dataset.")
        return

    original_length = path_length(original_path)
    new_length = path_length(new_path)

    difference = new_length - original_length

    if difference > 0:
        print(f"The new route is longer by {difference} road segments.")
    elif difference < 0:
        print(f"The new route is shorter by {abs(difference)} road segments.")
    else:
        print("The new route has the same length.")

    if original_path != new_path:
        print("The route changed because part of the road network was blocked.")
    else:
        print("The route did not change.")


def show_sample_edges(edges, limit=10):
    print("\nSAMPLE ROAD CONNECTIONS")
    print("-" * 80)

    for source, destination in edges[:limit]:
        print(f"{source} -> {destination}")


def run_default_demo(graph):
    """
    Runs a simple demo using known nodes from the dataset sample.

    Original route is usually:
    0 -> 1 -> 385

    Then we close intersection 1.
    """
    start = 0
    goal = 385
    blocked_node = 1

    print("\nDEFAULT ROAD CLOSURE DEMO")
    print("=" * 80)
    print(f"Start intersection: {start}")
    print(f"Goal intersection: {goal}")
    print(f"Closed intersection: {blocked_node}")

    original_path = optimized_adjacency_bfs(graph, start, goal)
    new_path = bfs_with_blocked_node(graph, start, goal, blocked_node)

    print_path("ORIGINAL SHORTEST ROUTE", original_path)
    print_path(f"NEW ROUTE AFTER CLOSING INTERSECTION {blocked_node}", new_path)

    compare_paths(original_path, new_path)


def custom_intersection_closure(graph):
    """
    Lets user close one intersection and compare routes.
    """
    try:
        start = int(input("\nEnter start intersection/node ID: ").strip())
        goal = int(input("Enter goal intersection/node ID: ").strip())
        blocked_node = int(input("Enter intersection/node ID to close: ").strip())
    except ValueError:
        print("Invalid input. Please enter integer node IDs.")
        return

    original_path = optimized_adjacency_bfs(graph, start, goal)
    new_path = bfs_with_blocked_node(graph, start, goal, blocked_node)

    print_path("ORIGINAL SHORTEST ROUTE", original_path)
    print_path(f"NEW ROUTE AFTER CLOSING INTERSECTION {blocked_node}", new_path)

    compare_paths(original_path, new_path)


def custom_road_closure(graph):
    """
    Lets user close one directed road segment and compare routes.
    """
    try:
        start = int(input("\nEnter start intersection/node ID: ").strip())
        goal = int(input("Enter goal intersection/node ID: ").strip())
        blocked_source = int(input("Enter blocked road source node: ").strip())
        blocked_destination = int(input("Enter blocked road destination node: ").strip())
    except ValueError:
        print("Invalid input. Please enter integer node IDs.")
        return

    original_path = optimized_adjacency_bfs(graph, start, goal)
    new_path = bfs_with_blocked_edge(
        graph,
        start,
        goal,
        blocked_source,
        blocked_destination
    )

    print_path("ORIGINAL SHORTEST ROUTE", original_path)
    print_path(
        f"NEW ROUTE AFTER CLOSING ROAD {blocked_source} -> {blocked_destination}",
        new_path
    )

    compare_paths(original_path, new_path)


def main():
    print("\nSNAP ROAD CLOSURE ANALYSIS TOOL")
    print("=" * 80)
    print(f"Loading first {EDGE_LIMIT} edges for live demo...")

    edges, nodes = load_edges(limit=EDGE_LIMIT)
    graph = build_adjacency_list(edges)

    print(f"Loaded edges: {len(edges)}")
    print(f"Loaded nodes: {len(nodes)}")

    show_sample_edges(edges)

    while True:
        print("\nOPTIONS")
        print("-" * 80)
        print("1. Run default demo")
        print("2. Close an intersection/node")
        print("3. Close a road/edge")
        print("4. Show sample road connections")
        print("q. Quit")

        choice = input("\nEnter your choice: ").strip()

        if choice.lower() == "q":
            print("Exiting road closure analysis.")
            break

        elif choice == "1":
            run_default_demo(graph)

        elif choice == "2":
            custom_intersection_closure(graph)

        elif choice == "3":
            custom_road_closure(graph)

        elif choice == "4":
            show_sample_edges(edges)

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
    