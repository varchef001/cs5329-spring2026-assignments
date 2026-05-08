import os


DATA_FILE = "data/roadNet-CA.txt"


def load_edges(limit=None):
    """
    Loads edges from the SNAP roadNet-CA dataset.

    Dataset format:
    source_node destination_node

    Lines starting with # are comments and should be skipped.

    Parameters:
        limit: Optional number of edges to load.
               Example: limit=10000 loads only first 10,000 edges.

    Returns:
        edges: list of (source, destination)
        nodes: set of all unique nodes
    """
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(
            f"Dataset file not found: {DATA_FILE}\n"
            "Make sure roadNet-CA.txt is inside the data folder."
        )

    edges = []
    nodes = set()

    with open(DATA_FILE, "r") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            parts = line.split()

            if len(parts) != 2:
                continue

            source = int(parts[0])
            destination = int(parts[1])

            edges.append((source, destination))
            nodes.add(source)
            nodes.add(destination)

            if limit is not None and len(edges) >= limit:
                break

    return edges, nodes


def print_dataset_summary(limit=None):
    """
    Prints a simple dataset summary.
    """
    edges, nodes = load_edges(limit)

    print("\nDATASET SUMMARY")
    print("-" * 60)

    if limit is None:
        print("Loaded: Full dataset")
    else:
        print(f"Loaded edge limit: {limit}")

    print(f"Total edges loaded: {len(edges)}")
    print(f"Total unique nodes loaded: {len(nodes)}")

    print("\nSample edges:")
    print("-" * 60)

    for edge in edges[:10]:
        print(edge)


if __name__ == "__main__":
    print_dataset_summary(limit=10000)