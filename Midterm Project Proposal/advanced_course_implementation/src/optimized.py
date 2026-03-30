
import json
from collections import defaultdict, deque
from typing import List, Dict, Tuple, Union


def load_courses(file_path: str) -> List[Dict]:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def optimized_course_planner(courses: List[Dict]) -> Tuple[bool, Union[List[str], str]]:
    """
    Optimized approach:
    Graph + Kahn's topological sort
    """

    graph = defaultdict(list)
    in_degree = {}
    all_course_ids = set()

    for course in courses:
        course_id = course["course_id"]
        in_degree[course_id] = 0
        all_course_ids.add(course_id)

    for course in courses:
        course_id = course["course_id"]
        for prereq in course.get("prerequisites", []):
            if prereq not in all_course_ids:
                return False, f"Invalid dataset: prerequisite '{prereq}' for course '{course_id}' is missing."

            graph[prereq].append(course_id)
            in_degree[course_id] += 1

    zero_in_degree = deque(sorted([cid for cid, deg in in_degree.items() if deg == 0]))
    ordered_courses = []

    while zero_in_degree:
        current = zero_in_degree.popleft()
        ordered_courses.append(current)

        for neighbor in sorted(graph[current]):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                zero_in_degree.append(neighbor)

    if len(ordered_courses) != len(courses):
        return False, "No valid course ordering exists because the prerequisite graph contains a cycle."

    return True, ordered_courses
