# Architecture

This repository demonstrates a sanitized civic-legislation data pipeline.

The goal is to show how public legislative records can be transformed into structured civic data that supports search, summaries, issue tagging, and human review.

## Workflow

```text
Raw public bill record
        ↓
Load source data
        ↓
Validate required fields
        ↓
Clean title and metadata
        ↓
Assign policy area
        ↓
Generate plain-English summary
        ↓
Attach source URL
        ↓
Mark review status
        ↓
Export structured civic data
