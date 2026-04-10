import json
import os

paper_id = "f49101078fb25f714a9813259ece149581017782"
fetch_path = f"/Users/woodj/.gemini/tmp/wiki-gen/{paper_id}.fetch.json"

with open(fetch_path, 'r') as f:
    data = json.load(f)

data["lead_paragraph"] = "Seppo Linnainmaa's 1970 Master's thesis and subsequent 1976 paper, 'Taylor expansion of the accumulated rounding error,' introduced what is now known as reverse-mode automatic differentiation (AD). While originally developed to estimate the rounding errors of numerical algorithms, Linnainmaa's method provided the first general and efficient algorithm for computing the partial derivatives of a composite function. This mathematical breakthrough is the direct algorithmic ancestor of the backpropagation algorithm used to train modern neural networks."

data["main_concept"] = "Reverse-Mode Automatic Differentiation"

data["infobox_data"] = {
    "architecture_type": "Algorithmic Differentiation / Numerical Analysis",
    "key_innovation": "Reverse-mode accumulation of partial derivatives in computational graphs.",
    "performance_metric": "Computational cost of gradients proportional to the cost of the function itself.",
    "computational_efficiency": "O(1) pass for all partial derivatives relative to the function evaluation pass."
}

data["sections"] = [
    {
        "title": "Rounding Error and Taylor Expansion",
        "content": "Linnainmaa's primary goal was to solve a problem in numerical stability: how to quantify the cumulative effect of rounding errors in a long sequence of floating-point operations. He proposed using a first-order Taylor expansion to linearize the error propagation.\n\nBy treating each elementary operation in a program as a node in a computational graph, he realized that the total error could be expressed as a weighted sum of the individual errors introduced at each step. The weights in this sum are the partial derivatives of the final output with respect to the intermediate values."
    },
    {
        "title": "Discovery of Reverse-Mode AD",
        "content": "To compute these weights efficiently, Linnainmaa described an algorithm that traverses the computational graph in reverse order (from output to inputs). This 'reverse pass' allows for the simultaneous calculation of all partial derivatives with a computational complexity that is a small constant multiple of the original function evaluation.\n\nThis was a major improvement over 'forward-mode' differentiation, which requires a separate pass for each input variable. Linnainmaa's method proved that for functions with many inputs and a single output—exactly the case for loss functions in machine learning—gradients could be calculated with incredible efficiency."
    },
    {
        "title": "The Link to Backpropagation",
        "content": "While Linnainmaa did not explicitly apply his method to neural networks, the algorithm he described is identical to the 'backpropagation' algorithm popularized by Rumelhart, Hinton, and Williams in 1986. Linnainmaa's work provided the pure mathematical and algorithmic framework for what would become the engine of the deep learning revolution.\n\nHistorians of AI, such as Jürgen Schmidhuber, have identified Linnainmaa as the originator of the core algorithm, noting that his 1970 thesis was the first to detail the efficient reverse-mode pass for arbitrary differentiable computational graphs."
    },
    {
        "title": "Historical Context and Legacy",
        "content": "Linnainmaa's work was initially published in Finnish in 1970 and later in English in 1976. Due to its focus on numerical analysis and its initial publication language, it remained relatively unknown to the early neural network community.\n\nToday, Linnainmaa is recognized as a pioneer of automatic differentiation. His algorithm is implemented in every major deep learning framework, including TensorFlow and PyTorch, which use reverse-mode AD to compute the gradients necessary for training massive models with billions of parameters."
    }
]

data["concept_breakdown"] = [
    {
        "concept": "Automatic Differentiation (AD)",
        "description": "A set of techniques to numerically evaluate the derivative of a function specified by a computer program."
    },
    {
        "concept": "Reverse Mode",
        "description": "An AD method that computes derivatives by working backward from the output, especially efficient for functions with many parameters."
    },
    {
        "concept": "Computational Graph",
        "description": "A directed graph where nodes represent mathematical operations and edges represent the flow of data."
    },
    {
        "concept": "Partial Derivative",
        "description": "The derivative of a multivariate function with respect to one variable while holding others constant."
    },
    {
        "concept": "Rounding Error",
        "description": "The difference between the result produced by a given algorithm using exact arithmetic and the result produced by the same algorithm using finite-precision floating-point arithmetic."
    }
]

data["math_equations"] = [
    {
        "name": "Error Propagation Weight",
        "latex": "w_i = \\frac{\\partial f}{\\partial x_i}",
        "explanation": "Linnainmaa defined weights $w_i$ as the partial derivatives of the result $f$ with respect to the intermediate value $x_i$, calculated via the chain rule in reverse.",
        "symbols": [
            {"symbol": "f", "meaning": "Final output or result of the computation"},
            {"symbol": "x_i", "meaning": "An intermediate or input variable in the sequence of operations"}
        ]
    },
    {
        "name": "The Chain Rule (Reverse)",
        "latex": "\\delta_i = \\sum_{j \\in \\text{children}(i)} \\delta_j \\frac{\\partial x_j}{\\partial x_i}",
        "explanation": "The fundamental recursive step of reverse-mode AD, where the gradient at node $i$ is the sum of gradients from its dependent nodes $j$, scaled by local derivatives.",
        "symbols": [
            {"symbol": "\\delta_i", "meaning": "The 'adjoint' or gradient of the output with respect to node i"}
        ]
    }
]

data["see_also"] = [
    {"topic": "Backpropagation", "description": "The application of reverse-mode AD to training artificial neural networks."},
    {"topic": "Chain Rule", "description": "The basic rule of calculus that enables automatic differentiation."},
    {"topic": "Numerical Stability", "description": "The property of an algorithm to remain accurate despite rounding errors, which was Linnainmaa's original focus."},
    {"topic": "PyTorch / TensorFlow", "description": "Modern software libraries that rely entirely on the reverse-mode AD algorithm described by Linnainmaa."}
]

data["glossary_terms"] = [
    {"term": "Adjoint", "definition": "In the context of AD, the partial derivative of the final output with respect to an intermediate variable."},
    {"term": "Forward Pass", "definition": "The initial computation of the function's output values."},
    {"term": "Reverse Pass", "definition": "The subsequent computation of derivatives by moving backward through the operation graph."},
    {"term": "Jacobian", "definition": "A matrix of all first-order partial derivatives of a vector-valued function."},
    {"term": "Floating Point", "definition": "A method of representing real numbers that can support a wide range of values but is subject to rounding error."}
]

with open(fetch_path, 'w') as f:
    json.dump(data, f, indent=2)
