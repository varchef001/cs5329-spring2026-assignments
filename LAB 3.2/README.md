# Week 2 – Event Scheduler Extension

## Overview
This project extends the event scheduler to support priority updates and event cancellations using a lazy update strategy. Since Python's heap does not support efficient in-place updates, the scheduler pushes a new version of an event into the heap whenever its priority changes. Old versions remain in the heap but are ignored later using version tracking.

## Runtime Analysis

The operation that dominates runtime in this scheduler is heap insertion and removal, which both run in O(log n) time. Every add, update, or pop operation requires interacting with the heap, making these the most expensive operations.

Scanning a list to find the next highest-priority event would take O(n) time per operation, which becomes inefficient as the number of events increases.

Lazy updating is acceptable in practice because it avoids costly in-place heap modifications. Although outdated entries remain temporarily in the heap, they are efficiently discarded later, keeping the overall system fast and scalable
