import json
import os

paper_id = "2c03df8b48bf3fa39054345bafabfeff15bfd11d"
fetch_path = f"/Users/woodj/.gemini/tmp/wiki-gen/{paper_id}.fetch.json"

with open(fetch_path, 'r') as f:
    data = json.load(f)

data["lead_paragraph"] = "Deep Residual Learning for Image Recognition introduced ResNets, a groundbreaking neural network architecture that enabled the training of substantially deeper networks by using skip connections. By reformulating layers as learning residual functions with reference to the layer inputs, the authors addressed the degradation problem where accuracy saturates and then rapidly diminishes as network depth increases. ResNets won the ILSVRC 2015 competition and have since become a foundational component of modern computer vision and deep learning."

data["main_concept"] = "Deep Residual Learning (ResNets)"

data["infobox_data"] = {
    "architecture_type": "Residual Convolutional Neural Network",
    "key_innovation": "Identity shortcut connections (skip connections) to bypass one or more layers.",
    "performance_metric": "3.57% error on ImageNet test set; won ILSVRC 2015.",
    "computational_efficiency": "Enables training of 152-layer networks with lower complexity than VGG-16."
}

data["sections"] = [
    {
        "title": "The Degradation Problem",
        "content": "As neural networks grew deeper, researchers encountered a counterintuitive phenomenon: adding more layers led to higher training error, a problem distinct from overfitting. This 'degradation' suggested that deep systems were difficult to optimize. If a shallow architecture can be augmented with identity mappings to form a deeper counterpart, the deeper model should, in theory, perform at least as well as the shallow one.\n\nHowever, experiments showed that standard solvers struggled to find these identity solutions. ResNets address this by explicitly allowing the network to learn the difference, or residual, between the input and the desired output, making identity mappings much easier to learn. [[Figure 1]] illustrates this residual learning block."
    },
    {
        "title": "Residual Learning Blocks and Shortcuts",
        "content": "The core of the ResNet is the residual block. Instead of trying to directly learn a mapping $H(x)$, the block is designed to learn $F(x) = H(x) - x$. The final output is then obtained by adding the input back: $y = F(x) + x$. This 'identity shortcut connection' skip-layers without adding extra parameters or computational complexity.\n\nThese shortcuts allow gradients to flow more easily through the network during backpropagation, mitigating the vanishing gradient problem. In many cases, the residual functions $F(x)$ are small, and the shortcut connections provide a 'highway' for information to pass through the deep stack."
    },
    {
        "title": "Architecture: VGG-style and Bottleneck Designs",
        "content": "The paper explores several ResNet architectures, including a 34-layer plain network and its residual counterpart. For deeper networks like ResNet-50, 101, and 152, the authors introduced 'bottleneck' blocks. These blocks use 1x1 convolutions to reduce and then restore dimensions, which significantly improves computational efficiency while maintaining high depth.\n\nThis design allowed the 152-layer ResNet to achieve state-of-the-art results while having lower complexity (FLOPs) than the 16-layer VGG-16 network. The consistency of these results across different depths demonstrated the robustness of the residual learning framework."
    },
    {
        "title": "Impact and Legacy",
        "content": "ResNets revolutionized deep learning by proving that depth was not just limited by hardware, but by architectural design. The principles of residual learning have been adopted far beyond image recognition, influencing the design of Transformers (which use residual connections), GANs, and various reinforcement learning agents.\n\nThe paper remains one of the most cited works in artificial intelligence, and ResNet-50 continues to serve as a standard benchmark and backbone for countless computer vision applications."
    }
]

data["concept_breakdown"] = [
    {
        "concept": "Residual Mapping",
        "description": "Learning the difference ($F(x)$) between the input and the target output, rather than the target output itself."
    },
    {
        "concept": "Identity Shortcut Connection",
        "description": "A connection that bypasses one or more layers, adding the input of a block directly to its output."
    },
    {
        "concept": "Degradation Problem",
        "description": "The observation that very deep networks often perform worse than shallower ones during training, even when not overfitting."
    },
    {
        "concept": "Bottleneck Design",
        "description": "A residual block variant using 1x1, 3x3, and 1x1 convolutions to reduce computational cost in very deep networks."
    },
    {
        "concept": "Vanishing Gradient",
        "description": "A problem in deep learning where gradients become extremely small during backpropagation, preventing weights from updating; ResNets mitigate this via shortcuts."
    }
]

data["math_equations"] = [
    {
        "name": "Residual Block Output",
        "latex": "y = \\mathcal{F}(x, \\{W_i\\}) + x",
        "explanation": "The output $y$ of a residual block is the sum of the residual function $\\mathcal{F}$ and the original input $x$.",
        "symbols": [
            {"symbol": "x", "meaning": "Input to the residual block"},
            {"symbol": "\\mathcal{F}", "meaning": "The residual function to be learned (e.g., two conv layers)"},
            {"symbol": "W_i", "meaning": "Learned weights of the layers within the block"}
        ]
    }
]

data["figure_explanations"] = [
    {
        "figure_index": 1,
        "explanation": "Diagram of a residual building block showing the weight layers and the identity shortcut connection that performs the element-wise addition."
    },
    {
        "figure_index": 2,
        "explanation": "Comparison of training error on ImageNet for 'plain' networks vs. ResNets, demonstrating how ResNets successfully overcome the degradation problem at increased depths."
    }
]

data["see_also"] = [
    {"topic": "VGG Network", "description": "A classic deep CNN that ResNets improved upon by increasing depth while managing complexity."},
    {"topic": "Inception Architecture", "description": "Another concurrent breakthrough in CNN design that used multi-scale convolutions."},
    {"topic": "Highway Networks", "description": "A precursor to ResNets that used gated shortcut connections."},
    {"topic": "Batch Normalization", "description": "A technique used extensively in ResNets to stabilize training and accelerate convergence."}
]

data["glossary_terms"] = [
    {"term": "Skip Connection", "definition": "A connection in a neural network that skips one or more layers."},
    {"term": "ILSVRC", "definition": "ImageNet Large Scale Visual Recognition Challenge; a premier computer vision competition."},
    {"term": "FLOPs", "definition": "Floating Point Operations; a measure of computational complexity."},
    {"term": "Identity Mapping", "definition": "A function that returns its input unchanged: $f(x) = x$."},
    {"term": "Backpropagation", "definition": "The algorithm used to calculate gradients and update weights in a neural network."}
]

with open(fetch_path, 'w') as f:
    json.dump(data, f, indent=2)
