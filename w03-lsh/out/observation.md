# Week 03 observations

## Task 1
One row pass evaluates each hash once per row and updates all columns containing that row; it avoids re-reading the matrix for each column and is compatible with a row stream (the provided API already holds columns in memory).
I reject non-divisible or zero-length signatures and invalid band counts with ValueError rather than silently dropping rows; empty documents retain infinity signatures in Task 1.
S1-S4 estimates 1.0 from only two hashes, while Jaccard is 2/3; more independent hashes reduce sampling variance but increase hashing time and signature storage.

## Task 2
On an Intel(R) Core(TM) i9-14900HX with 31.73 GiB usable RAM and Windows 11, the measured crossover lies between 1,000 and 2,000 documents; Codex/ChatGPT, Douyin and system apps were running.
Doubling n gave brute-time ratios 4.03x, 4.18x, 4.11x, 4.22x, 3.84x, 4.53x, approximately the expected 4x; curve.md contains the timings and memory-scope caveat.
Waiting became unpleasant at n=8,000: brute force took 243.73s, so time ran out first, not RAM; at the largest n, traced peaks were 0.0650 MiB brute and 16.0590 MiB LSH, excluding input.

## Task 3
I chose h=120, b=30, r=4: the approximate step (1/30)^(1/4)=0.4273 is below 0.6, and P(candidate|s=0.6)=1-(1-0.6^4)^30=98.4456%; favoring recall costs more candidates, then exact similarity filters false positives (124 comparisons, 99.9945% avoided, measured recall 100.00%, precision 100.00%).
Moving the step the wrong way with h=120, b=10, r=12 raises it to 0.8254 and lowers P(candidate|s=0.6) to 2.1556%; on the same data, recall fell to 37.19% with 45 comparisons (parameters.json; reproduce with task3_parameters.py).
Hashing is not free: updating signatures costs O(h times total shingle occurrences), with O(nh) signature storage plus postings and buckets; it can dominate small inputs, long documents or low-collision workloads, and 3 million documents need 360 million signature slots before index/candidate overhead. The probability formula assumes independent minhashes; seeded affine hashes approximate that model, so measured recall remains essential.
