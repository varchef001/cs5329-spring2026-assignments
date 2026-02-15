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
    # increase version number for this event
    version = current_version.get(event_id, 0) + 1
    current_version[event_id] = version

    # push into heap
    entry = (priority, created_time, version, event_id, payload)
    heapq.heappush(heap, entry)


def discard_stale_top(heap, current_version):
    """
    Removes cancelled or outdated events from the top of the heap.
    """
    while heap:
        priority, created_time, version, event_id, payload = heap[0]

        # if version is outdated, remove it
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

    # mark as processed (invalidate future stale copies)
    del current_version[event_id]

    return (event_id, priority, created_time, payload)


# ---------------- Simulation ---------------- #

def main():
    heap, current_version = create_scheduler()

    # Add at least 6 events
    add_event(heap, current_version, "E1", 3, 1, "IT help desk ticket")
    add_event(heap, current_version, "E2", 1, 2, "Emergency supply request")
    add_event(heap, current_version, "E3", 4, 3, "Tutoring request")
    add_event(heap, current_version, "E4", 2, 4, "Clinic intake")
    add_event(heap, current_version, "E5", 1, 5, "Server outage")
    add_event(heap, current_version, "E6", 5, 6, "General inquiry")

    print("Next event (peek):")
    print(peek_next(heap, current_version))

    print("\nProcessing order:")
    while True:
        event = pop_next(heap, current_version)
        if event is None:
            break
        print(event)


if __name__ == "__main__":
    main()
