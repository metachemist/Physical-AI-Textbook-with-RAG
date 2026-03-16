# Benchmark Results

> Populate this file after running `backend/tests/golden/run_benchmark.py`.

## Run Summary

| Date | Citation Presence | Recall@10 | Avg Latency | Pass? |
|------|------------------|-----------|-------------|-------|
| (pending) | — | — | — | — |

## Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Citation presence | ≥27/30 (90%) | SC-006 |
| Recall@10 | ≥0.80 (80%) | SC-007 |
| p95 chat latency | ≤3000ms | SC-005 |

## Instructions

```bash
cd backend
BASE_URL=https://<render-url>.onrender.com \
QDRANT_URL=$QDRANT_URL \
QDRANT_API_KEY=$QDRANT_API_KEY \
python tests/golden/run_benchmark.py --output-dir tests/golden/results/
```

Then paste the printed summary table here and attach the CSV path.
