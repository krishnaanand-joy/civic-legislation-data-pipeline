"""
claude_bill_summarizer.py

Purpose:
Use Claude to create plain-English summaries and policy-area labels for mock
legislative records.

This is a sanitized public demo. It does not include proprietary Pinion code,
private infrastructure, API keys, internal prompts, production schemas, or user data.

Setup:
1. Install dependencies:
   pip install -r requirements.txt

2. Set your API key as an environment variable:
   export ANTHROPIC_API_KEY="your-key-here"

3. Optional: choose a Claude model:
   export CLAUDE_MODEL="claude-opus-4-8"

4. Run:
   python src/claude_bill_summarizer.py
"""

from __future__ import annotations

from pathlib import Path
import json
import os
from typing import Any

import anthropic
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = ROOT / "data" / "sample_bills_raw.csv"
PROMPT_PATH = ROOT / "prompts" / "bill_summarization_prompt.md"

OUTPUT_DIR = ROOT / "outputs"
OUTPUT_PATH = OUTPUT_DIR / "claude_summary_examples.csv"

MODEL = os.getenv("CLAUDE_MODEL", "claude-opus-4-8")


REQUIRED_COLUMNS = {
    "bill_id",
    "bill_number",
    "title",
    "chamber",
    "sponsor",
    "status",
    "last_action_date",
    "source_url",
    "raw_description",
}


def load_prompt() -> str:
    """Load the reusable bill-summarization prompt."""
    if not PROMPT_PATH.exists():
        raise FileNotFoundError(f"Could not find prompt file: {PROMPT_PATH}")

    return PROMPT_PATH.read_text(encoding="utf-8")


def load_bills() -> pd.DataFrame:
    """Load mock raw bill records."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Could not find input data: {DATA_PATH}")

    bills = pd.read_csv(DATA_PATH)

    missing_columns = REQUIRED_COLUMNS - set(bills.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    return bills


def build_user_message(row: pd.Series) -> str:
    """Build the bill-specific message sent to Claude."""
    return f"""
Bill number: {row["bill_number"]}
Title: {row["title"]}
Chamber: {row["chamber"]}
Sponsor: {row["sponsor"]}
Status: {row["status"]}
Last action date: {row["last_action_date"]}
Source URL: {row["source_url"]}

Raw description:
{row["raw_description"]}
""".strip()


def parse_json_response(response_text: str) -> dict[str, Any]:
    """
    Parse Claude's JSON response.

    If the model returns invalid JSON, the output is not silently accepted.
    Instead, the record is marked for human review so the failure mode is visible.
    """
    try:
        parsed = json.loads(response_text)
    except json.JSONDecodeError:
        return {
            "plain_english_summary": response_text,
            "policy_area": "Needs review",
            "confidence": "low",
            "human_review_required": True,
            "human_review_reason": "Claude response was not valid JSON.",
        }

    required_keys = {
        "plain_english_summary",
        "policy_area",
        "confidence",
        "human_review_required",
        "human_review_reason",
    }

    missing_keys = required_keys - set(parsed.keys())
    if missing_keys:
        parsed["human_review_required"] = True
        parsed["human_review_reason"] = (
            "Claude response was missing required fields: "
            + ", ".join(sorted(missing_keys))
        )

    return parsed


def summarize_bill(
    client: anthropic.Anthropic,
    system_prompt: str,
    row: pd.Series,
) -> dict[str, Any]:
    """Call Claude for one bill summary."""
    message = client.messages.create(
        model=MODEL,
        max_tokens=500,
        temperature=0,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": build_user_message(row),
            }
        ],
    )

    response_text = message.content[0].text
    return parse_json_response(response_text)


def build_output_row(row: pd.Series, model_output: dict[str, Any]) -> dict[str, Any]:
    """Combine source fields and Claude-generated fields into one output row."""
    return {
        "bill_id": row["bill_id"],
        "bill_number": row["bill_number"],
        "title": row["title"],
        "source_url": row["source_url"],
        "plain_english_summary": model_output.get("plain_english_summary"),
        "policy_area": model_output.get("policy_area"),
        "confidence": model_output.get("confidence"),
        "human_review_required": model_output.get("human_review_required"),
        "human_review_reason": model_output.get("human_review_reason"),
    }


def main() -> None:
    """Run Claude-powered summarization over the mock bill records."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    client = anthropic.Anthropic()
    system_prompt = load_prompt()
    bills = load_bills()

    output_rows = []

    for _, row in bills.iterrows():
        model_output = summarize_bill(client, system_prompt, row)
        output_rows.append(build_output_row(row, model_output))

    output_df = pd.DataFrame(output_rows)
    output_df.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved Claude summary examples to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
