# Project Direction and Related Tracks

## Current direction

This repository documents a live project that continues to be iterated, automated, and refined. The current public package is centered on the V40 baseline, the staged architecture, and the surrounding curation/evaluation logic that shaped the system.

## Near-term project direction

Near-term additions most aligned with this repository include:

- expanding the visual layer in `assets/`
- publishing the Hugging Face demo represented by `examples/hf_space_app.py`
- adding additional public-facing examples in `examples/`
- extending the methods depth in `docs/MODEL_AND_TRAINING.md`
- extending the visual evaluation story in `docs/EVALUATION_AND_RESULTS.md`

## Longer-horizon direction

Longer-horizon work extends beyond presenting the V40 baseline and moves toward more automated curation and feedback-aware workflows. At a high level, that direction includes:

- stronger automation around hard-negative review and dataset assembly
- tighter feedback loops between uncertainty signals and review queues
- progressively more automated handling of difficult or ambiguous cases
- broader operational hardening around the workflows documented in the companion repository [`AutoFACS CLI Automation`](https://github.com/TFJune2025/autofacs-cli-automation)

## Broader AutoFACS context

AutoFACS CV/ML is one track inside a larger effort. Related work includes:

- data-governance and storage-boundary hardening
- evaluation and audit tooling
- automation and CLI governance
- future inference and product-facing surfaces

## Relationship to AutoFACS CLI Automation

The separate **[AutoFACS CLI Automation](https://github.com/TFJune2025/autofacs-cli-automation)** repository documents the governed control-plane layer intended to automate, harden, and audit workflows around the broader AutoFACS effort, including workflows that support this CV/ML track.

That companion repository provides operational context, while this repository remains centered on the domain/model story.