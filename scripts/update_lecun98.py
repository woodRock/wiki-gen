import json
import os

paper_id = "162d958ff885f1462aeda91cd72582323fd6a1f4"
fetch_path = f"/Users/woodj/.gemini/tmp/wiki-gen/{paper_id}.fetch.json"

with open(fetch_path, 'r') as f:
    data = json.load(f)

data["lead_paragraph"] = "Gradient-Based Learning Applied to Document Recognition introduced LeNet-5, a pioneering convolutional neural network that set the standard for modern deep learning. By combining convolutional layers, sub-sampling layers, and fully connected layers, Yann LeCun and colleagues demonstrated a robust system for handwritten character recognition that was deployed commercially to process millions of bank checks. This paper extensively details the architecture and training methods that proved backpropagation could be scaled to complex, multi-layer visual systems."

data["main_concept"] = "LeNet-5 CNN Architecture"

data["infobox_data"] = {
    "architecture_type": "7-Layer Convolutional Neural Network",
    "key_innovation": "Alternating convolutional and sub-sampling layers; Graph Transformer Networks.",
    "performance_metric": "Less than 1% error on handwritten digits (MNIST).",
    "computational_efficiency": "Highly efficient for 1990s hardware; optimized local connectivity."
}

data["sections"] = [
    {
        "title": "The LeNet-5 Architecture",
        "content": "LeNet-5 is a seven-layer convolutional neural network (excluding the input) that processes 32x32 pixel images. The architecture follows a specific sequence: Convolution (C1) -> Sub-sampling (S2) -> Convolution (C3) -> Sub-sampling (S4) -> Convolution (C5) -> Fully Connected (F6) -> Output.\n\nThis progressive reduction in spatial resolution combined with an increase in the number of feature maps allows the network to transform raw pixels into high-level categorical representations. The use of sub-sampling (specifically average pooling in this version) provides a degree of invariance to small translations and distortions in the input digit."
    },
    {
        "title": "Convolutional and Sub-sampling Layers",
        "content": "In LeNet-5, convolutional layers extract local features using 5x5 kernels. For example, the first layer (C1) produces 6 feature maps of size 28x28. The sub-sampling layers (S2 and S4) then reduce the size of these maps by a factor of two, which effectively doubles the receptive field of the neurons in the following layer.\n\nA notable detail in LeNet-5 is the sparse connection pattern between S2 and C3. Instead of every C3 map being connected to every S2 map, the authors used a specific table of connections to break symmetry and reduce the number of parameters, forcing different maps to specialize in different features."
    },
    {
        "title": "Graph Transformer Networks (GTN)",
        "content": "Beyond the individual digit recognition of LeNet-5, the paper introduces Graph Transformer Networks (GTNs) for handling whole documents. GTNs allow the system to perform 'segmentation-free' recognition by treating the entire sequence of characters as a graph of possible interpretations.\n\nBy optimizing a global loss function that accounts for the alignment between the predicted sequence and the true label, the system can learn to segment and recognize characters simultaneously. This approach was critical for the commercial success of the system in reading zip codes and bank checks where character boundaries are often ambiguous."
    },
    {
        "title": "The MNIST Dataset",
        "content": "The 1998 paper also serves as the formal introduction of the MNIST dataset, which has since become the 'Hello World' of machine learning. MNIST was created by re-mixing and normalizing digits from the USPS and NIST datasets to provide a standard benchmark for comparing different recognition algorithms.\n\nLeNet-5 achieved an error rate of 0.95% on the MNIST test set, outperforming several other methods including Support Vector Machines (SVMs) and simpler fully connected networks. This benchmark helped establish CNNs as the state-of-the-art for visual pattern recognition."
    }
]

data["concept_breakdown"] = [
    {
        "concept": "Feature Map",
        "description": "A 2D array of neurons where each neuron detects the same feature at different locations in the input."
    },
    {
        "concept": "Sub-sampling",
        "description": "A layer that reduces the spatial resolution of feature maps, providing spatial invariance and reducing computational cost."
    },
    {
        "concept": "Average Pooling",
        "description": "The specific type of sub-sampling used in LeNet-5, where the average value of a 2x2 neighborhood is calculated."
    },
    {
        "concept": "Sparse Connections",
        "description": "A technique used between layers to limit parameter count and encourage feature specialization."
    },
    {
        "concept": "MNIST",
        "description": "The Mixed National Institute of Standards and Technology dataset of handwritten digits, established by this paper."
    }
]

data["math_equations"] = [
    {
        "name": "Activation Function (Squashing)",
        "latex": "f(a) = A \\tanh(S a)",
        "explanation": "LeNet-5 uses a scaled hyperbolic tangent function, where $A=1.7159$ and $S=2/3$, ensuring that the non-linearities are in their most active range.",
        "symbols": [
            {"symbol": "a", "meaning": "Weighted sum of inputs to the neuron"},
            {"symbol": "f(a)", "meaning": "The activated output"}
        ]
    }
]

data["figure_explanations"] = [
    {
        "figure_index": 2,
        "explanation": "The classic LeNet-5 architecture diagram, showing the flow of information through the seven layers and the increasing abstraction of features."
    }
]

data["see_also"] = [
    {"topic": "LeNet-1", "description": "The first version of the LeNet architecture, developed in 1989."},
    {"topic": "Backpropagation", "description": "The algorithm used to train LeNet-5 by updating weights based on the gradient of the loss function."},
    {"topic": "AlexNet", "description": "The 2012 architecture that scaled LeNet's principles to much larger datasets and GPUs."},
    {"topic": "Graph Transformer Networks", "description": "The framework introduced in this paper for sequence-level document recognition."}
]

data["glossary_terms"] = [
    {"term": "Pooling", "definition": "A form of non-linear down-sampling used to reduce the spatial size of the representation."},
    {"term": "Recurrent Connection", "definition": "A connection that loops back to an earlier stage, though LeNet-5 is primarily feed-forward."},
    {"term": "Gradient Descent", "definition": "An optimization algorithm used to minimize the loss function by following the negative gradient."},
    {"term": "Hyperbolic Tangent", "definition": "A sigmoid-shaped mathematical function used as an activation non-linearity."},
    {"term": "Segmentation", "definition": "The process of dividing a document or image into meaningful parts, such as individual characters."}
]

with open(fetch_path, 'w') as f:
    json.dump(data, f, indent=2)
