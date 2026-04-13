# Analysis

## Part 1 - Greedy Strategy Design

### Strategy 1: Earliest Finish with Resource-Aware Filtering

This strategy sorts tasks by the earliest finishing time and then goes through them one by one. A task is added only if it does not break the resource capacity rule or the category overlap rule. The main greedy idea is that if a task finishes early, it leaves more room later in the timeline. That is the same basic reason why earliest-finish works for the classic interval scheduling problem. Here the problem is harder because I also have to check resources and categories, so I cannot just blindly take the next earliest task.

I expect this to work best when the tasks are more spread out and when weights are not too different from each other. In that type of input, keeping the timeline open is usually a good choice, and the schedule can fit more jobs overall. It also tends to do better when resource capacity is not extremely tight, because then the main issue is usually time overlap instead of heavy resource conflict.

A simple counterexample is when one long task has much higher weight than several short tasks. Example: let `R = 5` and `K = 2`. Suppose `A = (0, 10, 60, 5, compute)`. Also suppose there are five short tasks `B1` to `B5`, each using all 5 resources, each worth 8, and together covering the same time range in small pieces. Earliest-finish picks the short tasks first and gets total weight 40, but the optimal answer is just taking `A` with weight 60. So this rule can miss the best total weight even though it keeps the schedule flexible.

### Strategy 2: Highest Weight-to-Resource Ratio with Compatibility Checking

This strategy sorts tasks by decreasing `weight / resource`. After that, it checks whether each task can still be added without breaking feasibility. The greedy idea here is that resource capacity is limited, so I want to spend that resource on tasks that give the most value per unit. I also used tie-breakers like larger weight, shorter duration, earlier finish time, and smaller resource use so that the order is stable.

I expect this strategy to work better when the overlap is dense and the main problem is resource pressure. In those cases, a task with good value density is often a better local choice than a task that just finishes early. It is also useful when weights vary a lot, because then taking tasks with better weight/resource ratio can protect the schedule from wasting capacity on low-value jobs.

But it also fails sometimes. Example: let `R = 3` and `K = 2`. Task `A = (0, 10, 45, 3, compute)` has ratio 15. Then let `B1 = (0, 4, 20, 2, io)`, `B2 = (4, 7, 20, 2, network)`, and `B3 = (7, 10, 20, 2, io)`, each with ratio 10. The ratio rule chooses `A` first because 15 is bigger than 10. After that, the `B` tasks cannot fit with it because of resource capacity. So greedy gets 45, but the optimal answer is `B1 + B2 + B3 = 60`.

## Part 2 - Brute-Force Baseline

The brute-force solver checks every subset for `n <= 15`. For each subset it checks all three constraints, and then keeps the feasible subset with the highest total weight. I used it as the exact answer for five small validation cases.

| Validation case | Optimal weight | Earliest-finish quality | Ratio quality | Brute-force time (s) |
|---|---:|---:|---:|---:|
| validation_sparse_8 | 126.13 | 100.00% | 100.00% | 0.000426 |
| validation_dense_10 | 93.32 | 82.12% | 80.60% | 0.002663 |
| validation_category_12 | 129.45 | 100.00% | 100.00% | 0.008955 |
| validation_adversarial_10 | 106.93 | 67.05% | 100.00% | 0.001951 |
| validation_identical_6 | 40.00 | 100.00% | 100.00% | 0.000204 |

Average quality over these five exact comparisons was **89.83%** for earliest-finish and **96.12%** for the weight/resource ratio strategy.

## Part 3 - Benchmarking and Analysis

### Test scenarios

I generated these four scenario groups:

1. **Sparse** - fewer conflicts and higher capacity.
2. **Dense** - many overlaps and tighter resources.
3. **Category-heavy** - most tasks share one category and `K` is small.
4. **Adversarial** - made on purpose to hurt one greedy choice.

### Runtime table

This table shows the average greedy runtime across the four scenario groups.

| n | Earliest-finish avg time (s) | Ratio avg time (s) |
|---|---:|---:|
| 10 | 0.000055 | 0.000051 |
| 50 | 0.000548 | 0.000222 |
| 100 | 0.000576 | 0.000545 |
| 500 | 0.006673 | 0.006980 |
| 1000 | 0.023630 | 0.024348 |

### Quality on the `n = 10` benchmark cases

| Scenario | Earliest-finish quality | Ratio quality |
|---|---:|---:|
| sparse | 100.00% | 100.00% |
| dense | 84.89% | 89.10% |
| category-heavy | 81.97% | 95.08% |
| adversarial | 71.70% | 100.00% |

### 300-word discussion

Overall, the `highest_weight_to_resource_ratio` strategy did better on the exact small-case comparisons. Its average quality on the five validation cases was 96.12%, while earliest-finish got 89.83%. The same general pattern also appeared on the `n = 10` scenario benchmarks. Both methods were perfect on sparse data, but the ratio-based rule did better on dense, category-heavy, and adversarial small cases. My guess is that this happened because the harder inputs were driven more by resource pressure than by timeline flexibility. A short task is not always a good pick if it still uses too much capacity for the value it gives.

Earliest-finish struggled the most on adversarial inputs with lots of short, low-value tasks versus one longer, high-value task. In `validation_adversarial_10`, it only got 67.05% of the optimal weight because it committed early to tasks that looked locally safe but were not globally best. The ratio strategy also has weak spots though. In some dense and larger adversarial cases, one high-density task can block a chain of medium tasks that together are better. So even though the ratio heuristic was better overall, it is still only making a local choice.

The category constraint also mattered a lot. It made the problem less local because taking a task uses not only resource capacity, but also one overlap slot for that category. That means a task can look good by weight or ratio and still be a bad decision if it blocks too many future tasks from the same label. On some category-heavy inputs this changed the results noticeably. So my main takeaway is that the ratio strategy was stronger overall, but both heuristics still depend a lot on the structure of the instance.

One more thing I noticed is that the better greedy rule depended a lot on what was making the instance hard. When time windows were the main issue, earliest-finish was sometimes competitive. When resource pressure and category conflicts were the main issue, the ratio rule was usually stronger. That is why I think testing several different scenario types mattered more than looking at only one benchmark family.

## Part 4 - Reflection

I do not think a single simple greedy strategy can always solve this problem optimally. One choice affects several things at the same time: time overlap, resource usage, and category overlap. Because of that, a task that looks best right now can still block a better combination later. That means the problem does not have the kind of structure where one local rule always leads to the global best answer.

For greedy to be guaranteed optimal, the problem would need a stronger property, something like an exchange property where a locally best choice can always be part of an optimal solution. That is true for some simpler scheduling problems, but not for this one.

If I had to solve this in a real production system, I would still keep greedy because it is fast. But I would use it as a first pass or warm start, and then combine it with something stronger like integer programming, constraint programming, branch-and-bound, or local search to improve the answer.
