#!/usr/bin/env python3
"""Turn RUM samples into grouped reproducible performance scenarios."""
import argparse
import json
from collections import defaultdict
from pathlib import Path


def build(samples, lcp_threshold=2500):
    groups = defaultdict(list)
    for sample in samples:
        key = (sample.get("route", "/"), sample.get("device", "desktop"), sample.get("network", "4g"))
        groups[key].append(sample)
    scenarios = []
    for key, rows in sorted(groups.items()):
        avg = {metric: sum(row.get(metric, 0) for row in rows) / len(rows) for metric in ("lcp", "inp", "cls")}
        long_tasks = sum(len(row.get("long_tasks", [])) for row in rows)
        third_party = sorted({url for row in rows for url in row.get("third_party", [])})
        scenarios.append({"route": key[0], "device": key[1], "network": key[2], "samples": len(rows),
                          "metrics": avg, "regression": avg["lcp"] > lcp_threshold,
                          "long_task_count": long_tasks, "third_party": third_party})
    return {"scenarios": scenarios, "regressions": sum(item["regression"] for item in scenarios)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("samples")
    parser.add_argument("--lcp-threshold", type=float, default=2500)
    args = parser.parse_args()
    report = build(json.loads(Path(args.samples).read_text()), args.lcp_threshold)
    print(json.dumps(report, indent=2))
    raise SystemExit(1 if report["regressions"] else 0)


if __name__ == "__main__":
    main()
