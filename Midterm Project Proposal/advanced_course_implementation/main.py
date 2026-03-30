
import json
from src.baseline import baseline_course_planner
from src.optimized import optimized_course_planner
from src.validator import validate_course_order
from src.catalog_utils import (
    get_available_programs,
    get_available_concentrations,
    get_electives,
    build_student_course_plan,
)


def load_courses(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def display_course_schedule(courses, order):
    lookup = {course["course_id"]: course for course in courses}

    print("\nGenerated Course Schedule:\n")
    for index, course_id in enumerate(order, start=1):
        course = lookup.get(course_id, {})
        print(
            f"{index}. {course_id} - {course.get('course_name', course_id)} "
            f"[{course.get('program', '')} | {course.get('concentration', '')} | {course.get('category', '')}]"
        )


def choose_from_list(options, title):
    print(f"\n{title}")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")

    while True:
        choice = input("Enter choice number: ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(options):
                return options[idx - 1]
        print("Invalid choice. Try again.")


def choose_electives(electives):
    if not electives:
        return []

    print("\nAvailable Electives:")
    for i, course in enumerate(electives, start=1):
        print(f"{i}. {course['course_id']} - {course['course_name']}")

    raw = input("\nEnter elective numbers separated by commas (or press Enter to skip): ").strip()

    if not raw:
        return []

    selected_ids = []
    parts = [part.strip() for part in raw.split(",") if part.strip()]

    for part in parts:
        if part.isdigit():
            idx = int(part)
            if 1 <= idx <= len(electives):
                selected_ids.append(electives[idx - 1]["course_id"])

    return selected_ids


if __name__ == "__main__":
    file_path = input("Enter dataset path: ").strip()
    all_courses = load_courses(file_path)

    programs = get_available_programs(all_courses)
    program = choose_from_list(programs, "Available Programs:")

    concentrations = get_available_concentrations(all_courses, program)
    if concentrations:
        concentration = choose_from_list(concentrations, "Available Concentrations:")
    else:
        concentration = "Core"

    electives = get_electives(all_courses, program, concentration)
    chosen_elective_ids = choose_electives(electives)

    selected_courses = build_student_course_plan(
        all_courses,
        program,
        concentration,
        chosen_elective_ids
    )

    print("\nSelected Course Set:")
    for course in selected_courses:
        print(
            f"{course['course_id']} - {course['course_name']} "
            f"[{course['concentration']} | {course['category']}]"
        )

    print("\nChoose algorithm:")
    print("1. Baseline (Repeated Linear Scan)")
    print("2. Optimized (Topological Sort - Kahn's Algorithm)")
    algo_choice = input("Enter 1 or 2: ").strip()

    if algo_choice == "1":
        success, result = baseline_course_planner(selected_courses)
        method = "Baseline"
    elif algo_choice == "2":
        success, result = optimized_course_planner(selected_courses)
        method = "Optimized"
    else:
        print("Invalid choice.")
        raise SystemExit

    print(f"\n{method} Result:")

    if success:
        is_valid, message = validate_course_order(selected_courses, result)
        display_course_schedule(selected_courses, result)
        print(f"\nValidation Status: {message}")
    else:
        print(result)
