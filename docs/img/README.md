# Docs Images

This folder is for images referenced directly inside the documentation pages.

Based on the current manifest, the strongest candidate visuals are the ones that communicate system maturity **without** exposing raw data or private operational detail.

## Recommended image shortlist

### Highest-priority figures

1. **confusion_matrix_Stage1_V40.png**
   - useful for showing that Stage 1 is a real classifier, not a hand-wavy prefilter

2. **confusion_matrix_Stage2_V40.png**
   - useful for showing the uncalibrated downstream classification surface

3. **confusion_matrix_Stage2_Calibrated_V40.png**
   - strongest candidate for the docs because it reflects the calibrated V40 story described in this repo

4. **summary_emotion_pie_chart.png**
   - potentially useful for a lightweight demo or inference-output example if it does not reveal private source material

5. **emotion_timeline.png**
   - a strong candidate for future demo documentation because it aligns with the project's time-localized inference story

## Optional figures after filing

If you later want a more historical appendix, the manifest also suggests earlier lineage visuals such as:

- reliability diagrams across earlier V-series generations
- distribution plots across earlier V-series generations
- pre-V40 confusion matrices showing project evolution

Those are better suited for a post-filing appendix than the first public release.

## What not to place here

Do not include:

- raw face examples
- curated training images
- internal review spreadsheets exported as screenshots
- anything that makes the private working environment reconstructable
