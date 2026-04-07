# Engineering Lessons and Remaining Challenges

## Why this page exists

This page is included because engineering maturity is easier to judge when a project shows not only what worked, but also what the project had to learn.

## Major lessons

### 1. Data quality was a first-class problem

The project’s evolution repeatedly reinforced that model quality depended heavily on curation quality. Noisy labels, poor crops, and mixed-quality source datasets could easily limit downstream progress.

### 2. A flat classifier was not the whole answer

The project moved toward a staged architecture because gating, relevance, and review routing all mattered. In practice, better structure helped as much as simply pushing one model harder.

### 3. Hard negatives were operationally important

Some classes remained much harder than others. The project therefore benefited from explicit hard-negative review, confusion analysis, and routing logic instead of assuming every case should be forced into the same treatment.

### 4. Earlier rules were sometimes too brittle

One example from the project record is the evolution away from an overly strict neutrality heuristic. That kind of revision is worth acknowledging because it reflects real learning rather than retrospective polishing.

### 5. The public repo is intentionally narrower than the working system

The broader AutoFACS ecosystem includes private automation, storage-governance, and data-management surfaces that are intentionally not reproduced here. That is part of the publication boundary, not an accident.

### 6. Apple Silicon shaped the engineering style

The project’s Apple Silicon / MPS constraint was not only a limitation; it also shaped the engineering discipline behind the work. Developing locally on M-series hardware encouraged a more memory-conscious, efficiency-oriented workflow and made it practical to iterate on inference, curation, and evaluation loops without defaulting to cloud-first experimentation. That local-first posture helped shorten iteration cycles while keeping the project grounded in deployment-relevant constraints.

## Current public-release constraints

- no raw data release
- no checkpoint release
- no end-to-end rerun instructions against the private working environment
- selected terminology intentionally kept one level higher while IP work is still active

## Current project state

This repository represents a live project in progress: one that continues to be iterated, automated, and improved. The V40 baseline established a meaningful technical foundation, but several engineering pressures still shaped the next stages of work:

- hard confusions among the more difficult classes
- continued curation pressure from mixed-quality sources
- the gap between a strong model baseline and a polished end-user inference product
