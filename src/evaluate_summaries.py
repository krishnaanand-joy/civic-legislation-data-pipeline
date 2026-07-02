"""
evaluate_summaries.py

Purpose:
Evaluate Claude-generated bill summaries against simple expected checks.

This is not a full benchmark. It is a lightweight demonstration of how AI
outputs can be reviewed for policy-area fit, source-grounding, missing concepts,
and human-review flags.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

GENERATED_PATH = ROOT / "outputs" / "claude_summary_examples.csv"
EXPECTED_PATH = ROOT / "evaluation" / "expected_summary_checks.csv"

OUTPUT_DIR = ROOT / "outputs"
EVAL_OUTPUT_PATH = OUTPUT_DIR / "summary_evaluation_results.csv"


REQUIRED_GENERATED_COLUMNS = {
    "bill_id",
    "plain_english_summary",
    "policy_area",
    "confidence",
    "human_review_required",
    "human_review_reason",
}

REQUIRED_EXPECTED_COLUMNS = {
    "bill_id",
    "expected_policy_area",
    "must_mention",
    "human_review_expected",
}


def normalize_text(value: object) -> str:
    """Normalize text for simple comparison."""
    return str(value).lower().strip()


def load_csv(path: Path, required_columns: set[str]) -> pd.DataFrame:
    """Load a CSV and validate that required columns are present."""
    if not path.exists():
        raise FileNotFoundError(f"Could not find required file: {path}")

    df = pd.read_csv(path)

    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"{path.name} is missing required columns: {sorted(missing_columns)}"
        )

    return df


def evaluate_row(row: pd.Series) -> dict[str, object]:
    """Evaluate one generated summary against expected checks."""
    summary = normalize_text(row.get("plain_english_summary", ""))
    policy_area = normalize_text(row.get("policy_area", ""))
    expected_policy_area = normalize_text(row.get("expected_policy_area", ""))
    must_mention = normalize_text(row.get("must_mention", ""))

    policy_area_match = expected_policy_area == policy_area
    must_mention_present = must_mention in summary

    human_review_required = bool(row.get("human_review_required"))
    human_review_expected = bool(row.get("human_review_expected"))

    human_review_match = human_review_required == human_review_expected

    passes_basic_checks = (
        policy_area_match and must_mention_present and human_review_match
    )

    if passes_basic_checks:
        notes = "Passes basic evaluation checks."
    else:
        failed_checks = []

        if not policy_area_match:
            failed_checks.append("policy area mismatch")

        if not must_mention_present:
            failed_checks.append("missing expected concept")

        if not human_review_match:
            failed_checks.append("human-review flag mismatch")

        notes = "Needs review: " + ", ".join(failed_checks)

    return {
        "bill_id": row["bill_id"],
        "expected_policy_area": row["expected_policy_area"],
        "generated_policy_area": row.get("policy_area"),
        "policy_area_match": policy_area_match,
        "must_mention": row["must_mention"],
        "must_mention_present": must_mention_present,
        "human_review_expected": row["human_review_expected"],
        "human_review_required": row.get("human_review_required"),
        "human_review_match": human_review_match,
        "passes_basic_checks": passes_basic_checks,
        "notes": notes,
    }


def main() -> None:
    """Evaluate Claude-generated summaries and save the results."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    generated = load_csv(GENERATED_PATH, REQUIRED_GENERATED_COLUMNS)
    expected = load_csv(EXPECTED_PATH, REQUIRED_EXPECTED_COLUMNS)

    merged = expected.merge(generated, on="bill_id", how="left")

    if merged["plain_english_summary"].isna().any():
        missing_ids = merged.loc[
            merged["plain_english_summary"].isna(), "bill_id"
        ].tolist()
        raise ValueError(f"Missing generated summaries for bill IDs: {missing_ids}")

    results = [evaluate_row(row) for _, row in merged.iterrows()]

    result_df = pd.DataFrame(results)
    result_df.to_csv(EVAL_OUTPUT_PATH, index=False)

    print("Summary evaluation results")
    print(result_df.to_string(index=False))
    print(f"\nSaved evaluation output to: {EVAL_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
