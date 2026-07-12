# web-perf-replay

A dependency-free CLI that groups RUM samples into reproducible route, device, and network performance scenarios.

## Quick start

```bash
python replay.py samples.json --lcp-threshold 2500
```

Input is a JSON array of samples containing route context, `lcp`, `inp`, `cls`, optional `long_tasks`, and `third_party` URLs. The output groups matching execution contexts, averages Web Vitals, retains long-task and third-party evidence, and exits nonzero when a scenario exceeds the LCP budget.

## Test

```bash
python -m unittest discover -v
```

## License

MIT.
