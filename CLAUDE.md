# Claude Workflow Notes

This file documents how I use Claude Code while working on this repository.

## Project goal

Build a sanitized civic-tech demo that converts public legislative records into structured, reviewable civic data.

## Working principles

- Keep public demo code separate from private or proprietary production systems.
- Never commit API keys, credentials, internal prompts, private schemas, or user data.
- Use mock data for public examples.
- Preserve source URLs for traceability.
- Treat AI-generated summaries as reviewable drafts, not final legal or policy conclusions.
- Add human-review flags when the source is broad, ambiguous, or high-impact.

## Claude Code workflow

When using Claude Code, I use it as a coding assistant rather than an autopilot.

Typical workflow:

1. Define the task and expected output.
2. Ask Claude to draft code or documentation.
3. Review the output manually.
4. Check for privacy, overclaiming, broken paths, and hallucinated assumptions.
5. Run or inspect the code.
6. Revise prompts when the output is vague, overconfident, or not auditable.
7. Commit only after I understand the change.

## Review checklist

Before committing AI-assisted work, check:

- Does the code run from the repo root?
- Are paths relative and portable?
- Are outputs clearly labeled as mock or generated?
- Is any private information included?
- Does the README accurately describe what the code actually does?
- Are AI outputs tied back to source records?
- Are uncertain outputs marked for human review?

## Known limitations

This demo does not represent a production legislative-data system.

Limitations include:

- Mock input data
- Small sample size
- No live public-data ingestion
- No production database
- No automated source verification
- No final legal or policy interpretation
- Lightweight evaluation only
