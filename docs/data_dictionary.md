# Data Dictionary

This file explains the mock data fields used in the civic legislation data pipeline.

The data in this repository is fictional and created only for demonstration. It does not include proprietary Pinion data, production database fields, user data, API keys, or private platform information.

## Raw bill data

File: [`data/sample_bills_raw.csv`](../data/sample_bills_raw.csv)

This file represents the kind of messy or semi-structured legislative data that might come from a public source.

| Field | Description |
| --- | --- |
| `bill_id` | Fictional internal identifier for the mock record |
| `bill_number` | Mock bill number, such as HB 101 or SB 204 |
| `title` | Bill title as it appears in the raw record |
| `chamber` | Legislative chamber, such as House or Senate |
| `sponsor` | Mock primary sponsor |
| `status` | Current legislative status |
| `last_action_date` | Date of most recent legislative action |
| `source_url` | Mock source URL pointing back to the public record |
| `raw_description` | Unstructured or semi-structured description of the bill |

## Structured bill data

File: [`data/sample_bills_structured.csv`](../data/sample_bills_structured.csv)

This file represents the cleaner civic-data output that could support search, filtering, summaries, and issue tagging.

| Field | Description |
| --- | --- |
| `bill_id` | Fictional internal identifier carried over from the raw record |
| `bill_number` | Mock official bill number |
| `clean_title` | Cleaned and standardized bill title |
| `chamber` | Legislative chamber |
| `sponsor` | Mock primary sponsor |
| `status` | Current legislative status |
| `last_action_date` | Date of most recent legislative action |
| `policy_area` | High-level issue category assigned from the bill description |
| `plain_english_summary` | Short plain-English explanation of the bill |
| `source_url` | Mock source URL for traceability |
| `review_status` | Indicates whether the record should receive human review |

## Review status

The `review_status` field is included because civic information should be reviewable, especially when summaries or categories are generated automatically.

Possible values in this demo include:

| Value | Meaning |
| --- | --- |
| `Reviewed` | Mock record has been treated as reviewed for demo purposes |
| `Review recommended` | Record appears structured but should still be checked by a human |
| `Needs human review` | Record may need closer review before publication or use |

## Responsible data design

This data model is designed to keep legislative information traceable and auditable.

Important design choices include:

- Keep source URLs attached to every structured record
- Preserve the original bill number and chamber
- Separate raw descriptions from plain-English summaries
- Treat generated categories and summaries as reviewable
- Avoid presenting automated outputs as final legal or policy conclusions
