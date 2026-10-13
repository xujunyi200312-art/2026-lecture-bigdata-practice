# Week 04 observations

## Task 1
Bloom insertion only sets bits, and lookup checks the same positions without clearing them, so inserted items cannot become false negatives; predicted FP was 0.860%, measured 0.735% (20,000 absent queries; finite sampling and bitmap occupancy explain the difference).
For 19,953 true distinct items, arithmetic mean of 2^R gave 64,256, median 16,384, and median of group arithmetic means 70,400; the chosen median of eight corrected group geometric means gave 24,947 (1.25x), suppressing exponential outliers (1.259 is the asymptotic geometric-mean bias correction, not fitted to this stream).
Reservoir sampling uses j = rng.randrange(n) and replaces only when j < k: each arriving item enters with probability k/n, while older entries survive with the corresponding probability; only k entries are stored, and the 4,000-trial spread was 8.9%.

## Task 2
At 25,000,000 items, the exact set took 76.57s and 710.24 MiB traced peak on the i9-14900HX / 31.74 GiB Windows machine; waiting time became unpleasant before RAM ran out (the extra stress run is exact-only, not an OOM claim).
Over the four paired sizes (64x n), exact peak grew 47.74x, approximately O(n), versus 1.001x for FM, O(64) registers; FM ratios were 0.960x, 0.961x, 0.887x, 0.933x, so accuracy did not improve monotonically with size.
A factor of two is useful for rough daily traffic magnitude, but unsuitable for unique-user billing or a 5% change alert; fixed memory also did not mean faster execution here.

## Task 3
For p(k)=(1-exp(-kn/m))^k, differentiating log p gives exp(-kn/m)=1/2, hence k*=(m/n)ln(2)=6.931 and k=7; the ideal 10-bit/item floor is (1/2)^(10 ln(2))=0.8193% (integer k=7: 0.8194%).
Measured FP was 1,692/200,000=0.846%, down 91.1% from 9.511%, with zero false negatives; all persistent instance/bytearray/seed storage totals 80,000 bits, leaving 79,160 bitmap bits (predicted FP about 0.862%), so the result is close to the floor and below the 0.9% strong bar. Temporary hashing workspace and shared Python code are not retained filter state.
If n is unknown, monitor occupancy and add capacity through a scalable Bloom filter with an allocated error budget, or rotate filters for a stated time window; guessing too low saturates bits and raises FP, while guessing too high wastes memory (with a fixed bitmap, setting too many hashes can also hurt FP).
