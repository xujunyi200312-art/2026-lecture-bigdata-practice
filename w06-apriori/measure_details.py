"""Reproduce supplemental correctness, rule and memory measurements."""
import ctypes
import gc
import json
import platform
import time
import tracemalloc
from pathlib import Path
import bench
from task1_apriori import frequent_singletons, association_rules
from task3_pcy import PlainApriori, YourAlgorithm

OUT = Path(__file__).parent / 'out'

def main():
    baskets = bench.build()
    reference = PlainApriori(50).run(baskets)
    measurements = []
    for bucket_count in (None, 1_000_003, 10_007):
        gc.collect()
        algo = PlainApriori(50) if bucket_count is None else YourAlgorithm(50, bucket_count)
        tracemalloc.start()
        start = time.perf_counter()
        pairs = algo.run(baskets)
        elapsed = time.perf_counter() - start
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        assert pairs == reference, 'Pair supports must also match, not just keys'
        row = dict(buckets=bucket_count, peak_counters=algo.peak_counters,
                   peak_bytes=peak, seconds=elapsed, exact_counts_match=True)
        measurements.append(row)
        print(row, flush=True)
        del pairs
    singles = frequent_singletons(baskets, 50)
    rules = association_rules(baskets, 50, 0)
    best = rules[0]
    reverse = next(rule for rule in rules if rule[0] == best[1] and rule[1] == best[0])
    data = dict(measurements=measurements, frequent_singletons=len(singles),
                candidate_upper_bound=len(singles)*(len(singles)-1)//2,
                best_rule=best, reverse_rule=reverse)
    (OUT/'details.json').write_text(json.dumps(data, indent=2), encoding='utf-8')
    print(data, flush=True)
    if platform.system() == 'Windows':
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [('length', ctypes.c_ulong), ('load', ctypes.c_ulong)] + [
                (name, ctypes.c_ulonglong) for name in
                ('total_phys', 'avail_phys', 'total_page', 'avail_page', 'total_virtual', 'avail_virtual', 'extended')]
        memory = MEMORYSTATUSEX()
        memory.length = ctypes.sizeof(memory)
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory)):
            raise ctypes.WinError()
        path = OUT/'explosion.json'
        explosion = json.loads(path.read_text())
        explosion['machine'].update(cpu='Intel(R) Core(TM) i9-14900HX',
            ram_bytes=memory.total_phys, available_ram_bytes_at_supplemental_measurement=memory.avail_phys,
            other_running_apps=['ChatGPT/Codex', 'Chrome', 'Weixin', 'Douyin', 'HipsDaemon'],
            measurement_scope='tracemalloc allocations during run; excludes prebuilt baskets and interpreter')
        path.write_text(json.dumps(explosion, indent=2), encoding='utf-8')

if __name__ == '__main__':
    main()
