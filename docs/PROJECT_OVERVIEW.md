# Project Overview

## What AutoFACS CV/ML is

AutoFACS CV/ML is the model-facing track of the broader AutoFACS effort. Its purpose is to build a governed, high-accuracy facial expression recognition system informed by FACS-style reasoning, staged decision-making, and careful curation rather than a one-shot “throw data at a model” workflow.

The project started from a practical question: could micro-expression and expression-adjacent facial signals be labeled reliably enough to support time-localized review of recorded interview or interaction footage? As development progressed, the project expanded beyond the original HR-inspired use case and became a broader facial-expression understanding effort with legal, technical, and data-governance requirements.

## Why the project exists

Several recurring problems drove the project forward:

- early open-source solutions were not accurate enough for serious use
- open-source datasets varied widely in quality, cropping consistency, and label cleanliness
- manual curation was initially necessary but did not scale
- reliable inference required not just a better classifier, but stronger input filtering, curation, and audit logic

That led to a more disciplined system design in which data quality, staged modeling, review routing, and evaluation became core engineering surfaces.

## How this repository presents the project

This repository presents the project at two levels:

- **top level:** facial expression recognition
- **deeper technical docs:** a hierarchical, FACS-informed CV/ML pipeline
- **overall status:** an active engineering snapshot, not a final product release

## Scope of the public repo

This repository is documentation-first. It is meant to communicate:

- the project’s technical seriousness
- the staged architecture and design logic
- what the stable V40 generation demonstrated
- what the project learned from curation and evaluation
- how the public-facing repo differs from the full private working environment

It is not intended to provide enough information to reconstruct the entire private system from scratch.

## Public demo

A public Hugging Face demo is available here:
https://huggingface.co/spaces/TFJune2025/autofacs-cv-ml

The Space is a public-facing inference layer for live image and short-video use. It is intended as a controlled demo environment and does not expose the full private development history or internal serving artifacts.
