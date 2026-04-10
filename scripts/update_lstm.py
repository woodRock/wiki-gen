import json
import os

paper_id = "2e9d221c206e9503ceb452302d68d10e293f2a10"
fetch_path = f"/Users/woodj/.gemini/tmp/wiki-gen/{paper_id}.fetch.json"

with open(fetch_path, 'r') as f:
    data = json.load(f)

data["lead_paragraph"] = "Long Short-Term Memory (LSTM) is a landmark recurrent neural network (RNN) architecture designed to overcome the vanishing gradient problem, enabling the learning of long-range dependencies in sequential data. By introducing a novel 'constant error carousel' (CEC) and a system of gating units, LSTM allows gradients to flow through time without decaying or exploding. This architecture revolutionized sequence modeling and served as the state-of-the-art for tasks like speech recognition, translation, and handwriting synthesis for over two decades."

data["main_concept"] = "Long Short-Term Memory (LSTM)"

data["infobox_data"] = {
    "architecture_type": "Gated Recurrent Neural Network",
    "key_innovation": "Constant Error Carousel (CEC) and gating mechanisms (Input, Output, Forget gates).",
    "performance_metric": "Ability to learn dependencies over 1000+ time steps where standard RNNs fail.",
    "computational_efficiency": "O(1) per time step and parameter; local in space and time."
}

data["sections"] = [
    {
        "title": "The Vanishing Gradient Problem",
        "content": "Before LSTM, training Recurrent Neural Networks (RNNs) on long sequences was notoriously difficult. As gradients are backpropagated through time, they are repeatedly multiplied by the weights of the recurrent connections. If these weights are small, the gradient vanishes exponentially, making it impossible for the network to learn long-term dependencies.\n\nHochreiter and Schmidhuber identified this fundamental flaw and proposed a structural solution: a memory cell that can maintain its state over long periods. This led to the creation of the LSTM, which uses a linear unit with a fixed self-connection of weight 1.0, ensuring that the error signal remains constant as it flows back through time."
    },
    {
        "title": "The Memory Cell and Gating Mechanism",
        "content": "The core of the LSTM is the memory cell, which acts as a storage unit for information. Access to this cell is controlled by three specialized 'gates':\n\n1. **Input Gate**: Decides which new information from the current input and previous hidden state should be stored in the memory cell.\n2. **Forget Gate**: (Added in later versions, but conceptualized here) Determines which information is no longer relevant and should be discarded from the cell.\n3. **Output Gate**: Controls which part of the current memory cell state should be used to calculate the hidden state and output of the network.\n\nThese gates are themselves neural networks with sigmoid activations, allowing the LSTM to learn to selectively remember or forget information based on the context of the sequence."
    },
    {
        "title": "Constant Error Carousel (CEC)",
        "content": "The CEC is the theoretical heart of the LSTM. It refers to the linear unit within the memory cell that has a self-recurrent connection with a fixed weight of 1. By avoiding the non-linear activations typically found in RNN recurrent loops, the CEC prevents the gradient from being squashed or blown up during backpropagation.\n\nThis 'carousel' allows error signals to circulate indefinitely, effectively bridging the gap between distant events in a sequence. The gating units act as the 'doors' to this carousel, ensuring that it is only updated with meaningful data and only influences the output when necessary."
    },
    {
        "title": "Impact on Deep Learning",
        "content": "The introduction of LSTM was a turning point for artificial intelligence. It proved that neural networks could handle complex, real-world temporal data. For many years, LSTMs were the backbone of major commercial AI systems, including Google's speech recognition and Apple's Siri.\n\nWhile Transformers have largely superseded LSTMs for many large-scale language tasks due to their parallelization capabilities, the principles of gating and residual-like connections (found in the CEC) remain central to modern deep learning architecture design."
    }
]

data["concept_breakdown"] = [
    {
        "concept": "Memory Cell",
        "description": "A container that holds information over time, protected by gating units to maintain long-term dependencies."
    },
    {
        "concept": "Gating",
        "description": "The use of multiplicative units to regulate the flow of information into, out of, and within the memory cell."
    },
    {
        "concept": "Vanishing Gradient",
        "description": "The tendency of gradients to become zero during backpropagation in deep or recurrent networks, which LSTM prevents."
    },
    {
        "concept": "CEC",
        "description": "Constant Error Carousel; the linear internal state of an LSTM cell that preserves the gradient signal over time."
    },
    {
        "concept": "Backpropagation Through Time (BPTT)",
        "description": "The algorithm used to train recurrent networks by unfolding them into a deep feed-forward network."
    }
]

data["math_equations"] = [
    {
        "name": "Cell State Update",
        "latex": "c_t = f_t \\odot c_{t-1} + i_t \\odot \\tilde{c}_t",
        "explanation": "The current cell state $c_t$ is a combination of the previous state (filtered by the forget gate $f_t$) and the new candidate state (filtered by the input gate $i_t$).",
        "symbols": [
            {"symbol": "c_t", "meaning": "Memory cell state at time t"},
            {"symbol": "f_t, i_t", "meaning": "Forget and Input gate activations"},
            {"symbol": "\\tilde{c}_t", "meaning": "Candidate values for the memory cell"}
        ]
    }
]

data["see_also"] = [
    {"topic": "Recurrent Neural Network (RNN)", "description": "The broader class of neural networks that LSTM belongs to."},
    {"topic": "Gated Recurrent Unit (GRU)", "description": "A simplified version of LSTM that combines the input and forget gates."},
    {"topic": "Vanishing Gradient Problem", "description": "The core optimization challenge that LSTM was designed to solve."},
    {"topic": "Transformer", "description": "The current dominant architecture for sequence modeling that evolved from many of the same concepts."}
]

data["glossary_terms"] = [
    {"term": "CEC", "definition": "Constant Error Carousel; the mechanism that prevents gradient decay in LSTMs."},
    {"term": "Gate", "definition": "A multiplicative unit that controls information flow."},
    {"term": "Cell State", "definition": "The internal 'memory' of an LSTM unit."},
    {"term": "Recurrent", "definition": "Having a connection that loops back to an earlier stage or time step."},
    {"term": "Sigmoid", "definition": "An S-shaped activation function used in gates to squash values between 0 and 1."}
]

with open(fetch_path, 'w') as f:
    json.dump(data, f, indent=2)
