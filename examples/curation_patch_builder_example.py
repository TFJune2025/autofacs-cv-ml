"""Public-facing curation patch builder example.

This file distills the repository's patch-building ideas into a smaller example:
- shortlist low-confidence predictions
- merge curated sources
- prioritize fragile confusion corridors
- validate files before writing a patch CSV
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd

PUBLIC_LABELS = [
    "anger", "contempt", "disgust", "fear", "happiness",
    "neutral", "questioning", "sadness", "surprise",
    "neutral_speech", "speech_action",
]
CORRIDOR_LABELS = {"sadness", "neutral_speech", "speech_action"}


def build_shortlist(full_inference_csv: str | Path, out_csv: str | Path, threshold: float = 0.85) -> pd.DataFrame:
    df = pd.read_csv(full_inference_csv)
    if "confidence" not in df.columns:
        raise ValueError("Expected a confidence column in full inference CSV.")
    shortlist = df[df["confidence"] < threshold].copy()
    shortlist.to_csv(out_csv, index=False)
    return shortlist


def merge_patch_sources(out_csv: str | Path, *csv_paths: Iterable[str | Path]) -> pd.DataFrame:
    frames = []
    for csv_path in csv_paths:
        path = Path(csv_path)
        if path.exists():
            frames.append(pd.read_csv(path))
    if not frames:
        patch = pd.DataFrame(columns=["filepath", "label"])
        patch.to_csv(out_csv, index=False)
        return patch

    patch = pd.concat(frames, ignore_index=True)
    path_col = "filepath" if "filepath" in patch.columns else "image_path"
    label_col = "label" if "label" in patch.columns else "true_label"
    patch = patch.rename(columns={path_col: "filepath", label_col: "label"})
    patch = patch[patch["label"].isin(PUBLIC_LABELS)].copy()
    patch["priority_corridor"] = patch["label"].isin(CORRIDOR_LABELS)
    patch = patch.sort_values(["priority_corridor", "label"], ascending=[False, True])
    patch = patch.drop_duplicates(subset=["filepath"], keep="first")
    patch.to_csv(out_csv, index=False)
    return patch


def validate_patch(in_csv: str | Path, out_csv: str | Path) -> pd.DataFrame:
    df = pd.read_csv(in_csv)
    df["exists"] = df["filepath"].astype(str).map(lambda p: Path(p).exists())
    clean = df[df["exists"]].drop(columns=["exists"])
    clean.to_csv(out_csv, index=False)
    return clean


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build a public-style curation patch CSV.")
    parser.add_argument("full_inference_csv")
    parser.add_argument("--shortlist-out", default="shortlist_auto.csv")
    parser.add_argument("--patch-out", default="patch_public.csv")
    parser.add_argument("--validated-out", default="patch_public_validated.csv")
    parser.add_argument("--threshold", type=float, default=0.85)
    args = parser.parse_args()

    shortlist = build_shortlist(args.full_inference_csv, args.shortlist_out, threshold=args.threshold)
    merge_patch_sources(args.patch_out, args.shortlist_out)
    validate_patch(args.patch_out, args.validated_out)
    print(f"Shortlist rows: {len(shortlist)}")
