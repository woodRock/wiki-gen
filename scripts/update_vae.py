import json
import os

paper_id = "5f5dc5b9a2ba710937e2c413b37b053cd673df02"
fetch_path = f"/Users/woodj/.gemini/tmp/wiki-gen/{paper_id}.fetch.json"

with open(fetch_path, 'r') as f:
    data = json.load(f)

data["lead_paragraph"] = "Auto-Encoding Variational Bayes introduced the Variational Autoencoder (VAE), a powerful generative model that combines the principles of Bayesian inference with deep learning. By introducing the 'reparameterization trick,' the authors enabled the efficient training of directed probabilistic graphical models with continuous latent variables using standard backpropagation. This work provided a scalable solution for approximate inference in complex datasets, leading to significant advancements in manifold learning and generative modeling."

data["main_concept"] = "Variational Autoencoders (VAEs)"

data["infobox_data"] = {
    "architecture_type": "Stochastic Variational Inference / Autoencoder",
    "key_innovation": "Reparameterization trick for backpropagating through stochastic nodes.",
    "performance_metric": "Efficient approximation of the Evidence Lower Bound (ELBO).",
    "computational_efficiency": "Scales to large datasets using Stochastic Gradient Variational Bayes (SGVB)."
}

data["sections"] = [
    {
        "title": "Approximate Inference and the ELBO",
        "content": "A fundamental problem in Bayesian statistics is the intractability of the posterior distribution $p(z|x)$ for complex models. The authors propose using a recognition model $q_\\phi(z|x)$—an encoder—to approximate this true posterior.\n\nThe training objective is to maximize the Evidence Lower Bound (ELBO), which balances the reconstruction quality of the data with the similarity of the approximate posterior to a prior distribution (typically a standard Gaussian). This ensures that the latent space is well-structured and can be sampled to generate new data."
    },
    {
        "title": "The Reparameterization Trick",
        "content": "The most significant technical hurdle in training VAEs is that backpropagation cannot flow through random sampling operations. If we sample $z$ directly from $q_\\phi(z|x)$, the gradient with respect to the encoder parameters $\\phi$ is not well-defined.\n\nThe authors solve this with the **reparameterization trick**. Instead of sampling $z$ directly, they express $z$ as a deterministic transformation of an auxiliary noise variable $\\epsilon$: $z = \\mu + \\sigma \\odot \\epsilon$, where $\\epsilon \\sim \\mathcal{N}(0, I)$. This moves the stochasticity into an input branch, allowing gradients to flow through $\\mu$ and $\\sigma$ to the encoder."
    },
    {
        "title": "SGVB Estimator and AEVB Algorithm",
        "content": "The paper introduces the Stochastic Gradient Variational Bayes (SGVB) estimator, which provides a way to compute gradients of the ELBO using mini-batches of data. By applying the reparameterization trick, the ELBO becomes differentiable, enabling the use of standard stochastic gradient ascent algorithms like Adam.\n\nThe Auto-Encoding Variational Bayes (AEVB) algorithm is the practical implementation of this framework, where the encoder and decoder (generative model) are neural networks trained jointly to minimize the total loss (reconstruction error plus KL divergence)."
    },
    {
        "title": "Comparison with Traditional Methods",
        "content": "Before VAEs, approximate inference often relied on computationally expensive methods like Mean Field Variational Inference or Markov Chain Monte Carlo (MCMC). These methods struggle to scale to the large, high-dimensional datasets common in modern machine learning.\n\nVAEs demonstrated superior performance in manifold learning and image generation, producing smooth latent representations where nearby points in $z$-space correspond to similar data points in $x$-space. While GANs often produce sharper images, VAEs offer a more stable training process and a principled probabilistic framework."
    }
]

data["concept_breakdown"] = [
    {
        "concept": "Encoder (Recognition Model)",
        "description": "A neural network that maps input data $x$ to the parameters of a latent distribution (mean and variance)."
    },
    {
        "concept": "Decoder (Generative Model)",
        "description": "A neural network that takes a sample from the latent space $z$ and attempts to reconstruct the original input $x$."
    },
    {
        "concept": "Reparameterization Trick",
        "description": "A method to rewrite a random variable so that it becomes differentiable with respect to its distribution's parameters."
    },
    {
        "concept": "KL Divergence",
        "description": "A mathematical measure of the difference between two probability distributions, used in VAEs to regularize the latent space."
    },
    {
        "concept": "ELBO",
        "description": "Evidence Lower Bound; the objective function that VAEs maximize to train both the encoder and decoder."
    }
]

data["math_equations"] = [
    {
        "name": "Reparameterization Trick",
        "latex": "z = \\mu + \\sigma \\odot \\epsilon, \\quad \\epsilon \\sim \\mathcal{N}(0, I)",
        "explanation": "Allows the model to sample from a distribution while remaining differentiable.",
        "symbols": [
            {"symbol": "\\mu", "meaning": "Learned mean of the latent distribution"},
            {"symbol": "\\sigma", "meaning": "Learned standard deviation"},
            {"symbol": "\\epsilon", "meaning": "Random noise from a standard normal distribution"}
        ]
    },
    {
        "name": "The ELBO Objective",
        "latex": "\\mathcal{L}(\\theta, \\phi; x^{(i)}) = -D_{KL}(q_\\phi(z|x^{(i)}) || p_\\theta(z)) + \\mathbb{E}_{q_\\phi(z|x^{(i)})}[\\log p_\\theta(x^{(i)}|z)]",
        "explanation": "The loss function combining the KL divergence (regularization) and the expected log-likelihood (reconstruction).",
        "symbols": [
            {"symbol": "D_{KL}", "meaning": "Kullback-Leibler divergence"},
            {"symbol": "q_\\phi", "meaning": "The encoder (recognition) model"},
            {"symbol": "p_\\theta", "meaning": "The decoder (generative) model"}
        ]
    }
]

data["figure_explanations"] = [
    {
        "figure_index": 1,
        "explanation": "Illustration of the reparameterization trick, showing how the stochastic sampling node is 'moved' to allow gradients to flow back to the encoder."
    },
    {
        "figure_index": 2,
        "explanation": "Comparison of different estimators for the variational lower bound, showing the efficiency of the SGVB estimator."
    }
]

data["see_also"] = [
    {"topic": "Autoencoder", "description": "The deterministic foundation that VAEs build upon with probabilistic principles."},
    {"topic": "Bayesian Inference", "description": "The statistical framework for updating beliefs in the face of new evidence, which VAEs approximate."},
    {"topic": "Diffusion Models", "description": "A more recent class of generative models that share some probabilistic foundations with VAEs."},
    {"topic": "Normalizing Flows", "description": "A technique for creating more complex and flexible approximate posterior distributions."}
]

data["glossary_terms"] = [
    {"term": "Latent Variable", "definition": "A variable that is not directly observed but is inferred from other variables."},
    {"term": "Intractable", "definition": "Impossible to compute or solve in a reasonable amount of time."},
    {"term": "Posterior", "definition": "The probability distribution of a latent variable given the observed data."},
    {"term": "Prior", "definition": "The probability distribution representing initial beliefs before seeing the data."},
    {"term": "Stochastic", "definition": "Involving a random variable; having a random probability distribution."}
]

with open(fetch_path, 'w') as f:
    json.dump(data, f, indent=2)
