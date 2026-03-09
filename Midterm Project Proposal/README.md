# Building an Efficient Course Planner Using Graphs

**Names:** Varshith Gandra, Raja Brahmendra  
**TXST IDs:** VUP13, KGM120

## 1. Problem Statement

The problem we want to solve is how to generate a valid order for taking college courses when some courses have prerequisites. This is a useful problem because students often know which courses they need, but it can be hard to figure out the correct sequence, especially when several courses depend on each other.

The input for this project will be a dataset of courses and their prerequisites. We will most likely store the data in either **JSON** or **CSV** format because both are simple to work with in Python. Each course record will include a course ID, such as `CS101` or `MATH201`, and a list of prerequisite courses. For example, if `CS201` requires `CS102`, that relationship will be stored in the data. We plan to start with a dataset of around **50 to 200 courses**, which is realistic for a department or degree plan, and then create larger synthetic datasets to test performance.

The output of the program will be a valid course order that satisfies all prerequisite rules. A correct result means that every prerequisite must appear earlier in the order than the course that depends on it. If the input contains a cycle, such as Course A requiring Course B while Course B also requires Course A, then the program should report that no valid schedule exists instead of returning an incorrect result.

Our main performance goal is for the program to run quickly and reliably. For normal-sized datasets, we want the result to be generated in **well under one second**. We also want the program to stay within a reasonable memory limit, such as **under 512 MB**, although we do not expect memory to be a major issue for this project.

## 2. Motivation

We think this is an interesting problem because course planning is something almost every student deals with, and it becomes confusing when there are many prerequisite chains. A naive solution could repeatedly scan the same list of courses over and over, which is not efficient. This project will help show how choosing the right data structure and algorithm makes a problem easier to solve, faster to run, and more reliable when the input gets larger.

## 3. Candidate Approaches

### Approach A: Baseline

**Algorithm/Data Structure:** Repeated Linear Scan

The baseline approach will be a simple method that repeatedly checks the full list of courses. The program will keep track of which courses are already completed or added to the schedule. Then it will scan all remaining courses and look for any course whose prerequisites have already been satisfied. Once it finds one, it adds it to the schedule and continues the process until either all courses are scheduled or no progress can be made.

This approach is easy to understand, but it is not very efficient because the algorithm may need to scan the entire list many times before finishing.

**Theoretical Complexity:**  
- **Time:** O(n²) in many cases  
- **Space:** O(n)

### Approach B: Optimized

**Algorithm/Data Structure:** Graph + Topological Sort

The optimized approach will represent the courses as a directed graph. Each course will be a node, and each prerequisite relationship will be a directed edge. For example, if `CS101` must be taken before `CS102`, then there will be an edge from `CS101` to `CS102`.

We will then use **topological sort**, most likely **Kahn’s algorithm**, to generate a valid order. This works by first finding all courses with no prerequisites, then removing them one by one while updating the courses that depend on them. If at the end all courses have been processed, then a valid schedule exists. If not, that means there is a cycle.

This approach is much more natural for the problem because prerequisite relationships already form a graph structure.

**Theoretical Complexity:**  
- **Time:** O(V + E)  
- **Space:** O(V + E)

Where:  
- **V** = number of courses  
- **E** = number of prerequisite relationships  

## 4. Evaluation Plan

To evaluate runtime, we will use Python’s `time.perf_counter()` so we can compare how long the baseline and optimized approaches take on the same datasets.

To measure memory usage, we will use `tracemalloc` in Python. This will help us compare how much memory each approach uses while running.

To test correctness, we will write a validation function that checks whether every course appears after all of its prerequisites in the final output. We will also include cycle test cases to make sure the program correctly reports when no valid schedule exists.

To make the results more realistic, we will test multiple kinds of datasets, including:
- simple chain structures
- branching prerequisite structures
- random prerequisite graphs
- disconnected course groups
- cyclic graphs for invalid cases

This will help us see how the algorithms behave under different conditions, not just one example.

## 5. Dataset Plan

The main dataset for this project will be **synthetic**, because that gives us full control over the number of courses and the structure of the prerequisite relationships. We can create both valid and invalid cases and scale the data size up for testing.

We may also use a small sample from a real university course catalog to make the project feel more realistic. If we do that, we will manually collect course IDs and prerequisites from a public course catalog and convert them into JSON or CSV format.

For synthetic generation, we will create course names like `CS101`, `CS102`, `CS201`, and so on, then assign prerequisites in a controlled way. For valid graphs, we will only assign prerequisites from earlier-numbered courses so we do not accidentally create cycles unless we want to test that case on purpose.

## 6. Desired Output

The program should produce one of the following:

1. A valid ordering of all courses where every prerequisite appears before the course that depends on it.
2. A message saying that no valid ordering exists because the prerequisite graph contains a cycle.

A correct result means:
- each course appears only once
- every prerequisite appears before the course that requires it
- all courses are included if the graph is valid
- cycles are detected and reported correctly

### Example Valid Output
```text
CS101 -> MATH101 -> CS102 -> MATH102 -> CS201 -> CS301