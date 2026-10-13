#!/usr/bin/env python3
"""Week 4 · Task 3 — Same memory, fewer mistakes.

Textbook §4.4 (Bloom filters), §4.5 (counting distinct).

`NaiveFilter` is a membership filter in a fixed number of bits. It works. It
also makes far more mistakes than it has to with the memory it was given, and
it does so for a reason you can find by reading §4.4.2 and doing one derivative.

You get **exactly the same number of bits**. Make fewer mistakes.

    python3 bench.py
    python3 bench.py --yours

The rule that makes this interesting: a false negative is not allowed. Ever.
The whole point of this structure is that "no" means no. A filter that gets a
better score by occasionally forgetting something it was given has not improved
anything, it has broken the contract.
"""
import hashlib
import struct
import sys


class NaiveFilter:
    """One hash function, and the bits it was given."""

    def __init__(self, n_bits, seed=246):
        self.n_bits = n_bits
        self.seed = seed
        self.bits = bytearray(n_bits)

    def _index(self, item):
        d = hashlib.blake2b(str(item).encode(), digest_size=8,
                            key=str(self.seed).encode()).digest()
        return int.from_bytes(d, "big") % self.n_bits

    def add(self, item):
        self.bits[self._index(item)] = 1

    def __contains__(self, item):
        return bool(self.bits[self._index(item)])

    def memory_bits(self):
        return self.n_bits


class YourFilter:
    """Your filter.

        __init__(n_bits, seed=246)
        add(item)
        item in filter  ->  bool
        memory_bits()   ->  how many bits you are using

    `memory_bits()` must not exceed the `n_bits` you were given. The harness
    checks. Counting only some of your memory is not an optimisation.

    §4.4.2 gives the false-positive rate of a filter with m bits, k hashes and
    n items inserted. There is a k that minimises it, and it depends on m/n.
    The harness tells you n before you start, so you have no excuse for guessing.

    Then there is a second question, which is worth more: the harness inserts
    a **known** number of items, but a real stream does not tell you n in
    advance. What would you do then? You do not have to implement it - but
    observation.md asks.
    """

    __slots__ = ('bits',)

    def __init__(self, n_bits, seed=246):
        # Count Python instance and bytearray overhead, plus an 8-byte seed.
        size = n_bits // 8 - sys.getsizeof(self) - sys.getsizeof(bytearray(1)) + 1
        if size <= 8:
            raise ValueError("budget too small for filter metadata")
        self.bits = bytearray(size)
        self.bits[:8] = (seed % (1 << 64)).to_bytes(8, 'little')

    def _indices(self, item):
        m = (len(self.bits) - 8) * 8
        digest = hashlib.shake_256(bytes(self.bits[:8]) + str(item).encode()).digest(56)
        for h in struct.unpack('<7Q', digest):
            yield h % m

    def add(self, item):
        for i in self._indices(item):
            self.bits[8 + i // 8] |= 1 << (i % 8)

    def __contains__(self, item):
        return all(self.bits[8 + i // 8] & (1 << (i % 8))
                   for i in self._indices(item))

    def memory_bits(self):
        # All persistent per-filter storage, not just the bitmap payload.
        return 8 * (sys.getsizeof(self) + sys.getsizeof(self.bits))
