"""
evaluate_summaries.py

Purpose:
Evaluate Claude-generated bill summaries against simple expected checks.

This is not a full benchmark. It is a lightweight demonstration of how AI
outputs can be reviewed for traceability, policy-area fit, and missing content.
"""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
GENERATED_PATH = ROOT / "outputs" / "claude_summary_examples.csv"
EXPECTED_PATH = ROOT / "evaluation" / "expected_summary_checks.csv"
OUTPUT_DIR = ROOT / "outputs"
EVAL_OUTPUT_PATH = OUTPUT_DIR / "summary_evaluation_results.csv"


def normalize_text(value: str) -> str:
    """Normalize text for simple matching."""
    return str(value).lower().strip()


def main() -> None:
    """Compare generated summaries against expected checks."""
    generated = pd.read_csv(GENERATED_PATH)
    expected = pd.read_csv(EXPECTED_PATH)

    merged = expected.merge(generated, on="bill_id", how="left")

    results = []

    for _, row in merged.iterrows():
        summary = normalize_text(row.get("plain_english_summary", ""))
        policy_area = normalize_text(row.get("policy_area", ""))
        expected_policy_area = normalize_text(row.get("expected_policy_area", ""))
        must_mention = normalize_text(row.get("must_mention", ""))

        results.append(
            {
                "bill_id": row["bill_id"],
                "policy_area_match": expected_policy_area in policy_area,
                "must_mention_present": must_mention in summary,
                "human_review_required": row.get("human_review_required"),
                "notes": "Passes basic checks" if must_mention in summary else "Needs review for missing expected concept",
            }
        )

    result_df = pd.DataFrame(results)
    result_df.to_csv(EVAL_OUTPUT_PATH, index=False)

    print("Evaluation results")
    print(result_df.to_string(index=False))
    print(f"\nSaved evaluation output to: {EVAL_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
