# Week 04: measured memory limits

## Machine and method (2026-10-13)

- CPU: Intel(R) Core(TM) i9-14900HX; usable RAM: 31.74 GiB.
- OS: Windows-11-10.0.26200-SP0; Python: 3.12.14.
- Other applications: Chrome, Codex/ChatGPT, and Windows background services.
- Same generated stream for both methods: seed 246, key space 40% of n; 64 FM hashes.
- Memory is peak Python allocation measured by tracemalloc, including streaming input generation, not whole-process RSS or total system memory. Tracing especially slows the many Python integer operations in FM.
- Four paired sizes span 64x. A separate 25,000,000-item exact-only run tests the stopping point; no FM result is invented for that extra stress run.

## A3 / A5: measured results

| Stream n | True distinct | Exact seconds | Exact peak MiB | FM seconds | FM peak KiB | FM estimate / truth |
|---:|---:|---:|---:|---:|---:|---:|
| 25,000 | 9,189 | 0.072 | 0.932 | 3.955 | 11.278 | 0.9599x |
| 100,000 | 36,702 | 0.281 | 3.744 | 15.912 | 11.275 | 0.9613x |
| 400,000 | 146,970 | 1.150 | 11.054 | 64.209 | 11.284 | 0.8871x |
| 1,600,000 | 587,625 | 4.651 | 44.487 | 255.329 | 11.292 | 0.9329x |
| 25,000,000 | 9,179,304 | 76.571 | 710.242 | not run | not run | not measured |

## A2: stopping point

Stopped the exact-only stress experiment at n=25,000,000: 76.57 seconds and 710.24 MiB traced peak. The practical limit was interactive waiting time (a roughly one-minute-or-longer pass), not exhausted RAM. This is a usability stopping point, not a claim of an out-of-memory failure; the machine still has substantial RAM. Larger inputs were not measured.

## A4: memory growth

Across the four paired sizes, n grows 64x, exact peak grows 47.74x (empirical endpoint exponent 0.930), while FM peak grows only 1.001x (exponent 0.000). Exact storage is O(d), here approximately O(n) because distinct count is proportional to n; hash-table capacity jumps and string lengths affect finite-size constants. FM is O(h) fixed-width registers for h=64, hence O(1) in n in this experiment. Temporary hash buffers also depend on h, not n. The 32-bit hash range is finite, so this is not an unlimited-cardinality guarantee.

## Accuracy and cost

The paired accuracy ratios are 0.9599x, 0.9613x, 0.8871x, 0.9329x. They fluctuate rather than showing a consistent accuracy improvement with n; more data does not increase the fixed register budget. FM's bounded memory is bought with approximate answers and, in this pure-Python traced implementation, much longer runtime than the C-backed set.
A factor of two can support a rough order-of-magnitude traffic dashboard; it is inadequate for billing unique users or detecting a 5% traffic change. Increase the sketch precision or use an exact method when those distinctions matter.

## Reproduce

```text
python task1_sketches.py --verify
python task1_compare.py
python task2_limits.py --sizes 25000,100000,400000,1600000
python task2_limits.py --sizes 25000000 --exact-only
python bench.py --yours
python test_tasks.py
python ../check.py w04
```

`limits.json` appends runs; use a fresh output file for a fresh experiment.
