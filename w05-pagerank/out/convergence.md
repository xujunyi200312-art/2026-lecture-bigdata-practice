# PageRank convergence measurements

## Machine and method

Local Windows 11 (build 26200), Intel Core i9-14900HX, 31.74 GiB usable physical RAM, Python 3.12.14. ChatGPT/Codex, Chrome, Douyin and HipsDaemon were running. Times are single-run wall-clock measurements, so small timing differences include background load and timer noise.

All runs use the unmodified bench.build() generator with seed 246, uniform initial ranks and a maximum of 500 iterations. The stopping condition is L1 change < tolerance. Every recorded run stopped before the cap.

## Prediction before changing graph size

Prediction before the size experiment: increasing the graph from 1,200 to 20,000 nodes should increase time per iteration because there are more edges and nodes to visit. Iteration count need not increase in proportion: it depends on mixing, beta and tolerance, and the generated graphs have similar structure.

## Measured iteration curve

| Nodes | Beta | L1 tolerance | Iterations | Seconds |
| ---: | ---: | ---: | ---: | ---: |
| 1,200 | 0.5 | 1e-10 | 14 | 0.008929 |
| 1,200 | 0.7 | 1e-10 | 17 | 0.010722 |
| 1,200 | 0.85 | 1e-10 | 20 | 0.012699 |
| 1,200 | 0.95 | 1e-10 | 23 | 0.014453 |
| 1,200 | 0.99 | 1e-10 | 24 | 0.015099 |
| 20,000 | 0.85 | 1e-10 | 21 | 0.245061 |
| 20,000 | 0.95 | 1e-10 | 24 | 0.283124 |
| 1,200 | 0.85 | 1e-04 | 9 | 0.005711 |
| 1,200 | 0.85 | 1e-06 | 12 | 0.007484 |
| 1,200 | 0.85 | 1e-03 | 7 | 0.004373 |

## Beta and the shape of convergence (A3)

At 1,200 nodes and tolerance 1e-10, increasing beta from 0.50 to 0.99 raises the iteration count from 14 to 24 (14, 17, 20, 23, 24). Teleportation becomes rarer, so link-following structure and traps retain influence longer. For the stochastic transition operator P, the update contracts L1 differences by at most beta: ||beta P(r-s)||_1 <= beta ||r-s||_1. The worst-case contraction bound weakens as beta approaches 1; actual mixing and the starting vector determine the observed rate. This graph still converges quickly even at 0.99; slow convergence is not inevitable for every graph.

## Graph size: iterations versus elapsed time (A4)

At beta=0.85, 1,200 -> 20,000 nodes (16.67x) changes iterations 20 -> 21, but time 0.012699 -> 0.245061 seconds (19.30x).
At beta=0.95, 1,200 -> 20,000 nodes (16.67x) changes iterations 23 -> 24, but time 0.014453 -> 0.283124 seconds (19.59x).

The prediction holds: iteration counts barely grow, whereas each iteration visits substantially more nodes and edges. The generated graphs have similar structure, but they are different graphs, so identical iteration counts are not guaranteed. Size determines work per iteration, while mixing, beta and tolerance govern how many iterations are needed.

## Tolerance and the cost of extra digits (A5)

For beta=0.85 and 1,200 nodes, tolerances 1e-3, 1e-4, 1e-6 and 1e-10 require 7, 9, 12 and 20 iterations. Tightening 1e-3 -> 1e-4 costs 2 iterations for one digit; 1e-4 -> 1e-6 costs 3 for two digits (1.5 per digit); 1e-6 -> 1e-10 costs 8 for four digits (2 per digit). Across seven extra digits the average is 13/7 = 1.86 iterations per digit. These are measured convergence-threshold digits, not a guarantee of that many accurate decimal places in every rank.

## Top-10 stability (A6)

| Beta | Top 10, in descending rank order |
| ---: | --- |
| 0.5 | p00009, p00001, p00006, p00005, p00003, p00002, p00000, p00004, p00007, p00008 |
| 0.7 | p00009, p00001, p00006, p00005, p00003, p00002, p00004, p00000, p00007, p00008 |
| 0.85 | p00009, p00001, p00006, p00005, p00003, p00002, p00004, p00000, p00007, p00008 |
| 0.95 | p00009, p00001, p00006, p00005, p00003, p00002, p00004, p00000, p00007, p00008 |
| 0.99 | p00009, p00001, p00006, p00005, p00003, p00002, p00004, p00000, p00007, p00008 |

The first change among the tested beta values is at 0.70: p00004 and p00000 exchange positions 7 and 8 compared with beta=0.50. Membership of the top 10 and the first six positions are stable; the exact order is not. No further change occurs at 0.85, 0.95 or 0.99. This only brackets the first observed transition between 0.50 and 0.70, rather than identifying an exact critical beta. A published ranking should disclose beta, because small ordering differences can depend on that modelling choice.
