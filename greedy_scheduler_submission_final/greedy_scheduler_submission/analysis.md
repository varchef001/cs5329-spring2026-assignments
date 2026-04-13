# Analysis

## Part 1 — Greedy Strategy Design

### Strategy 1: Earliest Finish with Resource-Aware Filtering

**Greedy-choice idea.** This strategy sorts tasks by the earliest finishing time and then accepts a task only if it can be added without breaking the resource-capacity or category-overlap constraints. The main idea is that a task that ends early gives back both time and resource capacity earlier, so there should be more room left for future tasks. In standard interval scheduling, earliest finish is optimal because it preserves the most remaining timeline. Here I used the same intuition, but I added feasibility checks because this problem is harder than normal interval scheduling.

This strategy is expected to do well when tasks are fairly spread out, when weights are not drastically different, and when preserving future time windows matters more than chasing one heavy task. In sparse test cases, finishing early usually keeps the schedule flexible and makes it easier to accept later jobs. It can also work well when category limits are not very restrictive and when the resource capacity is high enough that the main issue is time overlap rather than resource overload.

A clear failure case can still happen. Suppose `R = 5` and `K = 2`. Let one long task be `A = (0, 40, 12, 5, compute)`. Now add four short tasks: `B1 = (0, 10, 2.2, 5, io)`, `B2 = (10, 20, 2.1, 5, network)`, `B3 = (20, 30, 2.2, 5, io)`, and `B4 = (30, 40, 2.1, 5, network)`. The earliest-finish rule will choose the short tasks because they end first, but their total weight is only `8.6`. The optimal solution is just `A` with weight `12`. So the heuristic keeps future windows open, but it can still lose to a single better global choice.

### Strategy 2: Highest Weight-to-Resource Ratio with Compatibility Checking

**Greedy-choice idea.** This strategy sorts by decreasing `weight / resource`, then breaks ties using larger weight, shorter duration, earlier finish time, and smaller resource demand. The basic intuition is that a task should be judged by how much value it gives for each unit of scarce resource it consumes. Since capacity is checked at every overlapping part of the timeline, this rule tries to make each local choice as efficient as possible. The compatibility test is still necessary because a task that looks great by itself can still cause an invalid schedule once overlapping tasks are considered.

This strategy is expected to perform better when resource pressure is the main difficulty: dense overlap, tight capacity, and strong variation in resource demand or value. In those situations, value density matters more than simply finishing early. The rule often does a good job of leaving enough space for other useful tasks instead of letting one bulky low-value task take too much of the available capacity.

But this strategy can fail too. Consider `R = 3` and `K = 2`. Let `A = (0, 10, 9, 1, compute)`, so its ratio is `9`. Now define `B1 = (0, 4, 4, 2, io)`, `B2 = (4, 7, 4, 2, network)`, and `B3 = (7, 10, 4, 2, io)`, each with ratio `2`. The ratio rule chooses `A` first because `9 > 2`, but after taking `A`, none of the `B` tasks can overlap with it because `1 + 2 = 3` already uses all capacity. The greedy total is `9`, while the better solution is `B1 + B2 + B3 = 12`. So the ratio rule can overvalue one task with a strong local score and miss a better combination of medium tasks.

## Part 2 — Brute-Force Baseline

The brute-force solver checks every subset for inputs with `n <= 15`, verifies all constraints, and keeps the feasible subset with the highest total weight. I used it as the exact baseline for five small validation cases:

| Validation case | Optimal weight | Earliest-finish quality | Ratio quality | Brute-force time (s) |
|---|---:|---:|---:|---:|
| validation_sparse_8 | 40.77 | 100.00% | 100.00% | 0.000267 |
| validation_dense_10 | 18.76 | 78.62% | 81.72% | 0.002313 |
| validation_category_12 | 26.92 | 100.00% | 100.00% | 0.008624 |
| validation_adversarial_10 | 12.00 | 72.58% | 100.00% | 0.002044 |
| validation_identical_6 | 16.00 | 100.00% | 100.00% | 0.000206 |

Average quality across these five exact comparisons was **90.24%** for earliest-finish and **96.34%** for the weight/resource strategy.

## Part 3 — Benchmarking and Analysis

### Generated scenarios

I generated four required scenario families:

1. **Sparse** — relatively separated tasks, high capacity, mild contention.
2. **Dense** — many overlapping tasks, tighter resource capacity, stronger competition.
3. **Category-heavy** — most tasks share one category while `K` is small.
4. **Adversarial** — intentionally built so earliest-finish gets trapped by short low-weight tasks while the ratio rule takes one better long task.

I also kept the weights fairly small across the test files. The largest generated weight is only `12.0`, which keeps the data simple and makes the adversarial behavior easier to see.

### Runtime comparison table

The following table reports the **average greedy runtime across the four scenario families** for the required input sizes.

| n | Earliest-finish avg time (s) | Ratio avg time (s) |
|---|---:|---:|
| 10 | 0.000057 | 0.000048 |
| 50 | 0.000476 | 0.000208 |
| 100 | 0.000455 | 0.000481 |
| 500 | 0.005128 | 0.005935 |
| 1000 | 0.014674 | 0.018660 |

### Quality snapshots on the `n = 10` benchmark cases

| Scenario | Earliest-finish quality | Ratio quality |
|---|---:|---:|
| sparse | 100.00% | 100.00% |
| dense | 81.91% | 87.00% |
| category-heavy | 79.27% | 94.31% |
| adversarial | 75.58% | 100.00% |

### 300-word analysis

Overall, the **highest weight-to-resource ratio** strategy performed better on the exact small comparisons. Its average quality on the five validation cases was 96.34%, while earliest-finish averaged 90.24%. The same general trend appears in the `n = 10` benchmark cases. Both strategies were perfect on sparse data, which makes sense because sparse schedules do not force many painful choices. Once overlap and competition increased, the ratio rule was usually stronger. It beat earliest-finish on dense data, category-heavy data, and the adversarial case.

The adversarial family was built on purpose so that one algorithm would clearly fail. I used one long task with weight `12.0` and several duplicated short tasks in four fixed windows, each with weight a little above `2`. The earliest-finish strategy kept grabbing the short tasks because they ended first, so on `validation_adversarial_10` it only reached **72.58%** of optimal. The ratio rule chose the long task immediately and reached **100%**. This made the failure mode easy to explain and easy to see in the output files.

The ratio strategy still was not perfect everywhere. Dense cases remained hard because many tasks overlapped and the resource capacity was tight. In those inputs, even a good local ratio can block a better later combination. The category-heavy cases also showed that category limits create another layer of conflict. At `n = 100`, earliest-finish scored `68.79`, while the ratio rule scored `63.30`. At `n = 1000`, earliest-finish again came out ahead in that scenario, `710.10` versus `657.67`. That swing is useful because it shows that neither rule dominates every single case. Once many tasks share the same category, local scoring becomes less reliable because each accepted task also uses one of the limited category overlap slots.

So my conclusion is that the ratio strategy was better overall, but the category constraint and overlap structure made both heuristics fail in predictable ways.

## Part 4 — Reflection

I do not think this problem can be solved optimally by one simple greedy rule in general. The reason is that accepting one task changes several future possibilities at the same time: remaining time overlap, remaining resource capacity during every affected segment, and remaining category slots for that label. Those effects are global, not local. A task that looks best under one rule such as earliest finish or value density can still block a better combination later. That is exactly what the counterexamples show.

For a greedy algorithm to be guaranteed optimal, the problem would need a much stronger structure, such as a matroid-like exchange property or some rule showing that every locally best choice can always be extended to a globally best solution. Classic unweighted interval scheduling has that property. This problem does not.

In a production system, I would use greedy only as a fast heuristic or starting point. For better solutions, I would combine it with something more global such as integer linear programming, constraint programming, branch-and-bound, or a local-search improvement phase.
