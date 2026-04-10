import json
import os

paper_id = "90abbc2cf38462b954ae1b772fac9532e2ccd8b0"
fetch_path = f"/Users/woodj/.gemini/tmp/wiki-gen/{paper_id}.fetch.json"

with open(fetch_path, 'r') as f:
    data = json.load(f)

data["lead_paragraph"] = "GPT-3 (Generative Pre-trained Transformer 3) is a massive autoregressive language model with 175 billion parameters that demonstrates remarkable few-shot learning capabilities. By training on hundreds of billions of words, GPT-3 can perform a wide variety of NLP tasks—including translation, question-answering, and cloze tasks—without any fine-tuning, often matching the performance of specialized state-of-the-art models. This paper marks a significant shift towards general-purpose AI systems that can adapt to new tasks through simple natural language prompts."

data["main_concept"] = "Few-Shot Learning at Scale"

data["infobox_data"] = {
    "architecture_type": "Autoregressive Transformer (Decoder-only)",
    "key_innovation": "Scaling language models to 175B parameters to enable few-shot task performance without fine-tuning.",
    "performance_metric": "State-of-the-art results on many NLP datasets in zero-, one-, and few-shot settings.",
    "computational_efficiency": "High training cost (3.14e23 FLOPS) but efficient task adaptation via in-context learning."
}

data["sections"] = [
    {
        "title": "Scaling Laws and the 175B Parameter Model",
        "content": "GPT-3 represents a 10x increase in scale over its predecessor, GPT-2. The researchers found that as language models grow in size, they develop emergent capabilities that are not present in smaller models. The 175 billion parameter version of GPT-3 uses the same basic Transformer architecture as previous models but with increased depth (96 layers) and width (12,288-dimensional embeddings).\n\nThis massive scale allows the model to capture a vast amount of world knowledge and linguistic patterns from its training data, which included Common Crawl, WebText2, Books1, Books2, and Wikipedia. The results suggest that for many tasks, performance follows a power-law relationship with model size, data, and compute."
    },
    {
        "title": "In-Context Learning: Zero, One, and Few-Shot",
        "content": "A key contribution of the GPT-3 paper is the formalization of 'in-context learning.' Unlike traditional models that require thousands of labeled examples and gradient updates (fine-tuning) to learn a new task, GPT-3 can be 'conditioned' using a natural language prompt.\n\nIn the **few-shot** setting, the model is given a short description of the task and a few examples (typically 10 to 100) within its context window. In the **one-shot** setting, only a single example is provided. In the **zero-shot** setting, only the task description is given. GPT-3's ability to succeed in these settings suggests it has learned a generalized 'meta-learning' capability during pre-training."
    },
    {
        "title": "Task Performance and Limitations",
        "content": "GPT-3 was evaluated on over 50 NLP datasets. It achieved state-of-the-art performance on several 'closed-book' question-answering tasks and demonstrated strong capabilities in translation and reasoning. However, it still struggles with certain tasks that require deep common sense or complex multi-step reasoning, such as the WSC (Winograd Schema Challenge).\n\nFurthermore, the model can sometimes generate biased or toxic content, reflecting the biases present in its large-scale training data. The researchers acknowledge these limitations and emphasize the need for further work in safety and alignment."
    },
    {
        "title": "The Shift from Fine-Tuning to Prompting",
        "content": "The success of GPT-3 challenges the dominant paradigm of pre-train-then-fine-tune. By showing that a sufficiently large model can adapt to tasks via prompting, GPT-3 opens up new possibilities for how humans interact with AI. Prompt engineering—the art of crafting the right input to guide the model—has since emerged as a critical skill for utilizing these large-scale foundation models."
    }
]

data["concept_breakdown"] = [
    {
        "concept": "Few-Shot Learning",
        "description": "The ability of a model to perform a task after seeing only a few examples in its input prompt, without any weights being updated."
    },
    {
        "concept": "In-Context Learning",
        "description": "The phenomenon where a language model uses the information provided in its prompt to understand and execute a specific task."
    },
    {
        "concept": "Autoregressive Model",
        "description": "A model that predicts the next token in a sequence based on all previous tokens, typical of the GPT series."
    },
    {
        "concept": "Prompt Engineering",
        "description": "The process of designing and refining the input text to a large language model to achieve a desired output or task performance."
    },
    {
        "concept": "Emergent Capabilities",
        "description": "Skills or behaviors that appear in large-scale models that were not observed or expected in their smaller counterparts."
    }
]

data["math_equations"] = [
    {
        "name": "Autoregressive Likelihood",
        "latex": "P(x) = \\prod_{i=1}^{n} P(x_i | x_1, \\dots, x_{i-1})",
        "explanation": "The objective of GPT-3 is to maximize the likelihood of the training data by predicting each token based on its preceding context.",
        "symbols": [
            {"symbol": "x_i", "meaning": "The i-th token in the sequence"},
            {"symbol": "P(x)", "meaning": "The probability of the entire sequence"}
        ]
    }
]

data["figure_explanations"] = [
    {
        "figure_index": 1,
        "explanation": "Diagram showing the difference between zero-shot, one-shot, and few-shot learning, where examples are integrated directly into the model's context window."
    },
    {
        "figure_index": 2,
        "explanation": "Accuracy scaling curves for various tasks as a function of the number of examples in the context, showing significant gains for the 175B parameter model."
    }
]

data["see_also"] = [
    {"topic": "GPT-2", "description": "The predecessor to GPT-3 which first suggested the potential of zero-shot learning."},
    {"topic": "Transformer", "description": "The underlying architecture that enables GPT-3 to process long-range dependencies efficiently."},
    {"topic": "Common Crawl", "description": "One of the primary datasets used to train GPT-3, consisting of petabytes of web data."},
    {"topic": "Prompt Engineering", "description": "The practice of optimizing prompts to improve model performance on specific tasks."}
]

data["glossary_terms"] = [
    {"term": "Parameter", "definition": "A variable within a neural network that is learned during the training process; GPT-3 has 175 billion of them."},
    {"term": "Zero-Shot", "definition": "Performing a task with no examples, only a description."},
    {"term": "Fine-Tuning", "definition": "The process of further training a pre-trained model on a specific, smaller dataset to improve performance on a specific task."},
    {"term": "Token", "definition": "A unit of text (like a word or part of a word) that a language model processes."},
    {"term": "Context Window", "definition": "The maximum number of tokens a model can 'see' at once; for GPT-3, this is 2048 tokens."}
]

with open(fetch_path, 'w') as f:
    json.dump(data, f, indent=2)
