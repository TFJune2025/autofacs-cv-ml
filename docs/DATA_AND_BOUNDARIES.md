# Data and Boundaries

## Data posture

AutoFACS CV/ML uses mixed facial-expression image/video-derived assets assembled through curation, earlier datasets, and ingestion/scraping workflows across the project’s evolution.

The important point for this repository is not the full dataset list. The important point is that **data quality became a major engineering problem in its own right**.

## What the project had to solve

The project encountered several practical data issues:

- inconsistent crops and framing
- low-resolution or unclear samples
- mixed-quality benchmark and open-source data
- label noise
- expression-adjacent states that were difficult to separate cleanly

That experience drove the project toward stronger preprocessing, filtering, and curation practices.

## What is intentionally not public in this repo

This repository does not include:

- raw face imagery
- identities
- sensitive annotations
- private filenames
- internal storage topology
- private mount paths or absolute local paths
- the private data lake itself
- full internal manifests
- non-public model artifacts

## What is described instead

This repo explains the **engineering pattern** rather than reproducing the private surfaces:

- heterogeneous data required curation
- dataset cleanliness mattered materially to downstream model quality
- human-guided review remained important even as automation increased
- the public package is a bounded technical explanation layer, not a data release

## Curation as an engineering surface

One of the strongest takeaways from the project is that curation was not a side task. It was a primary driver of quality. The project moved from heavy manual cleanup toward more automated crop/quality filtering while still preserving human review for difficult cases.

That curation story matters because it explains why the architecture, error analysis, and review loops look the way they do.
