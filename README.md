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
