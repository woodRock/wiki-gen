import json
import os

paper_id = "052b1d8ce63b07fec3de9dbb583772d860b7c769"
fetch_path = f"/Users/woodj/.gemini/tmp/wiki-gen/{paper_id}.fetch.json"

with open(fetch_path, 'r') as f:
    data = json.load(f)

data["lead_paragraph"] = "Learning representations by back-propagating errors is the seminal 1986 Nature paper that popularized the backpropagation algorithm for training multi-layer neural networks. David Rumelhart, Geoffrey Hinton, and Ronald Williams demonstrated that backpropagation could learn internal representations of data in hidden layers, effectively solving the credit assignment problem that had limited earlier simple perceptrons. This work reignited interest in neural networks and provided the fundamental training mechanism for almost all modern deep learning architectures."

data["main_concept"] = "The Backpropagation Algorithm"

data["infobox_data"] = {
    "architecture_type": "Multi-Layer Feedforward Neural Network",
    "key_innovation": "Efficient gradient descent in hidden layers via the chain rule.",
    "performance_metric": "First successful training of deep 'internal' representations.",
    "computational_efficiency": "Gradient calculation time proportional to the number of weights in the network."
}

data["sections"] = [
    {
        "title": "Solving the Credit Assignment Problem",
        "content": "Before the popularization of backpropagation, neural network research was stymied by the inability to train networks with hidden layers. While the perceptron learning rule could train a single layer, there was no principled way to determine how to adjust the weights of 'hidden' units that did not have a direct target output.\n\nRumelhart and his colleagues applied the chain rule of calculus to show that error signals from the output layer could be propagated backward through the network. This allowed the system to determine exactly how much each hidden weight contributed to the final error, enabling the simultaneous optimization of all parameters in a deep architecture."
    },
    {
        "title": "Learning Internal Representations",
        "content": "The paper's most significant claim is that backpropagation allows a network to discover its own internal representations of the data. To prove this, the authors used several tasks, including the 'family tree' problem and the XOR problem.\n\nIn the family tree task, the network learned to encode abstract concepts like 'generation' and 'branch' in its hidden units, despite never being explicitly told about these relationships. This demonstrated that neural networks were not just simple classifiers, but could develop complex, hierarchical features from raw data—a precursor to the 'deep features' identified in modern CNNs."
    },
    {
        "title": "The Backpropagation Procedure",
        "content": "The backpropagation procedure consists of two main passes. In the **forward pass**, an input vector is processed through the network to produce an output. The difference between this output and the desired target is used to calculate an error (or loss) function.\n\nIn the **backward pass**, the partial derivative of the error with respect to each weight is computed by working from the output layer back to the input. The weights are then adjusted in the direction that most rapidly reduces the error. The authors found that a simple 'momentum' term could be added to speed up learning and help the network navigate narrow valleys in the error surface."
    },
    {
        "title": "Historical Significance",
        "content": "While the core mathematics of backpropagation had been described earlier (e.g., by Linnainmaa and Werbos), it was the 1986 Rumelhart paper that made the algorithm accessible and demonstrated its power on meaningful problems.\n\nThis work ended the first 'AI winter' and established the connectionist paradigm. It provided the empirical evidence that multi-layer networks could learn complex non-linear mappings, laying the foundation for every subsequent breakthrough in deep learning, from AlexNet to modern large language models."
    }
]

data["concept_breakdown"] = [
    {
        "concept": "Hidden Units",
        "description": "Neurons in a network that are neither part of the input nor the output, responsible for learning abstract internal representations."
    },
    {
        "concept": "Error Derivative",
        "description": "The rate at which the network's total error changes with respect to a specific weight or activation."
    },
    {
        "concept": "Generalized Delta Rule",
        "description": "The specific update rule derived in the paper for adjusting weights in multi-layer networks."
    },
    {
        "concept": "Momentum",
        "description": "A technique introduced to accelerate gradient descent by adding a fraction of the previous weight change to the current one."
    },
    {
        "concept": "Connectionism",
        "description": "A movement in cognitive science that models mental phenomena using networks of simple, interconnected units."
    }
]

data["math_equations"] = [
    {
        "name": "Hidden Unit Gradient",
        "latex": "\\frac{\\partial E}{\\partial y_i} = \\sum_j \\frac{\\partial E}{\\partial y_j} \\frac{\\partial y_j}{\\partial y_i}",
        "explanation": "The core recursive step of backpropagation, showing how the error gradient at unit $i$ is derived from the gradients of all units $j$ in the subsequent layer.",
        "symbols": [
            {"symbol": "E", "meaning": "Total error function"},
            {"symbol": "y_i", "meaning": "Output of hidden unit i"}
        ]
    },
    {
        "name": "Weight Update with Momentum",
        "latex": "\\Delta w(t) = -\\eta \\frac{\\partial E}{\\partial w} + \\alpha \\Delta w(t-1)",
        "explanation": "The weight update rule combining the current gradient with a momentum term $\\alpha$ to stabilize learning.",
        "symbols": [
            {"symbol": "\\eta", "meaning": "Learning rate"},
            {"symbol": "\\alpha", "meaning": "Momentum coefficient"}
        ]
    }
]

data["figure_explanations"] = [
    {
        "figure_index": 1,
        "explanation": "Diagram showing a simple three-layer network and how the error signal $\\delta$ is sent backward to calculate weight changes."
    }
]

data["see_also"] = [
    {"topic": "David Rumelhart", "description": "The lead author and a central figure in the development of connectionist models."},
    {"topic": "Geoffrey Hinton", "description": "Co-author and a key architect of the modern deep learning revolution."},
    {"topic": "Perceptrons", "description": "The earlier, single-layer networks that were proven to be limited in their learning capabilities."},
    {"topic": "Stochastic Gradient Descent", "description": "The iterative optimization method that backpropagation enables for deep networks."}
]

data["glossary_terms"] = [
    {"term": "Credit Assignment", "definition": "The problem of determining which components of a system are responsible for its success or failure."},
    {"term": "Delta Rule", "definition": "A gradient descent learning rule for updating the weights of the inputs to artificial neurons."},
    {"term": "Internal Representation", "definition": "How a network encodes information about its environment in its hidden layers."},
    {"term": "Convergence", "definition": "The point at which an optimization algorithm has found a stable solution (usually a local minimum)."},
    {"term": "Non-linearity", "definition": "A mathematical function where the output is not directly proportional to the input, essential for learning complex patterns."}
]

with open(fetch_path, 'w') as f:
    json.dump(data, f, indent=2)
