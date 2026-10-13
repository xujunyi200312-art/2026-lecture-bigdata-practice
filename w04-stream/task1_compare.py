"""Compare FM combining rules on the same registers as the verification data."""
import random
import statistics

from task1_sketches import fm_maxima


def main():
    rng = random.Random(246)
    data = [f'k{rng.randrange(20000)}' for _ in range(120000)]
    maxima = fm_maxima(iter(data))
    truth = len(set(data))  # Reference only; the sketch does not retain input.
    estimates = {
        'arithmetic mean of 2^R': statistics.mean(2**r for r in maxima),
        'median of 2^R': statistics.median(2**r for r in maxima),
        'median of group arithmetic means': statistics.median(
            statistics.mean(2**r for r in maxima[i:i + 8])
            for i in range(0, 64, 8)),
        'chosen: median of corrected group geometric means': statistics.median(
            2**statistics.mean(maxima[i:i + 8])
            for i in range(0, 64, 8)) / 1.259,
    }
    print(f'True distinct count: {truth}; 64 hashes, seed 246, groups of 8')
    for name, estimate in estimates.items():
        print(f'{name}: {estimate:.2f} ({estimate / truth:.4f}x)')


if __name__ == '__main__':
    main()
