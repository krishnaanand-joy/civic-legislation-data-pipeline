"""
claude_bill_summarizer.py

Purpose:
Use Claude to create plain-English summaries and policy-area labels for mock
legislative records.

This is a sanitized public demo. It does not include proprietary Pinion code,
private infrastructure, API keys, internal prompts, production schemas, or user data.

Setup:
1. Install dependencies: pip install -r requirements.txt
2. Set your API key as an environment variable:
   export ANTHROPIC_API_KEY="your-key-here"
3. Run:
   python src/claude_bill_summarizer.py
"""

from __future__ import annotations

from pathlib import Path
import json
import os

import anthropic
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sample_bills_raw.csv"
PROMPT_PATH = ROOT / "prompts" / "bill_summarization_prompt.md"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_PATH = OUTPUT_DIR / "claude_summary_examples.csv"

MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5")


def load_prompt() -> str:
    """Load the reusable summarization prompt."""
    return PROMPT_PATH.read_text(encoding="utf-8")


def load_bills() -> pd.DataFrame:
    """Load mock bill records."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing input data: {DATA_PATH}")

    return pd.read_csv(DATA_PATH)


def build_user_message(row: pd.Series) -> str:
    """Build the bill-specific user message sent to Claude."""
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


def parse_json_response(text: str) -> dict:
    """
    Parse Claude's JSON response.

    Keeping this separate makes failure modes visible. If Claude returns invalid
    JSON, the record is marked for human review instead of silently failing.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "plain_english_summary": text,
            "policy_area": "Needs review",
            "confidence": "low",
            "human_review_required": True,
            "human_review_reason": "Model response was not valid JSON.",
        }


def summarize_bill(client: anthropic.Anthropic, system_prompt: str, row: pd.Series) -> dict:
    """Call Claude for one bill summary."""
    message = client.messages.create(
        model=MODEL,
        max_tokens=500,
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


def main() -> None:
    """Run Claude-powered summarization over the mock bill records."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    client = anthropic.Anthropic()
    prompt = load_prompt()
    bills = load_bills()

    results = []

    for _, row in bills.iterrows():
        model_output = summarize_bill(client, prompt, row)

        results.append(
            {
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
        )

    output_df = pd.DataFrame(results)
    output_df.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved Claude summary examples to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
