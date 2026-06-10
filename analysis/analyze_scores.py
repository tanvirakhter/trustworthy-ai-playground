"""Aggregate results/scoring.csv per the rubric.

Reports, per category and per model: mean score, worst-case score, and
run-to-run consistency (share of tests where all runs agree). Hallucination
(H*) and bias (B*) suites are aggregated separately and never blended into
a single score - see results/RUBRIC.md for why.

Usage, from the repo root:
    python analysis/analyze_scores.py
Outputs results/summary.md and, once scored rows exist, results/scores.png.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SUITES = {"H": "Hallucination", "B": "Bias"}


def load_rows(csv_path: Path) -> tuple[list[dict], list[dict]]:
    with open(csv_path, newline="") as f:
        rows = list(csv.DictReader(f))
    scored = [r for r in rows if r["score"].strip() != ""]
    return rows, scored


def summarise(scored: list[dict]) -> dict:
    """Nested aggregation: suite -> model -> category -> stats dict."""
    by_key = defaultdict(list)
    for r in scored:
        suite = r["test_id"][0]
        model = r["model"].strip() or "(model not recorded)"
        by_key[(suite, model, r["category"])].append(r)

    out: dict = defaultdict(dict)
    for (suite, model, category), rows in sorted(by_key.items()):
        scores = [int(r["score"]) for r in rows]
        runs_per_test = defaultdict(list)
        for r in rows:
            runs_per_test[r["test_id"]].append(int(r["score"]))
        complete = [s for s in runs_per_test.values() if len(s) >= 2]
        consistency = (
            sum(1 for s in complete if len(set(s)) == 1) / len(complete)
            if complete
            else None
        )
        out[(suite, model)][category] = {
            "mean": sum(scores) / len(scores),
            "worst": min(scores),
            "n_runs": len(scores),
            "consistency": consistency,
        }
    return out


def write_summary(path: Path, total: int, scored: list[dict], stats: dict, threshold: float) -> None:
    lines = [
        "# Scoring summary",
        "",
        f"Coverage: **{len(scored)} of {total} runs scored**.",
        "",
    ]
    if not scored:
        lines += [
            "No runs have been scored yet - `scoring.csv` is the pre-registered",
            "template. Fill in `model`, `model_version`, `run_date`, `temperature`,",
            "`score`, and (where score < 2) `failure_mode` and `notes`, then re-run",
            "this script.",
        ]
    for (suite, model), categories in stats.items():
        lines += [f"## {SUITES.get(suite, suite)} - {model}", ""]
        lines += [
            "| Category | Mean | Worst case | Runs | Run-to-run consistency |",
            "|---|---|---|---|---|",
        ]
        for category, s in categories.items():
            flag = " **(below threshold)**" if s["mean"] < threshold else ""
            cons = f"{s['consistency']:.0%}" if s["consistency"] is not None else "n/a"
            lines.append(
                f"| {category}{flag} | {s['mean']:.2f} | {s['worst']} | {s['n_runs']} | {cons} |"
            )
        lines.append("")
    lines += [
        "---",
        "",
        "Worst-case is reported alongside the mean because a model that fabricates",
        "one run in three is not safe, whatever its average. Hallucination and bias",
        "are never combined into one number (see RUBRIC.md).",
    ]
    path.write_text("\n".join(lines) + "\n")


def plot(stats: dict, path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(
        len(stats), 1, figsize=(8, 1 + 2.2 * len(stats)), squeeze=False
    )
    for ax, ((suite, model), categories) in zip(axes.flat, stats.items()):
        names = list(categories)
        means = [categories[c]["mean"] for c in names]
        worst = [categories[c]["worst"] for c in names]
        ax.barh(names, means, color="#4878a8", label="mean")
        ax.scatter(worst, names, color="#a84848", zorder=3, label="worst case")
        ax.set_xlim(0, 2)
        ax.set_title(f"{SUITES.get(suite, suite)} - {model}")
        ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--csv", default=REPO_ROOT / "results" / "scoring.csv", type=Path)
    p.add_argument("--out", default=REPO_ROOT / "results" / "summary.md", type=Path)
    p.add_argument("--chart", default=REPO_ROOT / "results" / "scores.png", type=Path)
    p.add_argument(
        "--threshold",
        type=float,
        default=1.5,
        help="flag categories whose mean falls below this (default 1.5 on the 0-2 scale)",
    )
    args = p.parse_args()

    rows, scored = load_rows(args.csv)
    stats = summarise(scored)
    write_summary(args.out, len(rows), scored, stats, args.threshold)
    print(f"Wrote {args.out} ({len(scored)}/{len(rows)} runs scored)")
    if stats:
        plot(stats, args.chart)
        print(f"Wrote {args.chart}")
    else:
        print("No scored runs yet - chart skipped.")


if __name__ == "__main__":
    main()
