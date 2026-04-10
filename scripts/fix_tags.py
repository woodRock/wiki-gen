
import json
import sqlite3
from pathlib import Path

# Import the tag keywords from site_generator if possible, or just redefine them
TAG_KEYWORDS = {
    "transformer": ["transformer", "attention is all you need", "bert", "gpt", "t5", "encoder-decoder"],
    "attention-mechanism": ["attention mechanism", "self-attention", "multi-head attention", "cross-attention", "scaled dot-product"],
    "computer-vision": ["image", "vision", "convolutional", "cnn", "object detection", "segmentation", "resnet", "vit", "visual"],
    "large-language-models": ["large language model", "llm", "gpt", "language model", "foundation model", "instruction tuning", "rlhf", "chat"],
    "generative-models": ["generative", "gan", "diffusion", "vae", "variational autoencoder", "image synthesis", "stable diffusion", "denoising"],
    "recurrent-networks": ["recurrent", "lstm", "gru", "rnn", "sequence model", "seq2seq"],
    "optimization": ["optimization", "gradient descent", "adam", "sgd", "learning rate", "convergence", "loss function"],
    "regularization": ["regularization", "dropout", "batch normalization", "weight decay", "overfitting", "l2"],
    "embeddings": ["embedding", "word2vec", "glove", "representation learning", "vector space", "token embedding"],
    "quantization": ["quantization", "quantized", "int8", "mixed precision", "model compression", "pruning"],
    "self-supervised-learning": ["self-supervised", "contrastive", "masked language model", "pretraining", "pre-training", "SimCLR", "BYOL"],
    "world-models": ["world model", "model-based", "environment model", "dreamer", "imagination"],
    "latent-space": ["latent space", "latent representation", "latent variable", "bottleneck", "encoding"],
    "jepa": ["jepa", "joint embedding predictive", "energy-based"],
}

def infer_tags(paper_data):
    """Infer tags for a paper based on keyword matching."""
    # Build corpus text
    parts = [
        paper_data.get('title', ''),
        paper_data.get('lead_paragraph', '') or '',
        paper_data.get('main_concept', '') or '',
        paper_data.get('abstract', '') or '',
    ]
    
    # Add sections and concept breakdown if available
    sections = json.loads(paper_data.get('sections', '[]')) if isinstance(paper_data.get('sections'), str) else paper_data.get('sections', [])
    for section in sections:
        parts.append(section.get('title', ''))
        parts.append(section.get('content', ''))
        
    concepts = json.loads(paper_data.get('concept_breakdown', '[]')) if isinstance(paper_data.get('concept_breakdown'), str) else paper_data.get('concept_breakdown', [])
    for concept in concepts:
        parts.append(concept.get('concept', ''))
        parts.append(concept.get('description', ''))

    corpus = ' '.join(parts).lower()

    inferred = []
    for tag, keywords in TAG_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in corpus:
                inferred.append(tag)
                break

    return inferred

def fix_tags():
    conn = sqlite3.connect('wiki/data/wiki.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM papers")
    papers = cursor.fetchall()
    
    updated_count = 0
    for paper in papers:
        current_tags = json.loads(paper['tags']) if paper['tags'] else []
        if not current_tags:
            new_tags = infer_tags(dict(paper))
            if new_tags:
                print(f"Updating tags for '{paper['title']}': {new_tags}")
                cursor.execute("UPDATE papers SET tags = ? WHERE paper_id = ?", (json.dumps(new_tags), paper['paper_id']))
                updated_count += 1
    
    conn.commit()
    conn.close()
    print(f"✅ Updated {updated_count} papers with inferred tags.")

if __name__ == "__main__":
    fix_tags()
