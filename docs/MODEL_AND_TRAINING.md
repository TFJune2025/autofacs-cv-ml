# Model and Training

## Modeling approach

This repository’s artifacts demonstrate the following modeling overview:

- a **hierarchical two-stage pipeline**
- transformer-family image classification in at least one deployed modeling surface
- reliability-aware evaluation rather than raw top-line optimization alone

The configuration examples in `examples/model_config.example.json` and `examples/preprocessor_config.example.json` show a **ViTForImageClassification** surface with **224×224** image inputs for a relevance-filter model example. In this repository, those files are used to illustrate the project’s model family and preprocessing posture at a level that is informative for readers and appropriate for public release.

## Method summary

At the level documented in this repository, the method story is:

1. curate and prepare heterogeneous facial samples
2. use a Stage 1 relevance model to screen inputs
3. use a downstream expression/state classifier over filtered samples
4. analyze errors, hard negatives, and routing behavior
5. iterate through versioned experiment generations

## Why the project moved this way

Earlier phases of the project benchmarked available open-source code and datasets against the real requirements of expression classification. Those baselines helped reveal the limits of the current off-the-shelf landscape, especially around data quality, consistency, and practical deployment usefulness.

The project then moved toward greater independence in both code and data treatment. That progression matters because it shows the work was not simple reuse of a pre-existing benchmark pipeline; it was an engineering response to observed quality ceilings and dataset problems.

## Environment constraints

The project should be described as developed under:

- **Apple Silicon / MPS** as the primary hardware/backend environment
- private data surfaces that are **not included** in the public release

## What this repo does not publish

This repo does not publish:

- full private training scripts
- full hyperparameter schedules
- checkpoint files
- internal experiment orchestration surfaces
- disclosure-sensitive detail not needed for public understanding

## Example configs

See:

- `examples/model_config.example.json`
- `examples/preprocessor_config.example.json`

These files are included to show the model family and input contract without publishing the full private training stack.
