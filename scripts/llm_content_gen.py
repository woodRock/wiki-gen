"""
LLM-powered paper ingestion with automatic summary, math extraction, and Manim generation.
"""

import sys
sys.path.insert(0, 'scripts')

from pathlib import Path
import fitz
import subprocess
import json
import re

def extract_full_text(pdf_path, max_chars=15000):
    """Extract text from PDF, limiting to avoid LLM context overflow."""
    doc = fitz.open(str(pdf_path))
    text = ""
    for page in doc:
        text += page.get_text()
        if len(text) >= max_chars:
            break
    doc.close()
    return text[:max_chars]

def analyze_paper_with_llm(text):
    """Use LLM to analyze paper and extract structured information."""
    # This would typically call an LLM API
    # For now, return structured template
    prompt = f"""Analyze this research paper and extract the following:

PAPER TEXT (truncated):
{text[:10000]}

Please provide a JSON response with:
1. "main_concept": The single most important concept that can be explained visually (brief description)
2. "visual_description": How to visualize this concept with Manim (specific elements to include)
3. "summary": 3-5 paragraph summary of the paper's main contributions
4. "key_points": List of 3-5 bullet points of the most important findings
5. "math_equations": List of objects with:
   - "name": Name of the equation/concept
   - "latex": LaTeX math expression  
   - "explanation": What this equation means in plain English
6. "glossary_terms": List of objects with:
   - "term": Technical term
   - "definition": Brief definition

Return ONLY valid JSON, no markdown formatting."""

    # TODO: Call actual LLM API here
    # For demo purposes, return template
    return {
        "main_concept": "Self-Attention Mechanism",
        "visual_description": "Show how query, key, and value vectors interact. Animate word embeddings becoming Q, K, V vectors, then show dot products creating attention weights as a heatmap, finally show weighted sum of values.",
        "summary": [
            "The paper introduces a novel attention mechanism that replaces recurrent and convolutional layers entirely with self-attention.",
            "The key innovation is scaled dot-product attention which prevents gradient issues in large models by normalizing with the square root of the key dimension.",
            "Multi-head attention allows the model to jointly attend to information from different representation subspaces at different positions.",
            "The architecture achieves state-of-the-art results on machine translation while being highly parallelizable."
        ],
        "key_points": [
            "Replaced recurrence with pure attention architecture",
            "Scaled dot-product attention prevents vanishing gradients", 
            "Multi-head attention captures different types of dependencies",
            "Positional encodings add sequence order information",
            "Achieved better performance with less training time"
        ],
        "math_equations": [
            {
                "name": "Scaled Dot-Product Attention",
                "latex": "\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{QK^T}{\\sqrt{d_k}}\\right)V",
                "explanation": "Computes attention by taking the dot product of queries and keys, scaling by the square root of key dimension to prevent small gradients, applying softmax to get weights, and multiplying by values."
            },
            {
                "name": "Multi-Head Attention", 
                "latex": "\\text{MultiHead}(Q, K, V) = \\text{Concat}(\\text{head}_1, \\ldots, \\text{head}_h)W^O",
                "explanation": "Runs h attention layers in parallel, each with different learned projections, then concatenates and projects the results."
            },
            {
                "name": "Positional Encoding",
                "latex": "PE_{(pos, 2i)} = \\sin\\left(\\frac{pos}{10000^{2i/d_{\\text{model}}}}\\right)",
                "explanation": "Adds position information using sine and cosine functions of different frequencies, allowing the model to attend to relative positions."
            }
        ],
        "glossary_terms": [
            {
                "term": "Self-Attention",
                "definition": "A mechanism that relates different positions of a single sequence to compute a representation of that sequence."
            },
            {
                "term": "Multi-Head Attention",
                "definition": "Running multiple attention layers in parallel to attend to information from different representation subspaces."
            },
            {
                "term": "Positional Encoding",
                "definition": "Fixed representations added to input embeddings to provide information about token positions in the sequence."
            }
        ]
    }

def generate_manim_script(visual_description, paper_title):
    """Generate Manim animation script based on visual description."""
    script = f'''"""
Manim animation: {paper_title}
{visual_description}
"""

from manim import *

class ConceptExplanation(Scene):
    def construct(self):
        # Title
        title = Text("{paper_title}", font_size=36)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        
        # Show key elements based on visual description
        # TODO: Generate specific Manim code based on the visual_description
        elements = Text("Visual Elements\\nBased on Concept", font_size=32)
        self.play(Write(elements))
        self.wait(2)
        
        # Add specific animations here
        # This should be customized based on the visual_description
        
        summary = Text("Animation Generated", font_size=32, color=GREEN)
        self.play(Write(summary))
        self.wait(1)
        self.play(FadeOut(summary))
'''
    return script

def run_manim(script_content, output_filename):
    """Run Manim to generate GIF from script."""
    # Write script to temp file
    temp_file = Path(f"/tmp/{output_filename}_temp.py")
    temp_file.write_text(script_content)
    
    try:
        # Run manim
        result = subprocess.run(
            ["manim", "-v", "WARNING", "--format=gif", 
             "-o", f"{output_filename}.gif",
             str(temp_file), "ConceptExplanation"],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            # Find and move the output file
            media_dir = Path("media")
            for gif_file in media_dir.rglob(f"{output_filename}.gif"):
                target = Path("wiki/site/assets/animations") / f"{output_filename}.gif"
                target.parent.mkdir(parents=True, exist_ok=True)
                gif_file.rename(target)
                return str(target)
        
        return None
    except Exception as e:
        print(f"  ⚠ Manim generation failed: {e}")
        return None
    finally:
        if temp_file.exists():
            temp_file.unlink()

def generate_llm_content(pdf_path, paper_id):
    """Main function to generate all LLM content for a paper."""
    print("  📖 Extracting paper text...")
    text = extract_full_text(pdf_path)
    
    print("  🤖 Analyzing paper with LLM...")
    analysis = analyze_paper_with_llm(text)
    
    print(f"  🎨 Concept to visualize: {analysis['main_concept']}")
    script = generate_manim_script(analysis['visual_description'], analysis['main_concept'])
    
    print("  🎬 Generating Manim animation...")
    animation_path = run_manim(script, paper_id)
    if animation_path:
        print(f"  ✓ Animation: {animation_path}")
    else:
        print("  ⚠ Animation generation skipped")
    
    return {
        "summary": analysis["summary"],
        "key_points": analysis["key_points"],
        "math_equations": analysis["math_equations"],
        "glossary_terms": analysis["glossary_terms"],
        "animation_path": animation_path,
        "main_concept": analysis["main_concept"]
    }

if __name__ == "__main__":
    # Test with a PDF
    pdf = Path("processed/han2025polarquant.pdf")
    if pdf.exists():
        result = generate_llm_content(pdf, "test_paper")
        print(f"\\n=== Results ===")
        print(f"Main concept: {result['main_concept']}")
        print(f"Math equations: {len(result['math_equations'])}")
        print(f"Glossary terms: {len(result['glossary_terms'])}")
        print(f"Animation: {result['animation_path']}")
