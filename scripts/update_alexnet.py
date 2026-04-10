import json
import os

paper_id = "abd1c342495432171beb7ca8fd9551ef13cbd0ff"
fetch_path = f"/Users/woodj/.gemini/tmp/wiki-gen/{paper_id}.fetch.json"

with open(fetch_path, 'r') as f:
    data = json.load(f)

data["lead_paragraph"] = "ImageNet Classification with Deep Convolutional Neural Networks, often referred to as AlexNet, is the seminal paper that triggered the modern deep learning revolution. By training a large, deep convolutional neural network on the 1.2 million images of the ImageNet LSVRC-2010 dataset, the authors achieved a top-5 error rate of 15.3%, shattering the previous state-of-the-art of 26.2%. This work demonstrated the power of GPUs for training deep networks and introduced key techniques like ReLU activations and Dropout that are now standard in the field."

data["main_concept"] = "AlexNet Convolutional Neural Network"

data["infobox_data"] = {
    "architecture_type": "Deep Convolutional Neural Network (CNN)",
    "key_innovation": "Large-scale training on GPUs, ReLU activation, and Dropout regularization.",
    "performance_metric": "15.3% top-5 error on ImageNet (winner of ILSVRC 2012).",
    "computational_efficiency": "First major success of multi-GPU training for deep vision models."
}

data["sections"] = [
    {
        "title": "The ILSVRC 2012 Breakthrough",
        "content": "In 2012, the ImageNet Large Scale Visual Recognition Challenge (ILSVRC) provided a benchmark of over 1.2 million images across 1,000 categories. Alex Krizhevsky, Ilya Sutskever, and Geoffrey Hinton entered a deep convolutional neural network that significantly outperformed all other entries, which mostly relied on traditional hand-crafted features and support vector machines.\n\nThis victory marked a paradigm shift in computer vision, proving that end-to-end representation learning from raw pixels was superior to engineered features. The magnitude of the improvement convinced the broader research community of the potential of deep learning."
    },
    {
        "title": "Architecture: Convolutional and Fully Connected Layers",
        "content": "AlexNet consists of eight learned layers: five convolutional layers followed by three fully connected layers. The first convolutional layer filters the 224x224x3 input image with 96 kernels of size 11x11x3. Subsequent layers use smaller kernels (5x5 and 3x3) to capture increasingly complex features.\n\nTo fit the large model into the limited memory of GPUs at the time (3GB NVIDIA GTX 580s), the network was split across two GPUs. Specific layers communicated between GPUs, while others operated independently, a precursor to modern distributed training strategies. [[Figure 2]] details this multi-GPU architecture."
    },
    {
        "title": "Key Innovations: ReLU and Dropout",
        "content": "One of the most important technical contributions of the paper was the use of the Rectified Linear Unit (ReLU) activation function, $f(x) = \\max(0, x)$. Prior to AlexNet, saturating activations like Tanh or Sigmoid were standard, but ReLUs allowed the network to train several times faster by mitigating the vanishing gradient problem.\n\nTo combat overfitting in the large fully-connected layers, the authors employed 'Dropout.' This technique involves randomly setting the output of each hidden neuron to zero with a probability of 0.5 during training. This forces the network to learn more robust, redundant features and is now a fundamental tool for regularizing deep models."
    },
    {
        "title": "Data Augmentation and Overfitting",
        "content": "Despite its depth, AlexNet was prone to overfitting due to its 60 million parameters. The authors used two primary forms of data augmentation to artificially enlarge the dataset: generating image translations and horizontal reflections, and altering the intensities of the RGB channels using PCA-based color augmentation.\n\nThese techniques, combined with Dropout, allowed the model to generalize effectively to unseen images, establishing a template for training large-scale vision models that persists today."
    }
]

data["concept_breakdown"] = [
    {
        "concept": "ReLU (Rectified Linear Unit)",
        "description": "A non-saturating activation function that speeds up training by providing constant gradients for positive inputs."
    },
    {
        "concept": "Dropout",
        "description": "A regularization technique where neurons are randomly ignored during training to prevent co-adaptation and overfitting."
    },
    {
        "concept": "Convolutional Layer",
        "description": "A layer that applies a set of learnable filters to the input to extract spatial features like edges, shapes, and textures."
    },
    {
        "concept": "Data Augmentation",
        "description": "The process of creating new training examples by applying transformations (crops, flips, color shifts) to existing data."
    },
    {
        "concept": "Overlapping Pooling",
        "description": "A technique used in AlexNet where the pooling regions overlap, which the authors found slightly reduced error rates."
    }
]

data["math_equations"] = [
    {
        "name": "ReLU Activation",
        "latex": "f(x) = \\max(0, x)",
        "explanation": "The simple thresholding function that replaced Sigmoid/Tanh and enabled much faster training of deep networks.",
        "symbols": [
            {"symbol": "x", "meaning": "The input to the neuron"},
            {"symbol": "f(x)", "meaning": "The activated output"}
        ]
    },
    {
        "name": "Local Response Normalization (LRN)",
        "latex": "b^i_{x,y} = a^i_{x,y} / \\left(k + \\alpha \\sum_{j=\\max(0, i-n/2)}^{\\min(N-1, i+n/2)} (a^j_{x,y})^2\\right)^\\beta",
        "explanation": "A normalization scheme used in AlexNet to encourage 'lateral inhibition' between feature maps (though it has mostly been replaced by Batch Normalization today).",
        "symbols": [
            {"symbol": "a^i_{x,y}", "meaning": "Activity of a neuron computed by applying kernel i at (x,y)"},
            {"symbol": "b^i_{x,y}", "meaning": "The response-normalized activity"}
        ]
    }
]

data["figure_explanations"] = [
    {
        "figure_index": 2,
        "explanation": "Detailed diagram of the AlexNet architecture, showing the split between two GPUs and the progression from convolutional to fully connected layers."
    },
    {
        "figure_index": 3,
        "explanation": "Visualization of the 96 convolutional kernels learned by the first layer, showing that the model successfully learned to detect edges and color blobs."
    }
]

data["see_also"] = [
    {"topic": "ImageNet", "description": "The massive visual database that made the training of AlexNet possible."},
    {"topic": "LeNet-5", "description": "An earlier CNN architecture for digit recognition that served as a foundation for AlexNet."},
    {"topic": "VGGNet", "description": "A successor to AlexNet that increased depth and used smaller 3x3 kernels throughout."},
    {"topic": "GPU Computing", "description": "The technology that enables parallel processing of neural network operations, critical for AlexNet's success."}
]

data["glossary_terms"] = [
    {"term": "CNN", "definition": "Convolutional Neural Network; a type of deep neural network most commonly applied to analyzing visual imagery."},
    {"term": "Overfitting", "definition": "When a model learns the training data too well, including its noise, and fails to generalize to new data."},
    {"term": "Kernel", "definition": "A small matrix of weights used in a convolutional layer to extract features from an image."},
    {"term": "Top-5 Error", "definition": "The percentage of test images where the correct label is not among the model's top five predictions."},
    {"term": "Max Pooling", "definition": "A sample-based discretization process that down-samples an input representation by taking the maximum value over a window."}
]

with open(fetch_path, 'w') as f:
    json.dump(data, f, indent=2)
