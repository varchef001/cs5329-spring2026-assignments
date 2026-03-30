
import json
from typing import List, Dict, Tuple, Union


def load_courses(file_path: str) -> List[Dict]:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def baseline_course_planner(courses: List[Dict]) -> Tuple[bool, Union[List[str], str]]:
    """
    Baseline approach:
    Repeatedly scans remaining courses and schedules those whose prerequisites
    are already completed.
    """

    remaining = {}
    all_course_ids = set()

    for course in courses:
        course_id = course["course_id"]
        prereqs = set(course.get("prerequisites", []))
        remaining[course_id] = prereqs
        all_course_ids.add(course_id)

    for course_id, prereqs in remaining.items():
        for prereq in prereqs:
            if prereq not in all_course_ids:
                return False, f"Invalid dataset: prerequisite '{prereq}' for course '{course_id}' is missing."

    completed = []
    completed_set = set()

    while remaining:
        progress = False
        ready_courses = []

        for course_id, prereqs in remaining.items():
            if prereqs.issubset(completed_set):
                ready_courses.append(course_id)

        ready_courses.sort()

        for course_id in ready_courses:
            completed.append(course_id)
            completed_set.add(course_id)
            del remaining[course_id]
            progress = True

        if not progress:
            return False, "No valid course ordering exists because the prerequisite graph contains a cycle."

    return True, completed
