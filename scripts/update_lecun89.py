import json
import os

paper_id = "a8e8f3c8d4418c8d62e306538c9c1292635e9d27"
fetch_path = f"/Users/woodj/.gemini/tmp/wiki-gen/{paper_id}.fetch.json"

with open(fetch_path, 'r') as f:
    data = json.load(f)

data["lead_paragraph"] = "Backpropagation Applied to Handwritten Zip Code Recognition is a foundational paper by Yann LeCun and colleagues that demonstrated the practical utility of convolutional neural networks (CNNs) for real-world pattern recognition. By training a multi-layer network directly on raw pixel images of handwritten digits from the U.S. Postal Service, the authors showed that local connection patterns and shared weights could automatically learn shift-invariant features. This work laid the groundwork for modern computer vision and proved that backpropagation could effectively train deep, constrained architectures."

data["main_concept"] = "Convolutional Neural Networks (LeNet-style)"

data["infobox_data"] = {
    "architecture_type": "Convolutional Neural Network (CNN)",
    "key_innovation": "Local receptive fields, shared weights (convolutions), and spatial sub-sampling.",
    "performance_metric": "1% error rate on training data; 9% on difficult zip code testing data.",
    "computational_efficiency": "Significant reduction in parameters compared to fully connected networks due to weight sharing."
}

data["sections"] = [
    {
        "title": "Learning from Raw Pixels",
        "content": "Before this paper, most pattern recognition systems relied on complex, hand-engineered feature extractors followed by a separate classifier. LeCun argued that the feature extractor should be part of the learning process itself.\n\nThe proposed network takes a 16x16 pixel image as input and processes it through several layers of 'feature maps.' Each unit in a feature map is connected to a small local neighborhood in the previous layer, mimicking the receptive fields found in biological visual systems. This ensures that the model captures local spatial correlations before building up to higher-level representations."
    },
    {
        "title": "Weight Sharing and Convolutions",
        "content": "A key innovation introduced in the paper is the concept of weight sharing. All units in a single feature map are constrained to use the same set of weights (a kernel), but applied at different locations. This operation is mathematically equivalent to a discrete convolution.\n\nWeight sharing provides two major benefits: first, it drastically reduces the number of free parameters, making the model easier to train and less prone to overfitting. Second, it naturally implements 'shift invariance,' meaning the network can recognize a digit regardless of its exact position within the input frame."
    },
    {
        "title": "Spatial Sub-sampling",
        "content": "To build robustness against small distortions and variations in the input, the network alternates between convolutional layers and sub-sampling layers. Each sub-sampling unit computes the average of a 2x2 neighborhood in the preceding feature map, then passes it through a non-linear activation.\n\nThis process reduces the spatial resolution of the feature maps while increasing the number of features being tracked. By the time the signal reaches the final fully connected layers, the network has extracted a high-level, low-resolution representation of the digit that is invariant to many common noise factors."
    },
    {
        "title": "Experimental Results on Zip Codes",
        "content": "The authors tested their architecture on a dataset of 9,298 handwritten digits provided by the US Postal Service. The results were highly competitive for the time, achieving a 1% error rate on the training set.\n\nOn a particularly difficult test set of 7,291 digits, the network achieved a 9% error rate. This performance proved that neural networks could handle the 'garbage' and variability found in real-world data, leading to the deployment of similar systems for automated check and mail processing in the 1990s."
    }
]

data["concept_breakdown"] = [
    {
        "concept": "Local Receptive Field",
        "description": "A small region of the input image that a single neuron 'sees' and processes, allowing the model to capture local spatial features."
    },
    {
        "concept": "Weight Sharing",
        "description": "The technique of using the same weights for different neurons in a layer, which defines the convolutional operation and reduces parameter count."
    },
    {
        "concept": "Feature Map",
        "description": "A set of neurons that all detect the same feature (e.g., a vertical edge) but at different locations across the input."
    },
    {
        "concept": "Shift Invariance",
        "description": "The property of a system to recognize a pattern correctly even if its position in the input changes."
    },
    {
        "concept": "Sub-sampling (Pooling)",
        "description": "The process of reducing the resolution of a feature map by aggregating information from local clusters of units."
    }
]

data["math_equations"] = [
    {
        "name": "Unit Activation",
        "latex": "x_j = f(\\sum_i w_{ij} x_i + b_j)",
        "explanation": "The standard neuron activation function where $f$ is a sigmoid-like non-linearity.",
        "symbols": [
            {"symbol": "w_{ij}", "meaning": "Shared weight between unit i and unit j"},
            {"symbol": "b_j", "meaning": "Bias term for unit j"},
            {"symbol": "f", "meaning": "Non-linear activation function (typically tanh in this paper)"}
        ]
    }
]

data["figure_explanations"] = [
    {
        "figure_index": 1,
        "explanation": "Diagram of the multi-layer network architecture, showing the input layer, convolutional layers (H1, H2), sub-sampling layers, and final output."
    }
]

data["see_also"] = [
    {"topic": "LeNet-5", "description": "The more advanced evolution of this architecture that became the standard for digit recognition."},
    {"topic": "Convolutional Neural Network", "description": "The general class of models that this paper helped pioneer."},
    {"topic": "Backpropagation", "description": "The algorithm used to train the network by calculating gradients through the layers."},
    {"topic": "MNIST", "description": "The classic dataset of handwritten digits that was later derived from the USPS data used here."}
]

data["glossary_terms"] = [
    {"term": "Convolution", "definition": "A mathematical operation on two functions that produces a third function expressing how the shape of one is modified by the other."},
    {"term": "Backpropagation", "definition": "A method used in artificial neural networks to calculate a gradient that is needed in the calculation of the weights to be used in the network."},
    {"term": "Sigmoid", "definition": "A mathematical function having a characteristic 'S'-shaped curve."},
    {"term": "Receptive Field", "definition": "The specific region of the sensory space in which a stimulus will modify the firing of that neuron."},
    {"term": "Invariance", "definition": "The property of remaining unchanged regardless of certain transformations, like translation or scaling."}
]

with open(fetch_path, 'w') as f:
    json.dump(data, f, indent=2)
