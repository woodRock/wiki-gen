import json
import os

paper_id = "df2b0e26d0599ce3e70df8a9da02e51594e0e992"
fetch_path = f"/Users/woodj/.gemini/tmp/wiki-gen/{paper_id}.fetch.json"

with open(fetch_path, 'r') as f:
    data = json.load(f)

data["lead_paragraph"] = "BERT (Bidirectional Encoder Representations from Transformers) is a groundbreaking language representation model that introduced deep bidirectional pre-training for language understanding. Unlike previous models that processed text left-to-right or right-to-left, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference."

data["main_concept"] = "Deep Bidirectional Transformers"

data["infobox_data"] = {
    "architecture_type": "Transformer Encoder (Bidirectional)",
    "key_innovation": "Masked Language Model (MLM) and Next Sentence Prediction (NSP) pre-training objectives.",
    "performance_metric": "State-of-the-art on 11 NLP tasks, including GLUE, SQuAD, and SWAG.",
    "computational_efficiency": "Highly parallelizable during training; enables efficient fine-tuning for downstream tasks."
}

data["sections"] = [
    {
        "title": "Bidirectional Pre-training",
        "content": "The fundamental technical innovation of BERT is applying the bidirectional training of Transformer, a popular attention model, to language modeling. Previous attempts at bidirectional models were limited because they were either a combination of two unidirectional models (left-to-right and right-to-left) or they allowed tokens to 'see themselves' in multi-layer architectures.\n\nBERT addresses this by using a 'Masked Language Model' (MLM) objective. During pre-training, some percentage of the input tokens are masked at random, and the model's goal is to predict the original vocabulary id of the masked word based only on its context. This allows the representation to fuse the left and the right context, which allows us to pre-train a deep bidirectional Transformer."
    },
    {
        "title": "The Masked Language Model (MLM)",
        "content": "In order to train a deep bidirectional representation, the authors simply mask 15% of the input tokens at random. Unlike standard directional models, the MLM objective allows the model to see the entire sequence, making it more effective at capturing nuanced linguistic relationships.\n\nTo ensure the model doesn't become over-reliant on the '[MASK]' token during fine-tuning (where masks don't exist), the authors used a specific strategy: 80% of the time the token is replaced with [MASK], 10% of the time with a random token, and 10% of the time it is kept unchanged. This forces the model to maintain a valid contextual representation for every input token."
    },
    {
        "title": "Next Sentence Prediction (NSP)",
        "content": "Many important downstream tasks such as Question Answering (QA) and Natural Language Inference (NLI) are based on understanding the relationship between two sentences, which is not directly captured by language modeling.\n\nTo train a model that understands sentence relationships, BERT is pre-trained for a binarized 'next sentence prediction' task that can be generated from any monolingual corpus. When choosing sentences A and B for each pre-training example, 50% of the time B is the actual next sentence that follows A, and 50% of the time it is a random sentence from the corpus. The model then learns to predict whether B is the next sentence or not."
    },
    {
        "title": "Fine-Tuning BERT",
        "content": "Fine-tuning BERT is relatively inexpensive. All parameters are fine-tuned jointly by simply adding one additional output layer for the specific task at hand. For sequence-level tasks, BERT uses the representation of the first token in the sequence (the special [CLS] token).\n\nThis unified architecture allows BERT to achieve state-of-the-art results on a wide variety of tasks with minimal task-specific architectural changes. The authors demonstrated this by breaking records on the GLUE benchmark, SQuAD question answering, and several other competitive NLP leaderboards."
    }
]

data["concept_breakdown"] = [
    {
        "concept": "Bidirectionality",
        "description": "The ability of the model to look at both the preceding and following words in a sequence simultaneously to understand context."
    },
    {
        "concept": "Masked Language Model (MLM)",
        "description": "A pre-training task where certain words in a sentence are hidden, forcing the model to use surrounding context to predict them."
    },
    {
        "concept": "Transformer Encoder",
        "description": "The specific part of the Transformer architecture used by BERT, which focuses on extracting deep contextual features from an input sequence."
    },
    {
        "concept": "Self-Attention",
        "description": "The mechanism that allows BERT to weight the importance of different words in a sentence relative to each other."
    },
    {
        "concept": "[CLS] Token",
        "description": "A special classification token added to the beginning of every sequence, used as the aggregate representation for sequence-level tasks."
    }
]

data["math_equations"] = [
    {
        "name": "Attention Weighting",
        "latex": "\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{QK^T}{\\sqrt{d_k}}\\right)V",
        "explanation": "The core attention mechanism used in each of BERT's layers to compute contextual relationships between tokens.",
        "symbols": [
            {"symbol": "Q, K, V", "meaning": "Query, Key, and Value matrices derived from the input"},
            {"symbol": "d_k", "meaning": "The dimension of the keys, used for scaling"}
        ]
    }
]

data["figure_explanations"] = [
    {
        "figure_index": 1,
        "explanation": "Comparison of BERT's bidirectional architecture with OpenAI GPT (unidirectional) and ELMo (shallow concatenation of two unidirectional models)."
    },
    {
        "figure_index": 2,
        "explanation": "BERT input representation, showing how token, segment, and position embeddings are summed to form the final input vector."
    }
]

data["see_also"] = [
    {"topic": "Transformer", "description": "The fundamental architecture upon which BERT is built."},
    {"topic": "GPT (Generative Pre-trained Transformer)", "description": "A contemporary unidirectional model that focuses on generative tasks rather than understanding."},
    {"topic": "RoBERTa", "description": "A robustly optimized BERT approach that improved pre-training by removing the NSP task and training on more data."},
    {"topic": "Word2Vec", "description": "An earlier, non-contextual word embedding method that BERT significantly improved upon."}
]

data["glossary_terms"] = [
    {"term": "Pre-training", "definition": "The process of training a model on a large dataset to learn general features before task-specific fine-tuning."},
    {"term": "Fine-tuning", "definition": "Adapting a pre-trained model to a specific task using a smaller, labeled dataset."},
    {"term": "Tokenization", "definition": "Breaking down text into smaller units (tokens) that the model can process."},
    {"term": "GLUE", "definition": "General Language Understanding Evaluation; a collection of diverse natural language understanding tasks."},
    {"term": "Embedding", "definition": "A mathematical representation of a word or token as a high-dimensional vector."}
]

with open(fetch_path, 'w') as f:
    json.dump(data, f, indent=2)
