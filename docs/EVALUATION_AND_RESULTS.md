# Evaluation and Results

![V40 benchmark snapshot](../assets/v40_results_overview.png)

## Publication posture

This page uses a conservative pre-filing posture:

- report selected V40 results only
- avoid releasing raw arrays, raw examples, or full private evaluation internals
- show enough quantitative evidence to establish technical credibility

## V40 result summary

![V40 Consolidated Results Snapshot](../assets/v40_results_overview.png)

### Stage 1 relevance filtering

Best reported Stage 1 row:
- epoch: **2**
- macro F1: **0.990**
- `relevant` F1: **0.985**
- `irrelevant` F1: **0.995**

![Stage 1 confusion matrix (V40)](img/confusion_matrix_stage1_v40.png)

Interpretation:
- Stage 1 performed at a very high level on its binary gating task.
- That supports the broader architectural choice to screen inputs before deeper expression/state classification.

### Stage 2 calibrated classification

Reported calibrated V40 snapshot:
- epoch marker: **5.985**
- macro F1: **0.902**

![Stage 2 confusion matrix (V40, uncalibrated)](img/confusion_matrix_stage2_uncalibrated_v40.png)

![Stage 2 confusion matrix (V40, calibrated)](img/confusion_matrix_stage2_calibrated_v40.png)

Selected calibrated examples:
- `neutral`: **0.978**
- `surprise`: **0.976**
- `happiness`: **0.973**
- `neutral_speech`: **0.951**

Classes that remained materially harder:
- `contempt`: **0.793**
- `disgust`: **0.792**
- `sadness`: **0.853**
- `speech_action`: **0.882**

![V40 benchmark snapshot](../assets/v40_results_overview.png)

## What these numbers mean

The results support several careful public claims:

- the project had a real staged CV/ML core, not just a concept
- the relevance filter was strong enough to justify the two-stage architecture
- downstream performance was strong for several classes while still leaving a meaningful hard tail of difficult cases
- curation and review-routing remained justified because not all classes were equally easy

![Emotion distribution summary](img/emotion_distribution_summary.png)

![Temporal emotion timeline](img/emotion_timeline.png)

## Scope of the published results

This page focuses on the V40 result surfaces that best explain the system: the strength of Stage 1 gating, the calibrated Stage 2 snapshot, and the class-specific tail that continued to drive curation and review work.

Accordingly, the repository centers the reader-facing summary rather than the full private evaluation package. The published view emphasizes the most informative aggregate result surfaces while leaving out raw arrays, raw confusion-case image references, private audit artifacts, and model weights.

## How to read these results

The most important takeaway is not a single headline number. The V40 snapshot is more useful when read as a system result:

- Stage 1 was strong enough to justify the staged architecture.
- Stage 2 showed solid calibrated downstream performance across much of the target state space.
- The remaining hard tail still mattered, which is why curation, hard-negative review, and routing continued to be part of the engineering story.

## Evidence basis for this page

The figures and summaries on this page correspond to the V40 result surfaces represented in this repository’s documentation and examples, especially `docs/MODEL_AND_TRAINING.md`, `examples/plot_v40_results.py`, and the summary asset `assets/v40_results_overview.png`.
