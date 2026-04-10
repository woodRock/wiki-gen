import json
import os

paper_id = "a6cb366736791bcccc5c8639de5a8f9636bf87e8"
fetch_path = f"/Users/woodj/.gemini/tmp/wiki-gen/{paper_id}.fetch.json"

with open(fetch_path, 'r') as f:
    data = json.load(f)

data["lead_paragraph"] = "Adam (Adaptive Moment Estimation) is an algorithm for first-order gradient-based optimization of stochastic objective functions, based on adaptive estimates of lower-order moments. By combining the advantages of AdaGrad, which works well with sparse gradients, and RMSProp, which works well in online and non-stationary settings, Adam has become the default optimizer for deep learning. Its computational efficiency, low memory requirements, and invariance to diagonal scaling of the gradients make it well-suited for large-scale data and parameter-heavy models."

data["main_concept"] = "Adam Optimization Algorithm"

data["infobox_data"] = {
    "architecture_type": "First-Order Stochastic Optimizer",
    "key_innovation": "Adaptive learning rates for each parameter using estimates of first and second moments of the gradients.",
    "performance_metric": "Faster convergence and lower loss across a wide range of deep learning tasks.",
    "computational_efficiency": "O(1) memory per parameter; computationally efficient with small constant overhead."
}

data["sections"] = [
    {
        "title": "Adaptive Moment Estimation",
        "content": "The Adam algorithm maintains exponentially moving averages of the gradient ($m_t$) and the squared gradient ($v_t$), which represent estimates of the first moment (the mean) and the second raw moment (the uncentered variance) of the gradients, respectively.\n\nTwo hyper-parameters $\\beta_1, \\beta_2 \\in [0, 1)$ control the exponential decay rates of these moving averages. By utilizing both the direction (momentum) and the magnitude (adaptive scaling) of the gradients, Adam can navigate complex loss landscapes more effectively than standard Stochastic Gradient Descent (SGD)."
    },
    {
        "title": "Bias Correction",
        "content": "A unique feature of Adam is the use of initialization bias correction. Since the moving averages $m_t$ and $v_t$ are typically initialized as vectors of zeros, they are biased towards zero, especially during the initial time steps or when the decay rates are small (i.e., $\\beta_1$ and $\\beta_2$ are close to 1).\n\nThe authors derived bias-corrected estimates $\\hat{m}_t$ and $\\hat{v}_t$ to counteract this effect. This correction ensures that the moments are more accurate early in the training process, leading to more stable updates and preventing the algorithm from 'stalling' at the beginning of optimization."
    },
    {
        "title": "Hyper-parameters and Stability",
        "content": "Adam is known for being robust to its hyper-parameters. The default values suggested in the paper—$\\alpha=0.001$, $\\beta_1=0.9$, $\\beta_2=0.999$, and $\\epsilon=10^{-8}$—work well for most deep learning problems.\n\nThe algorithm's update rule is conceptually similar to a 'signal-to-noise ratio' (SNR) where the step size is determined by how much the gradient signal outweighs its uncertainty. This property makes Adam particularly effective for non-stationary objectives and problems with very noisy or sparse gradients."
    },
    {
        "title": "Adam vs. Other Optimizers",
        "content": "The paper compares Adam to other popular optimization methods, including SGD with Nesterov momentum, AdaGrad, and RMSProp. Across experiments on MNIST, CIFAR-10, and various neural network architectures, Adam consistently demonstrated faster convergence and reached lower training loss.\n\nWhile SGD with momentum may sometimes achieve slightly better generalization on certain vision tasks, Adam's ease of use and consistent performance have made it the industry standard for training large-scale models like Transformers and GANs."
    }
]

data["concept_breakdown"] = [
    {
        "concept": "First Moment (m_t)",
        "description": "The exponentially decaying average of past gradients, providing momentum to accelerate descent in the correct direction."
    },
    {
        "concept": "Second Moment (v_t)",
        "description": "The exponentially decaying average of past squared gradients, used to scale the learning rate for each individual parameter."
    },
    {
        "concept": "Bias Correction",
        "description": "A mathematical adjustment made to the moment estimates to compensate for their initialization at zero."
    },
    {
        "concept": "Learning Rate (Alpha)",
        "description": "The step size used for each parameter update, which Adam automatically adjusts based on the moment estimates."
    },
    {
        "concept": "Epsilon",
        "description": "A small constant added to the denominator to prevent division by zero and ensure numerical stability."
    }
]

data["math_equations"] = [
    {
        "name": "Adam Update Rule",
        "latex": "\\theta_t = \\theta_{t-1} - \\alpha \\cdot \\frac{\\hat{m}_t}{\\sqrt{\\hat{v}_t} + \\epsilon}",
        "explanation": "The final parameter update, where the step is proportional to the ratio of the first moment to the square root of the second moment.",
        "symbols": [
            {"symbol": "\\theta_t", "meaning": "Parameters at time step t"},
            {"symbol": "\\alpha", "meaning": "Learning rate / step size"},
            {"symbol": "\\hat{m}_t", "meaning": "Bias-corrected first moment estimate"},
            {"symbol": "\\hat{v}_t", "meaning": "Bias-corrected second moment estimate"}
        ]
    },
    {
        "name": "Moment Estimates",
        "latex": "m_t = \\beta_1 m_{t-1} + (1 - \\beta_1) g_t, \\quad v_t = \\beta_2 v_{t-1} + (1 - \\beta_2) g_t^2",
        "explanation": "Formulas for updating the exponentially moving averages of the gradient ($g_t$) and its square.",
        "symbols": [
            {"symbol": "g_t", "meaning": "Gradient of the objective function at time step t"},
            {"symbol": "\\beta_1, \\beta_2", "meaning": "Decay rates for the first and second moments"}
        ]
    }
]

data["figure_explanations"] = [
    {
        "figure_index": 1,
        "explanation": "Comparison of Adam with other optimizers on the MNIST dataset, showing Adam's faster convergence in terms of training cost."
    },
    {
        "figure_index": 2,
        "explanation": "Evaluation of different optimizers on a multi-layer fully connected network, demonstrating Adam's robustness across different architectures."
    }
]

data["see_also"] = [
    {"topic": "Stochastic Gradient Descent (SGD)", "description": "The fundamental optimization algorithm that Adam improves upon."},
    {"topic": "RMSProp", "description": "An optimizer that also uses adaptive learning rates and served as a major inspiration for Adam."},
    {"topic": "AdaGrad", "description": "An earlier adaptive gradient algorithm that scales the learning rate based on the sum of all past squared gradients."},
    {"topic": "AdamW", "description": "A popular variant of Adam that correctly implements weight decay regularization."}
]

data["glossary_terms"] = [
    {"term": "Momentum", "definition": "A technique that uses previous gradients to smooth out updates and accelerate descent."},
    {"term": "Adaptive Learning Rate", "definition": "A learning rate that is automatically adjusted for each parameter during training."},
    {"term": "Bias", "definition": "A systematic error introduced into an estimate, in this case due to zero-initialization."},
    {"term": "Stochastic", "definition": "Involving random variables or processes; in optimization, this usually means using random subsets of data."},
    {"term": "Gradient", "definition": "The vector of partial derivatives of a function, indicating the direction of steepest ascent."}
]

with open(fetch_path, 'w') as f:
    json.dump(data, f, indent=2)
