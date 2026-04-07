---
name: wiki-gen
description: Research paper ingestion and wiki generation. Use when you need to process academic paper PDFs, fetch metadata from Semantic Scholar, and generate a searchable static wiki. Also includes Manim-based GIF generation for explaining mathematical concepts.
---

# Research Paper Wiki & Manim Explainer

This skill automates the creation of a "Wikipedia for Papers" from PDF files and provides a workflow for generating Manim animations to explain complex concepts.

## Prerequisites
- `pdf2doi`, `semanticscholar`, `pymupdf`, `mkdocs`, `mkdocs-material`, `python-dotenv`
- `manim` (for GIF generation)
- `.env` file with `SEMANTIC_SCHOLAR_API_KEY`

## Workflow: Ingest Papers
When a user adds PDFs to the `ingest/` folder:
1. Run `python3 <skill_path>/scripts/processor.py`.
2. This will:
   - Extract DOI/Title.
   - Fetch metadata from Semantic Scholar.
   - Generate Markdown files in `wiki/docs/`.
   - Update `wiki/docs/index.md`.
   - Move processed PDFs to `processed/`.
3. Run `mkdocs build` in the `wiki/` directory to update the static site.

## Workflow: Generate Manim GIFs
To explain a concept (e.g., "Attention mechanism") using Manim:
1. **Plan**: Design a Manim `Scene` that visually explains the concept.
2. **Code**: Generate the Python code for the scene. Use the `manim` library (community version).
3. **Execute**: Save the code to a temporary file (e.g., `temp_scene.py`) and run:
   ```bash
   python3 <skill_path>/scripts/manim_gen.py temp_scene.py SceneName
   ```
4. **Embed**: The GIF will be saved to `wiki/docs/assets/<SceneName>.gif`. Embed it in the relevant paper's Markdown file using:
   ```markdown
   ![Explanation](./assets/SceneName.gif)
   ```

## Wiki Configuration
The `mkdocs.yml` template is located in `assets/`. If it doesn't exist in the project root's `wiki/` folder, copy it:
```bash
cp <skill_path>/assets/mkdocs.yml wiki/mkdocs.yml
```

## Directory Structure
- `ingest/`: New PDFs.
- `processed/`: Processed PDFs.
- `wiki/docs/`: Markdown files.
- `wiki/docs/assets/`: GIFs and images.
