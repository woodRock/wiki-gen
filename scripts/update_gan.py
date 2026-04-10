import json
import os

paper_id = "86ee1835a56722b76564119437070782fc90eb19"
fetch_path = f"/Users/woodj/.gemini/tmp/wiki-gen/{paper_id}.fetch.json"

with open(fetch_path, 'r') as f:
    data = json.load(f)

data["lead_paragraph"] = "Generative Adversarial Nets (GANs) introduced a novel framework for estimating generative models via an adversarial process. By simultaneously training two models—a generator that captures the data distribution and a discriminator that estimates the probability that a sample came from the training data rather than the generator—this approach avoids the need for Markov chains or unrolling approximate inference networks. The resulting minimax game leads to a powerful method for generating high-quality, realistic data samples, which has since transformed the field of generative modeling."

data["main_concept"] = "Generative Adversarial Networks (GANs)"

data["infobox_data"] = {
    "architecture_type": "Adversarial Generative Framework",
    "key_innovation": "Minimax game between a Generator and a Discriminator.",
    "performance_metric": "Ability to generate sharp, realistic samples without explicit density estimation.",
    "computational_efficiency": "Backpropagation-based training; no need for complex sampling during training."
}

data["sections"] = [
    {
        "title": "The Adversarial Framework",
        "content": "The core idea of GANs is to frame generative modeling as a competition between two players. The **Generator ($G$)** takes a random noise vector as input and attempts to map it to the data space (e.g., an image). Its goal is to produce samples so realistic that they are indistinguishable from real training data.\n\nThe **Discriminator ($D$)** is a binary classifier that takes an input and outputs the probability that it came from the real dataset rather than from $G$. During training, $D$ is optimized to correctly label real and fake samples, while $G$ is optimized to maximize the probability of $D$ making a mistake. This competition drives both models to improve until $G$ produces highly realistic samples."
    },
    {
        "title": "The Minimax Objective Function",
        "content": "The training process is defined by a value function $V(D, G)$, which represents a minimax game. $D$ tries to maximize the log-likelihood of correctly identifying real and fake data, while $G$ tries to minimize the log-probability that $D$ identifies its samples as fake.\n\nIn practice, especially early in training, the generator may be so poor that the discriminator can reject samples with high confidence. To address this, the authors suggest a non-saturating objective for the generator: instead of minimizing $\\log(1 - D(G(z)))$, the generator can be trained to maximize $\\log D(G(z))$. This provides stronger gradients for the generator when its performance is low."
    },
    {
        "title": "Theoretical Convergence",
        "content": "The paper provides a theoretical proof that if $G$ and $D$ have enough capacity, there exists a unique solution where $G$ perfectly recovers the data distribution and $D$ is equal to $1/2$ everywhere (meaning it can no longer distinguish between real and fake samples).\n\nThis equilibrium point corresponds to the global minimum of the Jensen-Shannon divergence between the model's distribution and the true data distribution. While reaching this global optimum is challenging in practice due to the non-convex nature of neural network optimization, the framework provides a solid mathematical foundation for adversarial training."
    },
    {
        "title": "Advantages and Limitations",
        "content": "GANs offer several advantages over previous generative models like Boltzmann machines or Variational Autoencoders (VAEs). They do not require an explicit probability density function, avoiding the need for complex approximate inference or Markov chain sampling. Furthermore, they tend to produce sharper, more detailed images compared to the often-blurry outputs of VAEs.\n\nHowever, GANs are notoriously difficult to train. Issues such as 'mode collapse' (where the generator produces a limited variety of samples) and training instability require careful hyperparameter tuning and architectural choices. Despite these challenges, the GAN framework has inspired thousands of variations and applications in art, science, and industry."
    }
]

data["concept_breakdown"] = [
    {
        "concept": "Generator (G)",
        "description": "A neural network that learns to create fake data from a latent noise vector, aiming to mimic the real data distribution."
    },
    {
        "concept": "Discriminator (D)",
        "description": "A neural network that acts as a judge, learning to distinguish between real data and the fake data produced by the generator."
    },
    {
        "concept": "Minimax Game",
        "description": "A mathematical framework where one player tries to maximize their gain while the other tries to minimize it, leading to a competitive equilibrium."
    },
    {
        "concept": "Jensen-Shannon Divergence",
        "description": "A measure of similarity between two probability distributions, which the GAN objective implicitly minimizes."
    },
    {
        "concept": "Latent Space",
        "description": "The low-dimensional space of random noise (z) that serves as the input to the generator."
    }
]

data["math_equations"] = [
    {
        "name": "Minimax Value Function",
        "latex": "\\min_G \\max_D V(D, G) = \\mathbb{E}_{x \\sim p_{data}(x)}[\\log D(x)] + \\mathbb{E}_{z \\sim p_z(z)}[\\log(1 - D(G(z)))]",
        "explanation": "The fundamental objective of GANs, where the discriminator $D$ maximizes its ability to classify real/fake, and the generator $G$ minimizes the probability of being caught.",
        "symbols": [
            {"symbol": "D(x)", "meaning": "Discriminator's probability that real sample x is real"},
            {"symbol": "G(z)", "meaning": "Generator's output for noise vector z"},
            {"symbol": "D(G(z))", "meaning": "Discriminator's probability that generated sample G(z) is real"}
        ]
    }
]

data["figure_explanations"] = [
    {
        "figure_index": 1,
        "explanation": "Visual representation of the adversarial training process, showing how the generator's distribution (green) eventually aligns with the data distribution (black) as the discriminator (blue) reaches an equilibrium of 0.5."
    }
]

data["see_also"] = [
    {"topic": "Variational Autoencoder (VAE)", "description": "A different class of generative models based on probabilistic graphical models and approximate inference."},
    {"topic": "Deep Convolutional GAN (DCGAN)", "description": "An influential extension of the original GAN that used convolutional layers for more stable image generation."},
    {"topic": "Mode Collapse", "description": "A common failure mode in GAN training where the generator only learns to produce a few types of samples."},
    {"topic": "Wasserstein GAN (WGAN)", "description": "A variant that uses the Earth Mover's distance to improve training stability and avoid vanishing gradients."}
]

data["glossary_terms"] = [
    {"term": "Adversarial", "definition": "A setting involving two competing agents with opposing goals."},
    {"term": "Mode Collapse", "definition": "When a generative model maps many different inputs to the same output, losing diversity in its samples."},
    {"term": "Heuristic", "definition": "A practical approach to problem-solving that may not be optimal but is sufficient for the immediate goal."},
    {"term": "Equilibrium", "definition": "A state in a game where no player can improve their outcome by changing their strategy alone."},
    {"term": "Probability Density", "definition": "A function that describes the relative likelihood of a random variable taking on a given value."}
]

with open(fetch_path, 'w') as f:
    json.dump(data, f, indent=2)
