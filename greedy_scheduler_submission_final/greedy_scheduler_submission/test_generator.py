import argparse
import json
import os
import random
from typing import Dict, List, Any


def write_json(path: str, data: Dict[str, Any]) -> None:
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def make_task(task_id: int, start: int, end: int, weight: float, resource: int, category: str) -> Dict[str, Any]:
    return {
        "id": task_id,
        "start": start,
        "end": end,
        "weight": round(weight, 2),
        "resource": resource,
        "category": category,
    }


def generate_sparse(n: int, seed: int) -> Dict[str, Any]:
    rng = random.Random(seed)
    tasks: List[Dict[str, Any]] = []
    current_start = 0
    categories = ["compute", "io", "network", "storage"]
    for task_id in range(n):
        gap = rng.randint(0, 3)
        duration = rng.randint(2, 8)
        start = current_start + gap
        end = start + duration
        current_start = start + rng.randint(1, 3)
        weight = rng.uniform(1.5, 8.5)
        resource = rng.randint(1, 3)
        category = categories[task_id % len(categories)]
        tasks.append(make_task(task_id, start, end, weight, resource, category))

    return {
        "resource_capacity": 12,
        "category_limit": 3,
        "tasks": tasks,
    }


def generate_dense(n: int, seed: int) -> Dict[str, Any]:
    rng = random.Random(seed)
    tasks: List[Dict[str, Any]] = []
    categories = ["compute", "io", "network"]
    horizon = max(20, n // 3)
    for task_id in range(n):
        start = rng.randint(0, max(2, horizon - 8))
        duration = rng.randint(5, 15)
        end = min(horizon + 10, start + duration)
        if end <= start:
            end = start + 1
        weight = rng.uniform(1.0, 7.5)
        resource = rng.randint(2, 5)
        category = categories[rng.randint(0, len(categories) - 1)]
        tasks.append(make_task(task_id, start, end, weight, resource, category))

    return {
        "resource_capacity": 8,
        "category_limit": 2,
        "tasks": tasks,
    }


def generate_category_heavy(n: int, seed: int) -> Dict[str, Any]:
    rng = random.Random(seed)
    tasks: List[Dict[str, Any]] = []
    minority_categories = ["io", "network"]
    horizon = max(25, n // 2)
    for task_id in range(n):
        start = rng.randint(0, max(3, horizon - 6))
        duration = rng.randint(3, 12)
        end = min(horizon + 8, start + duration)
        if end <= start:
            end = start + 1
        weight = rng.uniform(1.0, 6.5)
        resource = rng.randint(1, 4)
        if rng.random() < 0.8:
            category = "compute"
        else:
            category = minority_categories[rng.randint(0, len(minority_categories) - 1)]
        tasks.append(make_task(task_id, start, end, weight, resource, category))

    return {
        "resource_capacity": 10,
        "category_limit": 1,
        "tasks": tasks,
    }


def generate_adversarial(n: int, seed: int) -> Dict[str, Any]:
    rng = random.Random(seed)
    tasks: List[Dict[str, Any]] = []

    horizon = 40
    tasks.append(make_task(0, 0, horizon, 12.0, 5, "compute"))

    windows = [(0, 10), (10, 20), (20, 30), (30, 40)]
    window_categories = ["io", "network", "io", "network"]

    for task_id in range(1, n):
        index = (task_id - 1) % len(windows)
        start, end = windows[index]
        weight = rng.uniform(2.0, 2.4)
        tasks.append(make_task(task_id, start, end, weight, 5, window_categories[index]))

    return {
        "resource_capacity": 5,
        "category_limit": 2,
        "tasks": tasks,
    }


def validation_cases() -> Dict[str, Dict[str, Any]]:
    return {
        "validation_sparse_8.json": generate_sparse(8, 101),
        "validation_dense_10.json": generate_dense(10, 202),
        "validation_category_12.json": generate_category_heavy(12, 303),
        "validation_adversarial_10.json": generate_adversarial(10, 404),
        "validation_identical_6.json": {
            "resource_capacity": 4,
            "category_limit": 2,
            "tasks": [
                make_task(0, 0, 4, 4.0, 2, "compute"),
                make_task(1, 0, 4, 4.0, 2, "compute"),
                make_task(2, 0, 4, 4.0, 2, "compute"),
                make_task(3, 4, 8, 4.0, 2, "io"),
                make_task(4, 4, 8, 4.0, 2, "io"),
                make_task(5, 4, 8, 4.0, 2, "io"),
            ],
        },
    }


def edge_cases() -> Dict[str, Dict[str, Any]]:
    return {
        "edge_empty.json": {
            "resource_capacity": 5,
            "category_limit": 2,
            "tasks": [],
        },
        "edge_single.json": {
            "resource_capacity": 3,
            "category_limit": 1,
            "tasks": [
                make_task(0, 0, 3, 3.5, 2, "compute"),
            ],
        },
        "edge_all_overlapping.json": {
            "resource_capacity": 4,
            "category_limit": 1,
            "tasks": [
                make_task(0, 0, 6, 5.0, 2, "compute"),
                make_task(1, 0, 6, 4.0, 2, "compute"),
                make_task(2, 0, 6, 4.5, 3, "io"),
                make_task(3, 0, 6, 3.0, 2, "network"),
            ],
        },
        "edge_capacity_one.json": {
            "resource_capacity": 1,
            "category_limit": 2,
            "tasks": [
                make_task(0, 0, 2, 2.5, 1, "compute"),
                make_task(1, 1, 3, 3.5, 1, "io"),
                make_task(2, 3, 5, 3.0, 1, "compute"),
                make_task(3, 4, 6, 2.0, 1, "network"),
            ],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate scheduler test cases")
    parser.add_argument("--output-dir", required=True, help="Directory where JSON files will be written")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    sizes = [10, 50, 100, 500, 1000]
    builders = {
        "sparse": generate_sparse,
        "dense": generate_dense,
        "category_heavy": generate_category_heavy,
        "adversarial": generate_adversarial,
    }

    for scenario_index, (scenario_name, builder) in enumerate(builders.items()):
        for size in sizes:
            instance = builder(size, 1000 + scenario_index * 100 + size)
            write_json(os.path.join(args.output_dir, f"{scenario_name}_{size}.json"), instance)

    for filename, instance in validation_cases().items():
        write_json(os.path.join(args.output_dir, filename), instance)

    for filename, instance in edge_cases().items():
        write_json(os.path.join(args.output_dir, filename), instance)

    print(f"Generated test cases in: {args.output_dir}")


if __name__ == "__main__":
    main()
