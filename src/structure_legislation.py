"""
structure_legislation.py

Purpose:
Convert mock raw legislative records into structured civic bill data.

This script is a sanitized public demo. It does not use proprietary Pinion code,
private infrastructure, API keys, internal prompts, production schemas, or user data.
"""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = ROOT / "data" / "sample_bills_raw.csv"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_PATH = OUTPUT_DIR / "structured_bill_output.csv"


POLICY_KEYWORDS = {
    "Health": ["health", "community health", "public agencies"],
    "Economic development": ["small business", "permit", "digital submission"],
    "Transportation": ["transit", "transportation", "infrastructure"],
    "Housing": ["housing", "redevelopment", "underused properties", "mixed-use"],
}


def load_raw_bills() -> pd.DataFrame:
    """Load mock raw bill records."""
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"Could not find raw data file: {RAW_DATA_PATH}")

    df = pd.read_csv(RAW_DATA_PATH)

    required_columns = {
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

    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    return df


def assign_policy_area(description: str) -> str:
    """Assign a simple policy area using keyword matching."""
    text = description.lower()

    for policy_area, keywords in POLICY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return policy_area

    return "Needs review"


def create_plain_english_summary(description: str) -> str:
    """
    Create a simple plain-English summary.

    In a production civic-tech setting, this step could involve an AI model,
    but generated summaries should preserve source links and remain reviewable.
    """
    cleaned = description.strip()

    if cleaned.lower().startswith("a bill"):
        cleaned = cleaned[6:].strip()

    return cleaned[:1].upper() + cleaned[1:]


def structure_bills(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Transform raw bill records into structured civic data fields."""
    structured = pd.DataFrame()

    structured["bill_id"] = raw_df["bill_id"]
    structured["bill_number"] = raw_df["bill_number"]
    structured["clean_title"] = raw_df["title"].str.strip()
    structured["chamber"] = raw_df["chamber"]
    structured["sponsor"] = raw_df["sponsor"]
    structured["status"] = raw_df["status"]
    structured["last_action_date"] = raw_df["last_action_date"]
    structured["policy_area"] = raw_df["raw_description"].apply(assign_policy_area)
    structured["plain_english_summary"] = raw_df["raw_description"].apply(create_plain_english_summary)
    structured["source_url"] = raw_df["source_url"]

    # Records with generated summaries or uncertain categories should remain reviewable.
    structured["review_status"] = structured["policy_area"].apply(
        lambda area: "Needs human review" if area == "Needs review" else "Review recommended"
    )

    return structured


def main() -> None:
    """Run the mock legislative-data structuring workflow."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    raw_bills = load_raw_bills()
    structured_bills = structure_bills(raw_bills)

    structured_bills.to_csv(OUTPUT_PATH, index=False)

    print("Structured bill output created.")
    print(f"Input records: {len(raw_bills)}")
    print(f"Output path: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
