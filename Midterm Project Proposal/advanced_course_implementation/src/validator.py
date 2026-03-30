
from typing import List, Dict, Tuple


def validate_course_order(courses: List[Dict], schedule: List[str]) -> Tuple[bool, str]:
    course_ids = [course["course_id"] for course in courses]

    if len(schedule) != len(course_ids):
        return False, "Schedule length does not match number of selected courses."

    if len(set(schedule)) != len(schedule):
        return False, "Schedule contains duplicate courses."

    if set(schedule) != set(course_ids):
        return False, "Schedule does not contain exactly the selected course set."

    position = {course_id: index for index, course_id in enumerate(schedule)}

    for course in courses:
        course_id = course["course_id"]
        for prereq in course.get("prerequisites", []):
            if prereq not in position:
                return False, f"Missing prerequisite '{prereq}' in schedule."
            if position[prereq] > position[course_id]:
                return False, f"Order violation: prerequisite '{prereq}' appears after '{course_id}'."

    return True, "Schedule is valid."
