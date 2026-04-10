"""
Claude CLI-powered paper content generation.
Uses `claude -p` (no API key needed) to produce rich Wikipedia-style content and Manim animations.
"""

import json
import re
import subprocess
import tempfile
from pathlib import Path

import fitz

ANIMATIONS_DIR = Path("wiki/site/assets/animations")


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def extract_full_text(pdf_path, max_chars=30000):
    """Extract text from PDF, limiting to avoid context overflow."""
    doc = fitz.open(str(pdf_path))
    text = ""
    for page in doc:
        text += page.get_text()
        if len(text) >= max_chars:
            break
    doc.close()
    
    # Sanitize text
    text = text.replace('\x00', '')  # Remove null bytes
    text = "".join(ch for ch in text if ch.isprintable() or ch in '\n\r\t')
    
    return text[:max_chars]


import os

# Default to gemini if not specified
PROVIDER = os.getenv("LLM_PROVIDER", "gemini")

def ask_llm(prompt):
    """Send a prompt to the configured LLM CLI (Gemini or Claude)."""
    cmd = [PROVIDER, "-p", prompt]
    print(f"    [LLM] Using {PROVIDER}...")
    
    result = subprocess.run(
        cmd,
        capture_output=True, text=True, timeout=600
    )
    if result.returncode != 0:
        raise RuntimeError(f"{PROVIDER} CLI error: {result.stderr[:500]}")
    return result.stdout.strip()


# ---------------------------------------------------------------------------
# Paper analysis
# ---------------------------------------------------------------------------

def analyze_paper(paper_title, paper_text, figures):
    """
    Ask Claude to produce a rich Wikipedia-quality analysis of the paper.

    figures: list of dicts with keys: index, caption, page
    """
    figure_context = ""
    if figures:
        figure_context = "\n\nFigures extracted from the PDF:\n"
        for fig in figures:
            caption = fig.get('caption') or 'no caption'
            figure_context += f"  Figure {fig['index']} (page {fig.get('page', '?')}): {caption}\n"

    prompt = f"""You are writing a Wikipedia article for a research paper. Your goal is a rich, authoritative, and deeply technical article that genuinely teaches the reader — not a bland summary.

Paper Title: {paper_title}
{figure_context}
Paper Text:
{paper_text}

Return a single JSON object with these exact fields:

{{
  "main_concept": "Short name for the paper's primary contribution (e.g. 'Scaled Dot-Product Attention', 'Polar Coordinate KV Quantization')",

  "lead_paragraph": "2-3 sentence Wikipedia-style opening. State what the paper introduces, what problem it solves, and its significance. Be specific — cite numbers or results if they are striking.",

  "infobox_data": {{
    "architecture_type": "e.g. Transformer, CNN, Hybrid",
    "key_innovation": "The single most important technical change",
    "performance_metric": "Striking result from the paper",
    "computational_efficiency": "Comment on memory or FLOPs"
  }},

  "sections": [
    {{
      "title": "Use a SPECIFIC title from the paper's content — not 'Method' but e.g. 'Scaled Dot-Product Attention Mechanism' or 'Sign-Bit Quantization via JL Projections'",
      "content": "3-5 paragraphs of encyclopedic prose separated by \\n\\n. Delve DEEPLY into the math and architecture. Explain the 'why' behind design choices. Use [[Figure X]] to reference figures where appropriate.",
      "figure_index": null
    }}
  ],

  "concept_breakdown": [
    {{
      "concept": "Specific sub-component or idea",
      "description": "2-3 sentences explaining this specific concept in detail."
    }}
  ],

  "math_equations": [
    {{
      "name": "Human-readable equation name",
      "latex": "Full LaTeX (no surrounding $)",
      "explanation": "Deep intuition for what this formula computes and why it is designed this way. Break down the variables.",
      "symbols": [
        {{"symbol": "Q", "meaning": "Query matrix — the set of vectors being matched against keys"}},
        {{"symbol": "d_k", "meaning": "Dimension of the key vectors, used to scale and stabilise gradients"}}
      ]
    }}
  ],

  "figure_explanations": [
    {{
      "figure_index": 1,
      "explanation": "Provide a detailed technical breakdown of what this figure shows. Explain the axes, the data flow, or the architectural component it depicts."
    }}
  ],

  "see_also": [
    {{
      "topic": "Name of a related concept, paper, or technique",
      "description": "One sentence explaining the connection"
    }}
  ],

  "glossary_terms": [
    {{"term": "Technical Term", "definition": "Clear definition for someone new to the field"}}
  ],

  "animation_description": "Describe a 15-second Manim animation that visually explains the core concept. Be specific: name the exact visual elements (axes, labelled arrows, coloured vectors, matrices, dots), describe the sequence of transformations step by step, and suggest colours. Focus on the one key idea that would most benefit from visual explanation."
}}

Rules:
- Sections should have PAPER-SPECIFIC titles, not generic ones.
- Write 4-6 sections. Assign figure_index (1-based integer) to sections where that figure naturally illustrates the point.
- Include ALL figures in figure_explanations.
- Include 3-5 math equations with full symbol breakdowns.
- Include 4-6 items in concept_breakdown.
- Include 5-8 glossary terms.
- Include 4-6 see_also entries.
- Use a formal, authoritative, yet educational tone.
- Return only valid JSON. No markdown, no commentary."""

    response = ask_llm(prompt)
    match = re.search(r'\{[\s\S]*\}', response)
    return json.loads(match.group(0) if match else response)

    response = ask_llm(prompt)
    match = re.search(r'\{[\s\S]*\}', response)
    return json.loads(match.group(0) if match else response)


# ---------------------------------------------------------------------------
# Manim animation
# ---------------------------------------------------------------------------

def generate_manim_code(main_concept, animation_description, paper_title):
    """Use Claude to generate working Manim Community Edition code."""
    prompt = f"""Generate Manim Community Edition Python code that animates this concept.

Paper: {paper_title}
Core Concept: {main_concept}
Animation to create: {animation_description}

STRICT REQUIREMENTS:
- Start with: from manim import *
- Exactly ONE class extending Scene, CamelCase name matching the concept (e.g., AttentionMechanism)
- Total runtime: 10-20 seconds with self.wait() between major steps
- Use MathTex for math (e.g., MathTex(r"Q K^T / \\sqrt{{d_k}}"))
- Use Text() for plain labels
- Use Write(), Create(), FadeIn(), FadeOut(), Transform() for animations
- 2D only — no ThreeDScene
- No external images or files
- No try/except blocks
- 4-6 clear visual steps — clarity over complexity

Return ONLY the raw Python code. No markdown fences, no explanation."""

    code = ask_llm(prompt)
    code = re.sub(r'^```python\n?', '', code)
    code = re.sub(r'^```\n?', '', code)
    code = re.sub(r'\n?```$', '', code)
    return code.strip()


def fix_manim_code(code, error_message):
    """Ask Claude to fix broken Manim code given the error output."""
    prompt = f"""This Manim Community Edition code produced an error. Fix it so it renders correctly.

ORIGINAL CODE:
{code}

ERROR OUTPUT:
{error_message}

Common fixes:
- MathTex needs raw strings r"..." and double braces for LaTeX groups: {{{{...}}}}
- next_to() uses Manim constants: UP, DOWN, LEFT, RIGHT, UR, UL, DR, DL
- Don't use .above() — use .next_to(obj, UP)
- Arrow(start, end) takes positional arguments

Return ONLY the corrected Python code. No markdown, no explanation."""

    fixed = ask_llm(prompt)
    fixed = re.sub(r'^```python\n?', '', fixed)
    fixed = re.sub(r'^```\n?', '', fixed)
    fixed = re.sub(r'\n?```$', '', fixed)
    return fixed.strip()


def extract_scene_class_name(code):
    match = re.search(r'class\s+(\w+)\s*\(Scene\)', code)
    return match.group(1) if match else None


def run_manim(script_content, scene_class_name, output_filename):
    """Run Manim to generate a GIF, retrying once with Claude's help on failure."""
    ANIMATIONS_DIR.mkdir(parents=True, exist_ok=True)

    def _render(code, scene_class):
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.py', prefix='manim_scene_', delete=False
        ) as f:
            f.write(code)
            temp_path = Path(f.name)
        try:
            result = subprocess.run(
                ["manim", "-v", "WARNING", "--format=gif",
                 "-o", f"{output_filename}.gif",
                 str(temp_path), scene_class],
                capture_output=True, text=True, timeout=300
            )
            error_output = (result.stdout + result.stderr)[-1500:]
            return result.returncode == 0, error_output
        except subprocess.TimeoutExpired:
            return False, "Manim timed out after 300s"
        except FileNotFoundError:
            return False, "manim command not found"
        finally:
            temp_path.unlink(missing_ok=True)

    success, error = _render(script_content, scene_class_name)

    if not success:
        print(f"  ⚠  Manim error, asking Claude to fix...")
        fixed_code = fix_manim_code(script_content, error)
        fixed_class = extract_scene_class_name(fixed_code) or scene_class_name
        success, error = _render(fixed_code, fixed_class)

    if not success:
        print(f"  ✗  Animation failed after retry")
        return None

    for gif_file in Path("media").rglob(f"{output_filename}.gif"):
        target = ANIMATIONS_DIR / f"{output_filename}.gif"
        gif_file.rename(target)
        return f"animations/{output_filename}.gif"

    print("  ⚠  GIF not found in media/ after successful manim run")
    return None


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def generate_llm_content(pdf_path, paper_id, paper_title=None, figures=None):
    """Generate all Claude-powered content for a paper."""
    print("  📖 Extracting paper text...")
    text = extract_full_text(pdf_path)
    title = paper_title or Path(pdf_path).stem

    print("  🤖 Analyzing paper with Claude...")
    analysis = analyze_paper(title, text, figures or [])

    main_concept = analysis.get('main_concept', 'Core Method')
    animation_description = analysis.get('animation_description', '')
    print(f"  💡 Core concept: {main_concept}")

    print("  ✍  Generating Manim code with Claude...")
    manim_code = generate_manim_code(main_concept, animation_description, title)
    scene_class = extract_scene_class_name(manim_code)

    animation_path = None
    if scene_class:
        print(f"  🎬 Rendering {scene_class}...")
        animation_path = run_manim(manim_code, scene_class, paper_id)
        if animation_path:
            print(f"  ✓  Animation: {animation_path}")
        else:
            print("  ⚠  Animation skipped")
    else:
        print("  ⚠  No Scene class found in generated Manim code")

    return {
        "lead_paragraph": analysis.get("lead_paragraph", ""),
        "sections": analysis.get("sections", []),
        "figure_explanations": analysis.get("figure_explanations", []),
        "see_also": analysis.get("see_also", []),
        "math_equations": analysis.get("math_equations", []),
        "glossary_terms": analysis.get("glossary_terms", []),
        "concept_breakdown": analysis.get("concept_breakdown", []),
        "infobox_data": analysis.get("infobox_data", {}),
        "animation_path": animation_path,
        "main_concept": main_concept,
        # Legacy fields (kept for DB compatibility)
        "summary": [s.get("content", "") for s in analysis.get("sections", [])],
        "key_points": [],
    }
