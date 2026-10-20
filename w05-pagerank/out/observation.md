# Week 5 observations

## Task 1
In the broken version, a dead end sends no contribution, so its rank disappears; I redistribute that mass uniformly over all nodes (the dead-end example changes from total rank 0 to 1).
Uniform redistribution prevents leakage, and uniform teleportation lets the surfer escape a spider trap; together they conserve probability and keep outside nodes reachable (A=0.0375 and B=0.069375 in the repaired trap).
Beta is the probability of following an outgoing link; with probability 1-beta the surfer jumps to a uniformly chosen page, while a dead-end surfer always chooses a page uniformly.

## Task 2
For 1,200 nodes at tolerance 1e-10, beta 0.50 -> 0.99 raises iterations 14 -> 24: less teleportation weakens the contraction bound and lets graph structure persist longer.
Increasing size to 20,000 nodes raises iterations only 20 -> 21 at beta=0.85, but time 0.012699 -> 0.245061 seconds, because each sparse iteration processes more nodes and edges.
The first observed top-10 order change is at beta=0.70, where p00004 overtakes p00000; membership stays unchanged, so exact published ordering should be interpreted with its beta setting.

## Task 3
I reuse the O(n+m) adjacency list and keep two n-element rank vectors, with a conservative 16 scalar/temporary float slots: 2n+16=2,416 versus the harness baseline's 1,440,000 matrix slots (596.0x fewer; 63.6x faster in this run). This counts numeric slots, not total Python memory in bytes.
Teleportation and dangling redistribution supply the same scalar base to every node, so initializing one length-n vector costs O(n), and distributing contributions over existing edges costs O(m); no n-by-n matrix is needed.
The worst per-node difference from the dense answer is 1.17e-15, below 1e-9; the tiny discrepancy comes from floating-point rounding when additions and multiplication by beta are grouped differently.
