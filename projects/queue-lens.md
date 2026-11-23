---
id: queue-lens
title: QueueLens
role: Graduate Researcher
start_date: '2025-02'
end_date: '2026-04'
highlights:
  - Built a trace replay harness for comparing scheduling policies under repeatable workloads.
  - Measured a 40 ms reduction in median latency in a synthetic burst workload.
public:
  title: QueueLens
  summary: A trace replay harness that compares scheduling policies for data pipelines under repeatable workloads.
  highlights:
    - Built a trace replay harness for controlled comparisons of pipeline scheduling policies.
  publication: queue-lens-paper
  image:
    file: queue-lens.png
    alt: Grouped bars comparing median latency before and after changing the scheduling policy on three synthetic workloads.
    caption: Median latency on three synthetic workloads.
---

## Evidence

Illustrative measurements for the template. Baseline and trace-guided median
latencies in milliseconds are 122 and 104 for Steady, 180 and 140 for Bursty,
and 148 and 128 for Mixed. Each pair uses the same replayed input.

## Application notes

For a research proposal, use this project to introduce the problem of comparing
schedulers under controlled workloads. A possible next experiment would hold
the arrival distribution constant and vary worker count.
