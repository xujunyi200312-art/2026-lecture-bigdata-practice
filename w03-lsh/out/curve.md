# Task 2: measured crossover

Measured locally on 2026-10-06. These are observed wall times, not extrapolated timings.

## Machine and measurement method

- CPU: Intel(R) Core(TM) i9-14900HX; usable physical RAM reported by Windows: 31.73 GiB (34,070,192,128 bytes).
- OS: Windows-11-10.0.26200-SP0; Python 3.12.14.
- Background: Codex/ChatGPT, Douyin, Explorer, ACE-Tray and audio services were running; normal background load, not an idle benchmark.
- Each method runs once per size with tracemalloc enabled. Timings include memory-tracing overhead; this is not an idle-machine, repeated-median benchmark.
- Peak memory means Python allocations traced during find(), excluding the already-generated input, interpreter, and other processes. It is not whole-process peak RAM.
- Threshold 0.6; 120 hashes, 30 bands, 4 rows per band; seed 246; 60 initial shingles from vocabulary 5,000; about 120/2120 documents are planted clones.
- Fixed the starter script: bench.build()[:n] silently caps data at 2,120 documents. The replacement generator creates exactly n documents and checks that brute-force calls equal n(n-1)/2. bench.py is unchanged.

## Results (A1, A3, A5)

| Documents | Brute seconds | LSH seconds | Brute comparisons | LSH comparisons | Brute peak MiB | LSH peak MiB |
|---:|---:|---:|---:|---:|---:|---:|
| 125 | 0.0480 | 2.3638 | 7,750 | 8 | 0.0075 | 0.9937 |
| 250 | 0.1934 | 3.0851 | 31,125 | 15 | 0.0075 | 1.4313 |
| 500 | 0.8073 | 3.4354 | 124,750 | 29 | 0.0099 | 2.1164 |
| 1,000 | 3.3207 | 3.8244 | 499,500 | 58 | 0.0117 | 3.2443 |
| 2,000 | 14.0241 | 4.4085 | 1,999,000 | 116 | 0.0207 | 5.2299 |
| 4,000 | 53.7918 | 6.3279 | 7,998,000 | 241 | 0.0278 | 8.9168 |
| 8,000 | 243.7259 | 9.2602 | 31,996,000 | 474 | 0.0650 | 16.0590 |

7 measured sizes span 64x, exceeding the five-size and 16x requirements.

## Quadratic check (A4)

| Doubling | Measured brute-time ratio | Expected approximately |
|---|---:|---:|
| 125 to 250 | 4.030x | 4x |
| 250 to 500 | 4.175x | 4x |
| 500 to 1,000 | 4.113x | 4x |
| 1,000 to 2,000 | 4.223x | 4x |
| 2,000 to 4,000 | 3.836x | 4x |
| 4,000 to 8,000 | 4.531x | 4x |

The measured doubling ratios are near four, supporting quadratic growth on this machine. Background scheduling, allocation tracing, and cache effects prevent exact 4x ratios; the exact comparison counts independently follow n(n-1)/2.

## Crossover and cost (A7-A8)

The observed crossover is bracketed by n=1,000 (brute 3.3207s, LSH 3.8244s) and n=2,000 (brute 14.0241s, LSH 4.4085s). This is a measured interval, not an exact universal crossover.

LSH loses at small n because it builds a sparse row-to-document index, computes 120 hash values per distinct shingle, updates 120 signature entries per document shingle, then creates 30 band keys per document and deduplicates candidates. Brute force has little setup, so a few cheap set comparisons cost less. Hashing remains real work even though the Task 3 score does not count it.

## Where waiting became unpleasant (A2, A5)

The first measured size exceeding one minute was n=8,000: brute force took 243.73s. Time became the practical limit; no out-of-memory failure was observed. Stopping here satisfies the minute-of-waiting criterion without claiming a memory limit was reached.

At the largest n=8,000, brute-force traced peak was 68,200 bytes (0.0650 MiB), versus LSH 16,839,060 bytes (16.0590 MiB). LSH stores signatures and postings; brute force streams through pairs. Neither number includes input storage.

Reproduce: `python task2_crossover.py --sizes 125,250,500,1000,2000,4000,8000 --background "describe current applications"`. The script appends real measurements to crossover.json.
