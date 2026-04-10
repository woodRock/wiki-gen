# Wiki-Gen

A system that turns research PDFs into a Wikipedia-style static website.

## Overview

Wiki-Gen processes research papers from the `ingest/` directory, extracts metadata and figures, generates a Wikipedia-style summary (using a language model), and builds a static HTML site.

## Multi-Agent Support

This repository is configured to be friendly with **Claude**, **Gemini**, and **Qwen**.

### Skills

Custom skills are located in the `skills/` directory and are symlinked to:
- `.claude/skills/`
- `.gemini/skills/`
- `.qwen/skills/`

These skills provide the model with domain-specific knowledge and instructions for:
- **ingest**: Process one or all PDFs in `ingest/`.
- **build**: Regenerate the static site from the database.
- **reingest**: Reprocess a paper from scratch.
- **fix-title**: Correct a paper's title in the database.
- **wiki-gen**: General help and information about the system.

### Custom Commands

Slash commands are available in both Gemini and Qwen:
- `/ingest [filename]`
- `/build`
- `/reingest <filename or paper_id>`
- `/fix-title <paper_id> <new title>`
- `/wiki-gen`

## Workflow

1.  **Ingest**: Place PDFs in the `ingest/` directory.
2.  **Process**: Run `/ingest` (or the equivalent skill) to process the papers.
3.  **View**: Open `wiki/site/index.html` to view the generated site.

## Directory Structure

- `ingest/`: Input PDFs.
- `processed/`: Successfully processed PDFs.
- `scripts/`: Python scripts for processing and site generation.
- `skills/`: Cross-tool skill definitions.
- `wiki/data/`: SQLite database.
- `wiki/site/`: Generated static website.
