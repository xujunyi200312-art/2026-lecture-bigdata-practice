#!/usr/bin/env python3
"""Week 3 · Task 2 — Find the crossover on your own machine.

Textbook §3.4.

Everybody knows brute force is quadratic and LSH is not. That is not the
interesting question. The interesting question is **where, on the machine in
front of you, does it start to matter** - and that answer is yours alone. It
depends on your CPU, your memory, and how big your shingle sets are.

This script gives you the timing loop. The two methods are yours: import them
from Task 1 and Task 3.

    python3 task2_crossover.py --sizes 500,1000,2000,4000
    python3 task2_crossover.py --sizes 8000,16000          # keep going

Write down where it hurts. That is the deliverable.
"""
import argparse, json, os, platform, time, tracemalloc, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")


def machine():
    info = {
        "platform": platform.platform(),
        "processor": platform.processor() or platform.machine(),
        "python": platform.python_version(),
    }
    if os.name == "nt":
        import ctypes
        import winreg
        class MemoryStatus(ctypes.Structure):
            _fields_ = [("length", ctypes.c_ulong), ("load", ctypes.c_ulong)] + [
                (name, ctypes.c_ulonglong) for name in
                ("total_physical", "available_physical", "total_pagefile",
                 "available_pagefile", "total_virtual", "available_virtual", "extended")]
        status = MemoryStatus()
        status.length = ctypes.sizeof(status)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            info["ram_bytes"] = status.total_physical
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            r"HARDWARE\DESCRIPTION\System\CentralProcessor\0") as key:
            info["processor"] = winreg.QueryValueEx(key, "ProcessorNameString")[0].strip()
    return info


def build_documents(n):
    """Generate exactly n documents, with the harness's shingle distribution.

    Unlike bench.build()[:n], this continues growing beyond 2,120 documents.
    Keep approximately the same 120/2120 planted-clone fraction at every size.
    """
    import bench
    rng = random.Random(bench.SEED)
    planted = round(n * bench.PLANTED / (bench.N_DOCS + bench.PLANTED))
    base = n - planted
    docs = [set(rng.sample(range(bench.VOCAB), bench.SHINGLES)) for _ in range(base)]
    for _ in range(planted):
        clone = set(docs[rng.randrange(base)])
        for _ in range(rng.randint(4, 14)):
            clone.discard(rng.choice(sorted(clone)))
            clone.add(rng.randrange(bench.VOCAB))
        docs.append(clone)
    rng.shuffle(docs)
    return docs


def timed(fn, *args):
    """Wall time and peak memory of one call."""
    tracemalloc.start()
    t0 = time.perf_counter()
    result = fn(*args)
    elapsed = time.perf_counter() - t0
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, elapsed, peak


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--sizes", default="250,500,1000,2000",
                   help="comma-separated document counts to try")
    p.add_argument("--threshold", type=float, default=0.6)
    p.add_argument("--background", default="not recorded",
                   help="applications running during the measurement")
    a = p.parse_args()
    os.makedirs(OUT, exist_ok=True)

    import bench
    from task3_scale import BruteForce
    try:
        from task3_scale import YourFinder
    except Exception:
        YourFinder = None

    path = os.path.join(OUT, "crossover.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            prior = json.load(f)
    else:
        prior = {"runs": []}
    prior["machine"] = machine()
    prior["machine"]["background"] = a.background
    prior["memory_method"] = "tracemalloc peak during find; excludes prebuilt input and total process RAM"
    for n in [int(x) for x in a.sizes.split(",")]:
        if n <= 0:
            raise ValueError("sizes must be positive")
        docs = build_documents(n)
        sim = bench.Counter()
        _, t_brute, m_brute = timed(BruteForce(a.threshold).find, docs, sim)
        c_brute = sim.calls

        row = {"n": len(docs), "threshold": a.threshold, "brute_s": t_brute, "brute_calls": c_brute,
               "brute_peak_bytes": m_brute}

        if YourFinder is not None:
            sim2 = bench.Counter()
            try:
                _, t_lsh, m_lsh = timed(YourFinder(a.threshold).find, docs, sim2)
                row.update({"lsh_s": t_lsh, "lsh_calls": sim2.calls,
                            "lsh_peak_bytes": m_lsh})
            except NotImplementedError:
                pass

        assert c_brute == n * (n - 1) // 2
        prior["runs"].append(row)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(prior, f, indent=2)
        line = f"  n={n:>6}  brute {t_brute:>8.2f}s  {c_brute:>12,} cmp"
        if "lsh_s" in row:
            line += f"   |  lsh {row['lsh_s']:>7.2f}s  {row['lsh_calls']:>9,} cmp"
        print(line)

    print(f"\n  -> out/crossover.json  ({len(prior['runs'])} measurement(s))")
    print("  Keep raising --sizes until something becomes unpleasant. Record where.")


if __name__ == "__main__":
    main()
