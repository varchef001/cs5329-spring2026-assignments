# Lab 2.1 – Recurrence Experimentation and Analysis

**Course:** CS 5329 – Algorithm Design and Analysis  
**Student Name:** Varshith Gandra  
**Semester:** Spring 2026  

---

## Overview
This lab compares a naive recursive Fibonacci implementation with a dynamic programming
(memoized) implementation. The goal is to observe how runtime changes as input size grows
and explain the performance difference using Big-O notation and recurrence intuition.

---

## How to Run the Code
From the repository root folder, run:

```bash
python Lab2.1/assignment2_fibonacci.py

Analysis Questions
a) Why does fib_recursive slow down as n increases?

Because it keeps solving the same Fibonacci values again and again, so the number of function calls becomes very large.

b) What is the Big-O time complexity of each approach?

fib_recursive: O(2ⁿ) (exponential)

fib_dp: O(n) (linear)

c) Would fib_recursive(50) be feasible?

No. It would take too long because the recursive method grows exponentially and makes too many calls.

d) How does memoization change the recurrence?

Memoization saves results, so each Fibonacci value is calculated only once. This reduces runtime from exponential to linear.
