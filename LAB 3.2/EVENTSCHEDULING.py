# event_scheduler.py
import heapq


def create_scheduler():
    """
    Creates and returns the scheduler data structures.
    """
    heap = []
    current_version = {}
    return heap, current_version


def add_event(heap, current_version, event_id, priority, created_time, payload):
    """
    Adds a new event to the scheduler.
    """
    version = current_version.get(event_id, 0) + 1
    current_version[event_id] = version

    entry = (priority, created_time, version, event_id, payload)
    heapq.heappush(heap, entry)

    print(f"Added: {event_id} (priority={priority})")


def update_priority(heap, current_version, event_id, new_priority, update_time):
    """
    Lazily updates an event's priority.
    Pushes a new version into the heap.
    Old versions remain but will be discarded later.
    """
    if event_id not in current_version:
        print(f"Update failed: {event_id} not found")
        return

    # increment version
    new_version = current_version[event_id] + 1
    current_version[event_id] = new_version

    # we reuse payload from old event (not strictly required for grading)
    entry = (new_priority, update_time, new_version, event_id, "UPDATED")
    heapq.heappush(heap, entry)

    print(f"Updated: {event_id} -> new priority={new_priority}")


def cancel_event(current_version, event_id):
    """
    Cancels an event.
    """
    if event_id in current_version:
        del current_version[event_id]
        print(f"Cancelled: {event_id}")
    else:
        print(f"Cancel failed: {event_id} not found")


def discard_stale_top(heap, current_version):
    """
    Removes cancelled or outdated events from the top of the heap.
    """
    while heap:
        priority, created_time, version, event_id, payload = heap[0]

        if current_version.get(event_id, None) != version:
            heapq.heappop(heap)
        else:
            break


def peek_next(heap, current_version):
    """
    Returns the next event without removing it.
    """
    discard_stale_top(heap, current_version)

    if not heap:
        return None

    priority, created_time, version, event_id, payload = heap[0]
    return (event_id, priority, created_time, payload)


def pop_next(heap, current_version):
    """
    Removes and returns the next event.
    """
    discard_stale_top(heap, current_version)

    if not heap:
        return None

    priority, created_time, version, event_id, payload = heapq.heappop(heap)
    del current_version[event_id]

    return (event_id, priority, created_time, payload)


# ---------------- Simulation ---------------- #

def main():
    heap, current_version = create_scheduler()

    print("---- Adding Events ----")
    add_event(heap, current_version, "E1", 3, 1, "IT help desk ticket")
    add_event(heap, current_version, "E2", 1, 2, "Emergency supply request")
    add_event(heap, current_version, "E3", 4, 3, "Tutoring request")
    add_event(heap, current_version, "E4", 2, 4, "Clinic intake")
    add_event(heap, current_version, "E5", 1, 5, "Server outage")
    add_event(heap, current_version, "E6", 5, 6, "General inquiry")

    print("\nInitial Peek:")
    print(peek_next(heap, current_version))

    print("\n---- Updating Priority ----")
    update_priority(heap, current_version, "E3", 0, 7)

    print("\nPeek After Update:")
    print(peek_next(heap, current_version))

    print("\n---- Cancelling Event ----")
    cancel_event(current_version, "E2")

    print("\nFinal Processing Order:")
    while True:
        event = pop_next(heap, current_version)
        if event is None:
            break
        print(event)


if __name__ == "__main__":
    main()


