
import argparse
import json
import os
import time
from collections import defaultdict
from itertools import combinations
from typing import Dict, List, Tuple, Any

Task = Dict[str, Any]


def load_instance(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    resource_capacity = int(data.get("resource_capacity", 0))
    category_limit = int(data.get("category_limit", 0))
    tasks = []
    for raw in data.get("tasks", []):
        task = {
            "id": int(raw["id"]),
            "start": int(raw["start"]),
            "end": int(raw["end"]),
            "weight": float(raw["weight"]),
            "resource": int(raw["resource"]),
            "category": str(raw["category"]),
        }
        tasks.append(task)

    tasks.sort(key=lambda item: item["id"])
    return {
        "resource_capacity": resource_capacity,
        "category_limit": category_limit,
        "tasks": tasks,
    }


def write_json(path: str, data: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def intervals_overlap(a: Task, b: Task) -> bool:
    return max(a["start"], b["start"]) < min(a["end"], b["end"])


def can_add_task(selected: List[Task], candidate: Task, resource_capacity: int, category_limit: int) -> bool:
    if candidate["resource"] > resource_capacity:
        return False

    start_events = defaultdict(lambda: [0, 0])
    end_events = defaultdict(lambda: [0, 0])

    s = candidate["start"]
    e = candidate["end"]

    for task in selected:
        overlap_start = max(task["start"], s)
        overlap_end = min(task["end"], e)
        if overlap_start < overlap_end:
            resource = task["resource"]
            same_category = 1 if task["category"] == candidate["category"] else 0
            start_events[overlap_start][0] += resource
            start_events[overlap_start][1] += same_category
            end_events[overlap_end][0] += resource
            end_events[overlap_end][1] += same_category

    critical_times = sorted(set([s, e] + list(start_events.keys()) + list(end_events.keys())))
    active_resource = 0
    active_same_category = 0

    for index, time_point in enumerate(critical_times):
        end_delta = end_events[time_point]
        active_resource -= end_delta[0]
        active_same_category -= end_delta[1]

        start_delta = start_events[time_point]
        active_resource += start_delta[0]
        active_same_category += start_delta[1]

        if index < len(critical_times) - 1 and critical_times[index + 1] > time_point:
            if active_resource + candidate["resource"] > resource_capacity:
                return False
            if active_same_category + 1 > category_limit:
                return False

    return True


def is_schedule_feasible(tasks: List[Task], resource_capacity: int, category_limit: int) -> bool:
    start_events = defaultdict(list)
    end_events = defaultdict(list)

    for task in tasks:
        if task["resource"] > resource_capacity:
            return False
        start_events[task["start"]].append(task)
        end_events[task["end"]].append(task)

    critical_times = sorted(set(list(start_events.keys()) + list(end_events.keys())))
    active_resource = 0
    active_categories: Dict[str, int] = defaultdict(int)

    for index, time_point in enumerate(critical_times):
        for task in end_events[time_point]:
            active_resource -= task["resource"]
            active_categories[task["category"]] -= 1
            if active_categories[task["category"]] == 0:
                del active_categories[task["category"]]

        for task in start_events[time_point]:
            active_resource += task["resource"]
            active_categories[task["category"]] += 1

        if index < len(critical_times) - 1 and critical_times[index + 1] > time_point:
            if active_resource > resource_capacity:
                return False
            for count in active_categories.values():
                if count > category_limit:
                    return False

    return True


def build_utilization_timeline(tasks: List[Task]) -> Dict[str, Any]:
    if not tasks:
        return {}

    start_events = defaultdict(list)
    end_events = defaultdict(list)
    for task in tasks:
        start_events[task["start"]].append(task)
        end_events[task["end"]].append(task)

    critical_times = sorted(set(list(start_events.keys()) + list(end_events.keys())))
    timeline: Dict[str, Any] = {}
    active_resource = 0
    active_categories: Dict[str, int] = defaultdict(int)

    for index, time_point in enumerate(critical_times):
        for task in end_events[time_point]:
            active_resource -= task["resource"]
            active_categories[task["category"]] -= 1
            if active_categories[task["category"]] == 0:
                del active_categories[task["category"]]

        for task in start_events[time_point]:
            active_resource += task["resource"]
            active_categories[task["category"]] += 1

        if index < len(critical_times) - 1:
            next_time = critical_times[index + 1]
            if next_time > time_point and (active_resource > 0 or active_categories):
                timeline[f"{time_point}-{next_time}"] = {
                    "resource_used": active_resource,
                    "categories": dict(sorted(active_categories.items())),
                }

    return timeline


def summarize_result(strategy_name: str, selected: List[Task], execution_time: float) -> Dict[str, Any]:
    ordered_selected = sorted(selected, key=lambda task: task["id"])
    return {
        "strategy_name": strategy_name,
        "selected_tasks": [task["id"] for task in ordered_selected],
        "total_weight": round(sum(task["weight"] for task in ordered_selected), 4),
        "execution_time_seconds": round(execution_time, 6),
        "utilization_timeline": build_utilization_timeline(ordered_selected),
    }


def greedy_earliest_finish(tasks: List[Task], resource_capacity: int, category_limit: int) -> Dict[str, Any]:
    ordered = sorted(
        tasks,
        key=lambda task: (
            task["end"],
            task["end"] - task["start"],
            task["resource"],
            -task["weight"],
            task["start"],
            task["id"],
        ),
    )

    selected: List[Task] = []
    start_time = time.perf_counter()
    for task in ordered:
        if can_add_task(selected, task, resource_capacity, category_limit):
            selected.append(task)
    end_time = time.perf_counter()
    return summarize_result("earliest_finish_resource_aware", selected, end_time - start_time)


def greedy_weight_resource_ratio(tasks: List[Task], resource_capacity: int, category_limit: int) -> Dict[str, Any]:
    ordered = sorted(
        tasks,
        key=lambda task: (
            -(task["weight"] / max(task["resource"], 1)),
            -task["weight"],
            task["end"] - task["start"],
            task["end"],
            task["resource"],
            task["id"],
        ),
    )

    selected: List[Task] = []
    start_time = time.perf_counter()
    for task in ordered:
        if can_add_task(selected, task, resource_capacity, category_limit):
            selected.append(task)
    end_time = time.perf_counter()
    return summarize_result("highest_weight_to_resource_ratio", selected, end_time - start_time)


def brute_force_solver(tasks: List[Task], resource_capacity: int, category_limit: int) -> Dict[str, Any]:
    if len(tasks) > 15:
        raise ValueError("Brute-force solver is restricted to inputs with n <= 15.")

    best_subset: List[Task] = []
    best_weight = -1.0
    start_time = time.perf_counter()

    for subset_size in range(len(tasks) + 1):
        for subset in combinations(tasks, subset_size):
            candidate_subset = list(subset)
            total_weight = sum(task["weight"] for task in candidate_subset)
            if total_weight < best_weight:
                continue
            if is_schedule_feasible(candidate_subset, resource_capacity, category_limit):
                if total_weight > best_weight:
                    best_weight = total_weight
                    best_subset = candidate_subset

    end_time = time.perf_counter()
    return summarize_result("brute_force_optimal", best_subset, end_time - start_time)


STRATEGIES = {
    "earliest_finish_resource_aware": greedy_earliest_finish,
    "highest_weight_to_resource_ratio": greedy_weight_resource_ratio,
    "brute_force_optimal": brute_force_solver,
}


def solve_instance(instance: Dict[str, Any], strategy_name: str) -> Dict[str, Any]:
    solver = STRATEGIES[strategy_name]
    return solver(
        instance["tasks"],
        instance["resource_capacity"],
        instance["category_limit"],
    )


def print_result(result: Dict[str, Any]) -> None:
    print(f"Strategy: {result['strategy_name']}")
    print(f"Selected tasks: {result['selected_tasks']}")
    print(f"Total weight: {result['total_weight']}")
    print(f"Execution time (seconds): {result['execution_time_seconds']}")
    print("Utilization timeline:")
    if not result["utilization_timeline"]:
        print("  <empty>")
    else:
        for span, usage in result["utilization_timeline"].items():
            print(f"  {span}: resource_used={usage['resource_used']}, categories={usage['categories']}")


def benchmark_solver(strategy_name: str, instance: Dict[str, Any], repeats: int = 1) -> Tuple[Dict[str, Any], float]:
    solver = STRATEGIES[strategy_name]
    best_result = None
    total_time = 0.0

    for _ in range(repeats):
        start_time = time.perf_counter()
        result = solver(
            instance["tasks"],
            instance["resource_capacity"],
            instance["category_limit"],
        )
        total_time += time.perf_counter() - start_time
        best_result = result

    assert best_result is not None
    best_result["execution_time_seconds"] = round(total_time / repeats, 6)
    return best_result, total_time / repeats


def run_benchmarks(input_dir: str, results_dir: str) -> Dict[str, Any]:
    scenarios = ["sparse", "dense", "category_heavy", "adversarial"]
    sizes = [10, 50, 100, 500, 1000]
    validation_files = [
        "validation_sparse_8.json",
        "validation_dense_10.json",
        "validation_category_12.json",
        "validation_adversarial_10.json",
        "validation_identical_6.json",
    ]

    benchmark_summary: Dict[str, Any] = {
        "large_benchmarks": {},
        "validation_against_optimal": {},
    }

    for scenario in scenarios:
        benchmark_summary["large_benchmarks"][scenario] = {}
        for size in sizes:
            filename = os.path.join(input_dir, f"{scenario}_{size}.json")
            instance = load_instance(filename)
            case_result: Dict[str, Any] = {}
            for strategy_name in ["earliest_finish_resource_aware", "highest_weight_to_resource_ratio"]:
                repeats = 3 if size <= 100 else 1
                result, avg_time = benchmark_solver(strategy_name, instance, repeats=repeats)
                case_result[strategy_name] = result
                write_json(
                    os.path.join(results_dir, f"{scenario}_{size}_{strategy_name}.json"),
                    result,
                )

            if size <= 15:
                brute_force_result, _ = benchmark_solver("brute_force_optimal", instance, repeats=1)
                case_result["brute_force_optimal"] = brute_force_result
                optimal_weight = brute_force_result["total_weight"]
                for strategy_name in ["earliest_finish_resource_aware", "highest_weight_to_resource_ratio"]:
                    achieved = case_result[strategy_name]["total_weight"]
                    quality = 100.0 if optimal_weight == 0 else (achieved / optimal_weight) * 100.0
                    case_result[strategy_name]["quality_percent_of_optimal"] = round(quality, 2)
            benchmark_summary["large_benchmarks"][scenario][str(size)] = case_result

    for filename in validation_files:
        instance = load_instance(os.path.join(input_dir, filename))
        case_name = filename.replace(".json", "")
        benchmark_summary["validation_against_optimal"][case_name] = {}
        brute_force_result, _ = benchmark_solver("brute_force_optimal", instance, repeats=1)
        benchmark_summary["validation_against_optimal"][case_name]["brute_force_optimal"] = brute_force_result
        write_json(
            os.path.join(results_dir, f"{case_name}_brute_force_optimal.json"),
            brute_force_result,
        )
        optimal_weight = brute_force_result["total_weight"]

        for strategy_name in ["earliest_finish_resource_aware", "highest_weight_to_resource_ratio"]:
            result, _ = benchmark_solver(strategy_name, instance, repeats=5)
            quality = 100.0 if optimal_weight == 0 else (result["total_weight"] / optimal_weight) * 100.0
            result["quality_percent_of_optimal"] = round(quality, 2)
            benchmark_summary["validation_against_optimal"][case_name][strategy_name] = result
            write_json(
                os.path.join(results_dir, f"{case_name}_{strategy_name}.json"),
                result,
            )

    summary_path = os.path.join(results_dir, "benchmark_summary.json")
    write_json(summary_path, benchmark_summary)
    return benchmark_summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-constraint greedy resource scheduler")
    subparsers = parser.add_subparsers(dest="command", required=True)

    solve_parser = subparsers.add_parser("solve", help="Solve one instance with a chosen strategy")
    solve_parser.add_argument("--input", required=True, help="Path to input JSON file")
    solve_parser.add_argument(
        "--strategy",
        required=True,
        choices=list(STRATEGIES.keys()),
        help="Scheduling strategy to run",
    )
    solve_parser.add_argument("--output", required=False, help="Optional output JSON path")

    benchmark_parser = subparsers.add_parser("benchmark", help="Run benchmarks over the generated test cases")
    benchmark_parser.add_argument("--input-dir", required=True, help="Directory containing test case JSON files")
    benchmark_parser.add_argument("--results-dir", required=True, help="Directory where results will be written")

    args = parser.parse_args()

    if args.command == "solve":
        instance = load_instance(args.input)
        result = solve_instance(instance, args.strategy)
        print_result(result)
        if args.output:
            write_json(args.output, result)
    elif args.command == "benchmark":
        summary = run_benchmarks(args.input_dir, args.results_dir)
        print(f"Wrote benchmark summary to: {os.path.join(args.results_dir, 'benchmark_summary.json')}")
        print(f"Scenarios benchmarked: {', '.join(summary['large_benchmarks'].keys())}")


if __name__ == "__main__":
    main()
