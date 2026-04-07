"""Plot approved V40 summary results from per-class metric CSVs.

This script is meant for public-safe visual regeneration from aggregate metrics,
not from raw private evaluation arrays.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def normalize_metric_frame(df: pd.DataFrame) -> pd.DataFrame:
    columns = {c.lower(): c for c in df.columns}
    label_col = columns.get("label") or columns.get("class") or columns.get("class_name")
    f1_col = columns.get("f1") or columns.get("f1_score") or columns.get("f1-score")
    precision_col = columns.get("precision")
    recall_col = columns.get("recall")
    if not label_col or not f1_col:
        raise ValueError("CSV must contain a label/class column and an F1 column.")
    out = pd.DataFrame({
        "label": df[label_col],
        "f1": df[f1_col],
    })
    if precision_col:
        out["precision"] = df[precision_col]
    if recall_col:
        out["recall"] = df[recall_col]
    return out


def plot_f1(df: pd.DataFrame, title: str, output_path: str | Path) -> None:
    ordered = df.sort_values("f1", ascending=True)
    plt.figure(figsize=(10, 6))
    plt.barh(ordered["label"], ordered["f1"])
    plt.xlabel("F1 score")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot V40 per-class results from aggregate CSVs.")
    parser.add_argument("metrics_csv", help="Path to a per_class_metrics CSV file.")
    parser.add_argument("--title", default="V40 per-class F1")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.metrics_csv)
    normalized = normalize_metric_frame(df)
    plot_f1(normalized, args.title, args.output)
    print(f"Saved plot to {args.output}")


if __name__ == "__main__":
    main()
