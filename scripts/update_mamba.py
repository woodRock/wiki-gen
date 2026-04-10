import json
import os

paper_id = "7bbc7595196a0606a07506c4fb1473e5e87f6082"
fetch_path = f"/Users/woodj/.gemini/tmp/wiki-gen/{paper_id}.fetch.json"

with open(fetch_path, 'r') as f:
    data = json.load(f)

data["lead_paragraph"] = "Mamba is a breakthrough sequence modeling architecture that introduces selective state space models (SSMs) to achieve linear-time scaling and high-performance across modalities like language, genomics, and audio. By allowing SSM parameters to be functions of the input, Mamba enables content-based reasoning—a key limitation of previous subquadratic architectures. Combined with a hardware-aware parallel algorithm, Mamba matches or exceeds Transformer performance while offering 5x higher throughput and the ability to process million-length sequences."

data["main_concept"] = "Selective State Space Models (S6)"

data["infobox_data"] = {
    "architecture_type": "Selective State Space Model (SSM)",
    "key_innovation": "Input-dependent (selective) transition matrices and a hardware-aware parallel scan algorithm.",
    "performance_metric": "5x higher throughput than Transformers; state-of-the-art performance on million-length sequences.",
    "computational_efficiency": "Linear scaling in sequence length ($O(L)$) for both training and inference."
}

data["sections"] = [
    {
        "title": "From Linear SSMs to Selective Selection",
        "content": "Traditional State Space Models (SSMs) are linear time-invariant (LTI) systems that map an input sequence to an output sequence through an intermediate latent state. While efficient due to their convolutional representation, LTI systems struggle with content-based reasoning because their transition matrices are fixed and independent of the input.\n\nMamba introduces 'Selection' by making the SSM parameters ($B$, $C$, and $\\Delta$) functions of the input $x$. This allows the model to 'selectively' propagate or forget information based on the current token, enabling it to handle discrete modalities like language where certain words (like 'if' or 'else') dictate the importance of subsequent information."
    },
    {
        "title": "Hardware-Aware Parallel Scan",
        "content": "The introduction of input-dependency breaks the convolutional property of SSMs, seemingly requiring a slow recurrent computation. Mamba overcomes this through a hardware-aware parallel scan algorithm. Instead of materializing the full expanded state in slow GPU memory (HBM), the model performs the discretization and recurrence in fast SRAM.\n\nBy utilizing the memory hierarchy of modern GPUs, Mamba achieves the efficiency of convolutions while maintaining the flexibility of recurrent models. This allows the model to scale linearly with sequence length, making it practical for processing extremely long contexts that would be computationally prohibitive for Transformers' $O(L^2)$ attention."
    },
    {
        "title": "The Mamba Block Architecture",
        "content": "The Mamba architecture simplifies the standard deep learning stack by integrating the selective SSM into a streamlined block. Unlike Transformers, which alternate between attention and MLP layers, Mamba uses a single homogenous block that combines linear projections, 1D convolutions, and the selective SSM.\n\nThis design removes the need for attention mechanisms entirely, significantly reducing the memory footprint for KV caches during inference. The result is a model that is both faster to train and more efficient to deploy, particularly for long-generation tasks."
    },
    {
        "title": "Empirical Performance and Scaling",
        "content": "In language modeling benchmarks, Mamba-3B matches the performance of Transformers twice its size. It demonstrates consistent improvements as the sequence length increases, whereas Transformers often suffer from performance degradation or memory exhaustion beyond their training window.\n\nBeyond language, Mamba excels in genomics (long DNA sequences) and audio modeling, where its ability to handle millions of time steps with linear complexity provides a decisive advantage over previous state-of-the-art architectures."
    }
]

data["concept_breakdown"] = [
    {
        "concept": "Selective SSM (S6)",
        "description": "A state space model where the parameters vary with the input, allowing the model to choose which information to keep or discard."
    },
    {
        "concept": "Parallel Scan",
        "description": "A technique to compute prefix sums or recurrences in parallel, adapted in Mamba for hardware-efficient SSM updates."
    },
    {
        "concept": "Linear Scaling",
        "description": "Computational complexity that grows proportionally to the sequence length ($O(L)$), enabling processing of very long sequences."
    },
    {
        "concept": "Hardware-Awareness",
        "description": "Designing algorithms to minimize data movement between different levels of GPU memory (HBM vs. SRAM) to maximize throughput."
    },
    {
        "concept": "Discretization",
        "description": "The process of converting a continuous-time state space model into a discrete-time version for digital computation."
    }
]

data["math_equations"] = [
    {
        "name": "Continuous State Space Model",
        "latex": "h'(t) = A h(t) + B x(t), \\quad y(t) = C h(t)",
        "explanation": "The fundamental linear ODE that defines the evolution of the latent state $h(t)$ in a continuous SSM.",
        "symbols": [
            {"symbol": "h(t)", "meaning": "Latent state at time t"},
            {"symbol": "x(t)", "meaning": "Input signal at time t"},
            {"symbol": "A, B, C", "meaning": "System matrices defining state transitions and output mapping"}
        ]
    },
    {
        "name": "Selective Discretization",
        "latex": "\\bar{A} = \\exp(\\Delta A), \\quad \\bar{B} = (\\Delta A)^{-1}(\\exp(\\Delta A) - I) \\cdot \\Delta B",
        "explanation": "In Mamba, the step size $\\Delta$ and matrices $B$ and $C$ are functions of the input $x$, making the discretized matrices $\\bar{A}$ and $\\bar{B}$ time-varying.",
        "symbols": [
            {"symbol": "\\Delta", "meaning": "Input-dependent step size (timescale)"},
            {"symbol": "\\bar{A}, \\bar{B}", "meaning": "Discretized transition and input matrices"}
        ]
    }
]

data["figure_explanations"] = [
    {
        "figure_index": 1,
        "explanation": "Comparison of the selective SSM selection mechanism vs. standard LTI SSMs, highlighting how parameters change based on the input tokens."
    },
    {
        "figure_index": 2,
        "explanation": "Diagram of the Mamba block architecture, showing the integration of convolutions and selective SSMs."
    }
]

data["see_also"] = [
    {"topic": "Structured State Space Models (S4)", "description": "The predecessor to Mamba that introduced efficient initialization and parameterization for SSMs."},
    {"topic": "Transformer", "description": "The dominant architecture for sequence modeling that Mamba aims to replace for long-context tasks."},
    {"topic": "Linear Attention", "description": "A class of attention mechanisms that also achieve linear complexity but often lack the reasoning power of SSMs."},
    {"topic": "FlashAttention", "description": "A hardware-aware algorithm for Transformers that inspired Mamba's memory-efficient parallel scan."}
]

data["glossary_terms"] = [
    {"term": "SSM", "definition": "State Space Model; a mathematical model used to describe systems via state variables."},
    {"term": "LTI", "definition": "Linear Time-Invariant; a system whose behavior does not change over time, regardless of the input."},
    {"term": "SRAM", "definition": "Static Random-Access Memory; fast, on-chip memory used for intermediate computations in GPUs."},
    {"term": "HBM", "definition": "High Bandwidth Memory; the primary, larger, but slower memory used on GPUs."},
    {"term": "Prefix Sum", "definition": "A mathematical operation where each element in a sequence is the sum of all preceding elements."}
]

with open(fetch_path, 'w') as f:
    json.dump(data, f, indent=2)
