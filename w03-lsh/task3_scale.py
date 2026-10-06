#!/usr/bin/env python3
"""Week 3 · Task 3 — Find the same pairs without comparing everything.

Textbook §3.4.

`BruteForce` compares every pair. On 3,000 documents that is 4.5 million
comparisons and it is completely correct. On 3 million documents it is 4.5
trillion and it is completely useless.

Beat it. Find the same near-duplicate pairs while making far fewer comparisons.

    python3 bench.py
    python3 bench.py --yours

The harness counts every call you make to `similarity()`. That is your score.
It also checks **recall** - which of the truly similar pairs you found. Skipping
comparisons is easy; skipping comparisons without losing the pairs is the task.
"""


import random

from task1_minhash import lsh_candidates


class BruteForce:
    """Correct, and quadratic."""

    def __init__(self, threshold):
        self.threshold = threshold

    def find(self, docs, similarity):
        """docs is [set_of_shingles, ...]. Return {(i, j), ...} with i < j."""
        out = set()
        for i in range(len(docs)):
            for j in range(i + 1, len(docs)):
                if similarity(docs[i], docs[j]) >= self.threshold:
                    out.add((i, j))
        return out


class YourFinder:
    """Your near-duplicate finder.

        __init__(threshold)
        find(docs, similarity) -> {(i, j), ...}

    `similarity(a, b)` is the only way to compare two documents, and every call
    is counted. Everything else - signatures, banding, bucketing - is free, in
    the sense that the harness does not charge you for it. That is deliberate:
    it is also roughly true at scale, where the comparison is the expensive
    part and the hashing is linear.

    Two knobs decide everything:

        the number of hashes in a signature
        how many bands you split it into

    §3.4.2 gives you the relationship between those and the probability that a
    pair at similarity s becomes a candidate. It is an S-curve, and where its
    step sits is something you choose. Choose it on purpose and be able to say
    why in observation.md - a threshold of 0.8 does not mean bands should be
    anything in particular until you have done the arithmetic.

    You may reuse your Task 1 code.
    """

    def __init__(self, threshold, hashes=120, bands=30):
        if hashes <= 0 or bands <= 0 or hashes % bands:
            raise ValueError("hash count must be positive and divisible by bands")
        self.threshold = threshold
        self.hashes = hashes
        self.bands = bands

    def find(self, docs, similarity):
        if self.threshold <= 0:
            return BruteForce(self.threshold).find(docs, similarity)
        # Invert the sparse matrix so each occupied row is hashed only once.
        postings = {}
        for i, doc in enumerate(docs):
            for shingle in doc:
                postings.setdefault(shingle, []).append(i)
        prime = 2**61 - 1
        rng = random.Random(246)
        coefficients = [(rng.randrange(1, prime), rng.randrange(prime))
                        for _ in range(self.hashes)]
        signatures = [[prime] * self.hashes for _ in docs]
        for shingle, columns in postings.items():
            values = [(a * shingle + b) % prime for a, b in coefficients]
            for column in columns:
                sig = signatures[column]
                for k, value in enumerate(values):
                    if value < sig[k]:
                        sig[k] = value
        # Empty documents have Jaccard 0 and cannot match a positive threshold.
        ids = [i for i, doc in enumerate(docs) if doc]
        candidates = lsh_candidates([signatures[i] for i in ids], self.bands)
        return {(ids[i], ids[j]) for i, j in candidates
                if similarity(docs[ids[i]], docs[ids[j]]) >= self.threshold}
