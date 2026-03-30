
from typing import List, Dict, Set


def get_available_programs(courses: List[Dict]) -> List[str]:
    return sorted(set(course["program"] for course in courses))


def get_available_concentrations(courses: List[Dict], program: str) -> List[str]:
    concentrations = {
        course["concentration"]
        for course in courses
        if course["program"] == program and course["concentration"] != "Core"
    }
    return sorted(concentrations)


def get_electives(courses: List[Dict], program: str, concentration: str) -> List[Dict]:
    return [
        course for course in courses
        if course["program"] == program
        and course["concentration"] == concentration
        and course["category"] == "Elective"
    ]


def build_course_lookup(courses: List[Dict]) -> Dict[str, Dict]:
    return {course["course_id"]: course for course in courses}


def collect_prerequisites(course_id: str, lookup: Dict[str, Dict], selected_ids: Set[str]) -> None:
    if course_id not in lookup:
        return

    for prereq in lookup[course_id].get("prerequisites", []):
        if prereq not in selected_ids:
            selected_ids.add(prereq)
            collect_prerequisites(prereq, lookup, selected_ids)


def build_student_course_plan(
    all_courses: List[Dict],
    program: str,
    concentration: str,
    chosen_elective_ids: List[str]
) -> List[Dict]:
    """
    Build final selected course set:
    - include all Core courses for the chosen program
    - include all Required courses for the chosen concentration
    - include chosen Electives for the chosen concentration
    - include missing prerequisites automatically
    """

    lookup = build_course_lookup(all_courses)
    selected_ids = set()

    for course in all_courses:
        if course["program"] == program and course["category"] == "Core":
            selected_ids.add(course["course_id"])

    for course in all_courses:
        if (
            course["program"] == program
            and course["concentration"] == concentration
            and course["category"] == "Required"
        ):
            selected_ids.add(course["course_id"])

    for elective_id in chosen_elective_ids:
        if elective_id in lookup:
            course = lookup[elective_id]
            if (
                course["program"] == program
                and course["concentration"] == concentration
                and course["category"] == "Elective"
            ):
                selected_ids.add(elective_id)

    original_ids = list(selected_ids)
    for course_id in original_ids:
        collect_prerequisites(course_id, lookup, selected_ids)

    final_courses = [lookup[course_id] for course_id in selected_ids if course_id in lookup]
    final_courses.sort(key=lambda c: c["course_id"])
    return final_courses
