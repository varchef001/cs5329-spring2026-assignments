
import json
import os
import time
import tracemalloc

from src.baseline import baseline_course_planner
from src.optimized import optimized_course_planner
from src.validator import validate_course_order
from src.catalog_utils import build_student_course_plan


def load_courses(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def measure_performance(algorithm, courses):
    tracemalloc.start()
    start_time = time.perf_counter()

    success, result = algorithm(courses)

    end_time = time.perf_counter()
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    runtime = end_time - start_time

    if success:
        is_valid, message = validate_course_order(courses, result)
        return runtime, peak_memory, is_valid, message
    else:
        return runtime, peak_memory, False, result


def benchmark_dataset(file_path: str):
    courses = load_courses(file_path)
    dataset_name = os.path.basename(file_path)

    print("=" * 90)
    print(f"Dataset: {dataset_name}")
    print(f"Number of Courses: {len(courses)}")

    baseline_runtime, baseline_memory, baseline_valid, baseline_message = measure_performance(
        baseline_course_planner, courses
    )

    optimized_runtime, optimized_memory, optimized_valid, optimized_message = measure_performance(
        optimized_course_planner, courses
    )

    print("\nBaseline Approach (Repeated Linear Scan)")
    print(f"Runtime: {baseline_runtime:.8f} seconds")
    print(f"Peak Memory: {baseline_memory / 1024:.2f} KB")
    print(f"Valid Output: {baseline_valid}")
    print(f"Message: {baseline_message}")

    print("\nOptimized Approach (Kahn's Topological Sort)")
    print(f"Runtime: {optimized_runtime:.8f} seconds")
    print(f"Peak Memory: {optimized_memory / 1024:.2f} KB")
    print(f"Valid Output: {optimized_valid}")
    print(f"Message: {optimized_message}")

    if optimized_runtime > 0:
        speedup = baseline_runtime / optimized_runtime
        print(f"\nSpeedup (Baseline / Optimized): {speedup:.2f}x")


if __name__ == "__main__":
    print("Course Planner Benchmark Program")
    print("1. Benchmark full dataset directly")
    print("2. Benchmark filtered student plan from master catalog")
    mode = input("Enter 1 or 2: ").strip()

    file_path = input("Enter dataset path: ").strip()
    all_courses = load_courses(file_path)

    if mode == "1":
        benchmark_dataset(file_path)

    elif mode == "2":
        program = input("Enter program exactly as in dataset: ").strip()
        concentration = input("Enter concentration exactly as in dataset: ").strip()

        raw_electives = input(
            "Enter elective course IDs separated by commas (or press Enter to skip): "
        ).strip()

        elective_ids = [x.strip() for x in raw_electives.split(",") if x.strip()] if raw_electives else []

        selected_courses = build_student_course_plan(
            all_courses,
            program,
            concentration,
            elective_ids
        )

        print(f"\nFiltered plan contains {len(selected_courses)} courses.")

        baseline_runtime, baseline_memory, baseline_valid, baseline_message = measure_performance(
            baseline_course_planner, selected_courses
        )

        optimized_runtime, optimized_memory, optimized_valid, optimized_message = measure_performance(
            optimized_course_planner, selected_courses
        )

        print("\nBaseline Approach (Repeated Linear Scan)")
        print(f"Runtime: {baseline_runtime:.8f} seconds")
        print(f"Peak Memory: {baseline_memory / 1024:.2f} KB")
        print(f"Valid Output: {baseline_valid}")
        print(f"Message: {baseline_message}")

        print("\nOptimized Approach (Kahn's Topological Sort)")
        print(f"Runtime: {optimized_runtime:.8f} seconds")
        print(f"Peak Memory: {optimized_memory / 1024:.2f} KB")
        print(f"Valid Output: {optimized_valid}")
        print(f"Message: {optimized_message}")

        if optimized_runtime > 0:
            speedup = baseline_runtime / optimized_runtime
            print(f"\nSpeedup (Baseline / Optimized): {speedup:.2f}x")
    else:
        print("Invalid mode.")
