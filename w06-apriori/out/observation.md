# Week 06 observations

## Task 1
On the generated data at support 50, item 1468 -> 0 has confidence 0.838710, versus 0 -> 1468 at 0.003976: the useful directional claim is that a buyer of rare item 1468 often also buys item 0; the reverse does not predict 1468. This is the highest-confidence rule, but lift 1.282431 is only a modest association, not causal evidence (the toy diaper -> beer rule has confidence 0.8 and lift 1.12).
For 2,000 items a dense brute-force table needs 1,999,000 pair counters; 1,849 frequent singletons leave a 1,708,476-pair upper bound, while the sparse A-Priori baseline actually holds 820,259 observed-pair counters.

## Task 2
No unbearable threshold was reached: support 1, the lowest meaningful value, completed in 7.86 s with 327.0 MB traced peak; no resource ran out, so a failure boundary cannot honestly be claimed on the fixed dataset (see explosion.md for machine and measurement scope).
Counter growth on successive early halvings was 5.539x, 4.669x and 2.997x, then 1.089x and a plateau at 893,456; this is nonlinear growth followed by saturation, not perpetual doubling.
From 400 to 50 counters grew 77.49x versus 25.69x for answers, requiring 128.2 counters per answer at 50; below 25 counters stayed flat while answers increased, illustrating that the candidate/answer gap depends on the threshold.

## Task 3
I chose 1,000,003 buckets to limit collisions: peak pair counters fell from 820,259 to 23,356 (97.15%) with exactly equal pair counts; 10,007 buckets instead retained all 820,259 counters, so collisions destroyed the filter (details.json).
The 64-bit bucket array costs 8,000,024 payload bytes, and its packed bitmap 125,001 bytes; both coexist briefly before the array is released. Measured total traced algorithm peaks were 8.34 MB for PCY versus 102.29 MB for baseline, including singleton structures and returned results but excluding prebuilt baskets; bucket counters are reported separately from the benchmark's pair-counter metric.
Using baseline's roughly 125 bytes per observed pair as a rough empirical estimate, the fixed 8.34 MB cost crosses over around 67,000 baseline pair counters, provided the bitmap stays selective; there is no universal basket-count cutoff because item skew, support, collisions and output size change it. Smaller datasets may lose to the fixed array, and the traced PCY run was slower despite its memory saving.
