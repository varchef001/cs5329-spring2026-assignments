# Activity 3 – Event Scheduler (Heap-Based Priority Queue)

**Name:** Varshith Gandra  
**Student ID:** vup13  

---

## Overview

This project implements a basic event scheduler using a heap-based priority queue in Python. 
The scheduler simulates real-world systems such as clinic intake processing, IT help desk 
ticket management, transportation dispatch, and emergency coordination systems.

The system always processes the most urgent valid event first.

Each event is stored as a tuple:

(priority, created_time, version, event_id, payload)

Lower priority values indicate more urgent events. The created_time field ensures fair 
tie-breaking when two events share the same priority. The version field helps detect 
outdated or replaced events.

---

## Why a Heap is Better Than a List or Array

A heap is more efficient than a list or array for this scheduler because it allows us 
to insert and remove priority-based events in O(log n) time. If we used a list, we would 
need to sort the list after every insertion (O(n log n)) or scan the entire list to 
find the most urgent event (O(n)). Since this system repeatedly retrieves the next 
most urgent event, using a heap significantly improves performance.

Heaps are specifically designed for priority queue operations, making them the 
natural choice for event-driven systems.

---

## Core Repeated Operation

The operation performed most frequently in this system is retrieving and removing 
the highest-priority event. This operation happens every time the scheduler processes 
a request. Because heap removal (heappop) runs in O(log n) time, the scheduler remains 
efficient even as the number of events grows large.

---

## Key Operations Implemented

- Creating a scheduler
- Adding events
- Peeking at the next event
- Removing the next event
- Skipping stale or outdated events

---

## Time Complexity Summary

- Adding an event: O(log n)
- Peeking at the next event: O(1) (after stale cleanup)
- Removing the next event: O(log n)
- Discarding stale events: Amortized O(log n)

This ensures the scheduler scales efficiently for large event queues.

---

## Real-World Connection

Heap-based schedulers are widely used in:

- Operating systems (process scheduling)
- Network packet routing
- Simulation engines
- Cloud job schedulers
- Emergency response systems

This assignment demonstrates how algorithmic efficiency directly impacts 
real-world system performance.
