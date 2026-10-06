"""Reproduce the requested experiment of moving the LSH step too high."""
import json
from pathlib import Path
from functools import partial

import bench
from task3_scale import YourFinder


def main():
    docs = bench.build()
    truth = bench.truth(docs)
    results = []
    for bands in (30, 10):
        hashes = 120
        rows = hashes // bands
        metrics = bench.run(partial(YourFinder, hashes=hashes, bands=bands),
                            f"b={bands},r={rows}", docs, truth)
        results.append(dict(hashes=hashes, bands=bands, rows=rows,
                            step=(1 / bands)**(1 / rows),
                            probability_at_threshold=1 - (1 - bench.THRESHOLD**rows)**bands,
                            true_pairs=len(truth), **metrics))
    out = Path(__file__).parent / "out"
    out.mkdir(exist_ok=True)
    (out / "parameters.json").write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
