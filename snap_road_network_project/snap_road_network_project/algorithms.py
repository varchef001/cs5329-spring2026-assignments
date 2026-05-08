from collections import deque, defaultdict


def baseline_edge_scan_bfs(edges, start, goal):
    """
    Baseline BFS.

    This version does not build an adjacency list.
    Every time it visits a node, it scans the full edge list to find neighbors.

    Time Complexity:
    O(V * E)

    V = number of visited nodes
    E = number of edges
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

        for source, destination in edges:
            if source == current and destination not in visited:
                queue.append((destination, path + [destination]))

    return None


def build_adjacency_list(edges):
    """
    Builds an adjacency list from an edge list.

    Example:
    Edge list:
    [(0, 1), (0, 2), (1, 3)]

    Adjacency list:
    {
        0: [1, 2],
        1: [3]
    }

    Time Complexity:
    O(E)

    E = number of edges
    """
    graph = defaultdict(list)

    for source, destination in edges:
        graph[source].append(destination)

    return graph


def optimized_adjacency_bfs(graph, start, goal):
    """
    Optimized BFS.

    This version uses an adjacency list, so neighbors can be found quickly.

    Time Complexity:
    O(V + E)

    V = number of nodes
    E = number of edges
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
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))

    return None


def path_length(path):
    """
    Returns the number of edges in the path.

    Example:
    [0, 1, 3, 5] has length 3.
    """
    if path is None:
        return None

    return len(path) - 1


def verify_same_result(baseline_path, optimized_path):
    """
    Verifies that baseline and optimized BFS produce the same shortest path length.

    The exact path may be different if multiple shortest paths exist.
    So we compare path lengths, not exact node sequence.
    """
    baseline_length = path_length(baseline_path)
    optimized_length = path_length(optimized_path)

    return baseline_length == optimized_length