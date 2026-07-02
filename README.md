# Civic Legislation Data Pipeline

Sanitized civic-tech demo for turning public legislative records into structured, usable bill data.

## Overview

This repository presents a public, sanitized version of a legislative-data workflow inspired by civic-engagement work at Pinion.

The project demonstrates how messy legislative information can be converted into structured civic data that supports bill tracking, summaries, search, issue tagging, and public understanding.

This public version uses mock data, public examples, and sanitized code. It does **not** include proprietary Pinion code, private infrastructure, API keys, internal prompts, production database schemas, credentials, user data, or non-public platform information.

## Why this project matters

Legislative information is public, but it is often difficult for ordinary citizens to understand or use.

Bill records can be long, inconsistent, technical, and spread across multiple government sources. A civic-engagement platform needs a way to transform those records into clearer, structured information while preserving accuracy and source traceability.

This project shows one approach to that problem:

```text
Public legislative record
        ↓
Data extraction
        ↓
Cleaning and normalization
        ↓
Structured bill fields
        ↓
Issue tagging and summary generation
        ↓
Searchable civic data
```

## Project goals

The goal of this demo is to show how legislative data can be transformed from raw public records into a cleaner format that can support civic products.

The workflow is designed to:

- Extract key bill information from public legislative records
- Normalize inconsistent fields
- Structure bill metadata for easier search and filtering
- Generate plain-English summaries
- Preserve links back to source material
- Support issue tagging for civic engagement
- Demonstrate responsible handling of public policy data

## Working demo

This repository includes a small mock data workflow that shows how raw legislative records can be converted into structured civic data.

**Raw mock data:** [`data/sample_bills_raw.csv`](data/sample_bills_raw.csv)  
**Structured mock data:** [`data/sample_bills_structured.csv`](data/sample_bills_structured.csv)  
**Transformation script:** [`src/structure_legislation.py`](src/structure_legislation.py)  
**Generated output:** [`outputs/structured_bill_output.csv`](outputs/structured_bill_output.csv)  
**Architecture notes:** [`docs/architecture.md`](docs/architecture.md)  
**Data dictionary:** [`docs/data_dictionary.md`](docs/data_dictionary.md)

## Claude-powered summarization module

This repo includes an optional Claude API-powered summarization module.

**Prompt:** [`prompts/bill_summarization_prompt.md`](prompts/bill_summarization_prompt.md)  
**Claude summarizer:** [`src/claude_bill_summarizer.py`](src/claude_bill_summarizer.py)  
**Evaluation checks:** [`evaluation/expected_summary_checks.csv`](evaluation/expected_summary_checks.csv)  
**Evaluation script:** [`src/evaluate_summaries.py`](src/evaluate_summaries.py)  
**Claude workflow notes:** [`CLAUDE.md`](CLAUDE.md)

To run the Claude summarizer:

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key-here"
python src/claude_bill_summarizer.py
To run the workflow locally:

```bash
pip install -r requirements.txt
python src/structure_legislation.py
```

The demo uses fictional bill records and exists only to show the structure of the workflow.

## Example use case

A user should be able to start with a public bill record and end with structured information such as:

- Bill number
- Bill title
- Legislative chamber
- Sponsor
- Current status
- Last action date
- Policy category
- Plain-English summary
- Source URL
- Confidence or review status

The point is not only to collect data, but to make legislative information easier to understand and act on.

## Repository structure

```text
civic-legislation-data-pipeline/
│
├── README.md
├── requirements.txt
│
├── data/
│   ├── sample_bills_raw.csv
│   └── sample_bills_structured.csv
│
├── src/
│   └── structure_legislation.py
│
├── outputs/
│   └── structured_bill_output.csv
│
└── docs/
    ├── architecture.md
    └── data_dictionary.md
```

## Data model

A structured bill record includes fields such as:

| Field | Description |
| --- | --- |
| `bill_id` | Unique mock bill identifier |
| `bill_number` | Official-style bill number |
| `clean_title` | Cleaned and standardized bill title |
| `chamber` | House, Senate, or other chamber |
| `sponsor` | Primary sponsor, when available |
| `status` | Current bill status |
| `last_action_date` | Most recent legislative action date |
| `policy_area` | High-level issue category |
| `plain_english_summary` | Short summary written for public understanding |
| `source_url` | Link back to the original source record |
| `review_status` | Whether the record should receive human review |

## Technical approach

The demo script performs a simplified version of a legislative-data pipeline:

1. Loads mock raw bill records from CSV
2. Validates required fields
3. Cleans bill titles and metadata
4. Assigns a policy area using keyword matching
5. Creates a plain-English summary from the raw description
6. Preserves the source URL for traceability
7. Adds a review status field
8. Exports a structured CSV output

This is intentionally lightweight. The goal is to demonstrate the workflow and design logic, not to reproduce a production system.

## Responsible AI and civic-data approach

Legislative data affects public understanding of civic issues, so AI-assisted outputs should be treated carefully.

This project is designed around several principles:

- Keep source links attached to generated summaries
- Distinguish extracted facts from generated explanations
- Use human review for uncertain or high-impact records
- Avoid overstating what a bill does
- Preserve original legislative context
- Make structured outputs auditable
- Prioritize clarity without sacrificing accuracy

## What is intentionally excluded

This repository does **not** include:

- Proprietary Pinion source code
- Production database schemas
- API keys or credentials
- Internal prompts
- Private platform data
- User data
- Internal strategy documents
- Non-public business logic
- Any information that should remain confidential

## Skills demonstrated

- Civic-tech product thinking
- Legislative data structuring
- Public-data workflow design
- Python data cleaning
- AI-assisted summarization concepts
- Source tracking
- Responsible AI documentation
- Public-interest technology
- Translating complex government records into usable civic information

## Why this belongs in my portfolio

This project reflects my broader interest in civic technology and public-impact AI: taking complex public systems and making them easier for people to understand, navigate, and use.

The technical challenge is not just automation. It is building a workflow that respects accuracy, transparency, and public trust while making legislative information more accessible.
