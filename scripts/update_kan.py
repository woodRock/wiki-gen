import json
import os

paper_id = "14fdab35cc6288083a38a92392af3f1da0b95a90"
fetch_path = f"/Users/woodj/.gemini/tmp/wiki-gen/{paper_id}.fetch.json"

with open(fetch_path, 'r') as f:
    data = json.load(f)

data["lead_paragraph"] = "Kolmogorov-Arnold Networks (KANs) are a novel class of neural network architectures that challenge the dominance of Multi-Layer Perceptrons (MLPs). Inspired by the Kolmogorov-Arnold representation theorem, KANs replace fixed activation functions on nodes with learnable activation functions on edges, parameterized as splines. This structural shift allows KANs to achieve superior accuracy and interpretability compared to MLPs, particularly in scientific computing tasks, while demonstrating faster neural scaling laws."

data["main_concept"] = "Kolmogorov-Arnold Networks (KANs)"

data["infobox_data"] = {
    "architecture_type": "Edge-Activation Network (Spline-based)",
    "key_innovation": "Replacing linear weights with learnable univariate activation functions on edges.",
    "performance_metric": "Faster neural scaling laws ($N^{-4}$ vs $N^{-2}$ for specific tasks) and higher accuracy with fewer parameters.",
    "computational_efficiency": "More parameter-efficient for function fitting, though currently slower per-parameter training due to spline evaluation."
}

data["sections"] = [
    {
        "title": "Theoretical Foundation: The Kolmogorov-Arnold Theorem",
        "content": "The mathematical bedrock of KANs is the Kolmogorov-Arnold representation theorem, which states that any multivariate continuous function can be represented as a finite sum of continuous univariate functions of a single variable. While MLPs are based on the Universal Approximation Theorem, KANs directly implement the structure suggested by Kolmogorov and Arnold.\n\nSpecifically, for a function of $n$ variables, the theorem guarantees a representation using $2n+1$ inner functions and a set of outer functions. KANs generalize this by stacking these structures into multiple layers, creating a deep architecture that can learn complex hierarchical representations."
    },
    {
        "title": "Architecture: Learnable Edges vs. Fixed Nodes",
        "content": "In a traditional MLP, data is multiplied by a fixed linear weight and then passed through a fixed activation function (like ReLU or Sigmoid) at the node. KANs eliminate linear weights entirely. Instead, each edge in the network is a learnable univariate function, typically represented as a B-spline.\n\nNodes in a KAN simply perform a summation of the incoming signals from the edges. This 'weight-on-edge' approach allows the network to adapt its activation functions locally to the data, enabling much greater flexibility in function approximation. [[Figure 1]] compares this structure directly with the MLP."
    },
    {
        "title": "Spline Parameterization and Grid Extension",
        "content": "To make the edge functions learnable, KANs use B-splines, which are piecewise polynomial functions defined by a grid of points. The grid density can be increased during training—a process called 'grid extension'—allowing the network to refine its approximation of complex functions without retraining from scratch.\n\nEach edge function is a combination of a base function (like SiLU) and a spline component. This hybrid approach ensures that the network has a global 'shape' while being able to capture fine-grained local details."
    },
    {
        "title": "Interpretability and AI for Science",
        "content": "One of the most significant advantages of KANs is their interpretability. Because the edge functions are univariate, they can be easily visualized and often simplified into symbolic mathematical expressions. This makes KANs ideal 'collaborators' for scientists looking to discover physical or mathematical laws.\n\nThe researchers demonstrated this by using KANs to rediscover the knot polynomial relation in mathematics and scaling laws in condensed matter physics. By pruning weak connections and performing symbolic regression on the learned edge functions, users can extract human-readable formulas from the trained model."
    }
]

data["concept_breakdown"] = [
    {
        "concept": "Kolmogorov-Arnold Representation Theorem",
        "description": "A theorem stating that multivariate continuous functions can be decomposed into a sum of univariate functions, providing the theoretical basis for KANs."
    },
    {
        "concept": "Learnable Activation Function",
        "description": "Instead of fixed functions like ReLU, KANs use univariate functions on edges that are optimized during the training process."
    },
    {
        "concept": "B-Splines",
        "description": "Piecewise polynomial functions used to parameterize the activation functions on KAN edges, allowing for flexible and local control of function shape."
    },
    {
        "concept": "Grid Extension",
        "description": "A technique in KANs where the number of spline grid points is increased to improve the resolution of the learned functions during training."
    },
    {
        "concept": "Symbolic Regression",
        "description": "The process of identifying simple mathematical formulas that approximate the learned univariate functions in a KAN, enhancing interpretability."
    }
]

data["math_equations"] = [
    {
        "name": "KAN Layer Transformation",
        "latex": "y_q = \\sum_{p=1}^{n} \\phi_{q,p}(x_p)",
        "explanation": "The transformation for a single KAN layer, where the output node $y_q$ is the sum of univariate functions $\\phi_{q,p}$ applied to each input $x_p$.",
        "symbols": [
            {"symbol": "x_p", "meaning": "p-th input variable"},
            {"symbol": "\\phi_{q,p}", "meaning": "Learnable univariate activation function on the edge between input p and output q"},
            {"symbol": "y_q", "meaning": "q-th output node"}
        ]
    },
    {
        "name": "Edge Function Decomposition",
        "latex": "\\phi(x) = w \\cdot (b(x) + \\text{spline}(x))",
        "explanation": "The parameterization of a KAN edge function, combining a basis function $b(x)$ and a learnable spline.",
        "symbols": [
            {"symbol": "b(x)", "meaning": "Basis function, typically SiLU(x)"},
            {"symbol": "\\text{spline}(x)", "meaning": "The B-spline component of the activation function"},
            {"symbol": "w", "meaning": "An overall scaling weight"}
        ]
    }
]

data["figure_explanations"] = [
    {
        "figure_index": 1,
        "explanation": "Diagram contrasting the MLP architecture (fixed node activations, learnable weights) with the KAN architecture (learnable edge activations, summation nodes)."
    },
    {
        "figure_index": 2,
        "explanation": "Illustration of the Kolmogorov-Arnold representation theorem as a two-layer KAN-like structure."
    }
]

data["see_also"] = [
    {"topic": "Multi-Layer Perceptron (MLP)", "description": "The traditional neural network architecture that KANs aim to improve upon."},
    {"topic": "Splines", "description": "The mathematical curves used to define the learnable functions in KANs."},
    {"topic": "Symbolic AI", "description": "A subfield of AI concerned with representing knowledge using symbols and logic, which KANs bridge through symbolic regression."},
    {"topic": "Neural Scaling Laws", "description": "Power-law relationships describing how model performance improves with increased parameters or data."}
]

data["glossary_terms"] = [
    {"term": "KAN", "definition": "Kolmogorov-Arnold Network; a neural network with learnable functions on its edges."},
    {"term": "Univariate Function", "definition": "A function that takes only one input variable."},
    {"term": "B-Spline", "definition": "A specific type of spline used for its efficiency and stability in approximating functions."},
    {"term": "Grid Points", "definition": "The discrete points that define the segments of a spline function."},
    {"term": "SiLU", "definition": "Sigmoid Linear Unit; a common activation function used as a basis in KAN edge functions."}
]

with open(fetch_path, 'w') as f:
    json.dump(data, f, indent=2)
