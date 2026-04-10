import json
import os

paper_id = "0800357049444fb80588f264d68e0c23f9b12a19"
fetch_path = f"/tmp/wiki-gen/{paper_id}.fetch.json"

with open(fetch_path, 'r') as f:
    data = json.load(f)

data["lead_paragraph"] = "Craig Reynolds' 1987 paper, 'Flocks, Herds, and Schools: A Distributed Behavioral Model,' introduced the 'Boids' model, a groundbreaking approach to simulating collective motion in computer graphics. By breaking down complex group behavior into three simple local rules—separation, alignment, and cohesion—Reynolds demonstrated that lifelike aggregate motion could emerge from the interactions of individual agents without a centralized leader. This model revolutionized character animation and found applications across diverse fields, including biological modeling, robotics, and artificial life."

data["main_concept"] = "Boids Model of Collective Motion"

data["infobox_data"] = {
    "architecture_type": "Distributed Agent-Based Model",
    "key_innovation": "Emergent group behavior through simple local steering rules: Separation, Alignment, Cohesion.",
    "performance_metric": "First model to produce lifelike flocking behavior in computer graphics; standard for agent-based simulations.",
    "computational_efficiency": "Localized interactions allow for large-scale simulations with high frame rates."
}

data["sections"] = [
    {
        "title": "The Distributed Behavioral Model",
        "content": "Before Reynolds' work, animating groups of creatures often relied on scripted paths or global controllers, which lacked the organic feel of natural flocks. Reynolds proposed a distributed model where each 'boid' (a simulated bird-like object) makes its own steering decisions based on its immediate neighbors.\n\nThis approach shifts the complexity from the group level to the interaction level, allowing for emergent behaviors that are both dynamic and realistic. The model assumes that each agent has access to limited information about the positions and velocities of nearby boids, rather than a global view of the entire flock."
    },
    {
        "title": "The Three Fundamental Steering Rules",
        "content": "The core of the Boids model consists of three simple steering behaviors that are applied to each agent at every time step:\n\n1. **Separation**: Steer to avoid crowding or colliding with nearby flockmates. This ensures that agents maintain a safe personal space.\n2. **Alignment**: Steer towards the average heading of nearby flockmates. This rule synchronizes the velocity and direction of the group.\n3. **Cohesion**: Steer to move towards the average position (center of mass) of nearby flockmates. This keeps the flock together as a cohesive unit.\n\nTogether, these rules balance the competing needs for individual safety, group synchronization, and collective unity."
    },
    {
        "title": "Neighborhood and Perception",
        "content": "A critical aspect of the Boids model is the concept of a 'neighborhood.' A boid only reacts to flockmates within a certain distance and angle, simulating a natural field of vision and perception. This localization is what makes the model 'distributed' rather than 'centralized.'\n\nIf the neighborhood is too small, the flock may break apart into isolated individuals. If it is too large, the boids may become overwhelmed by distant information, leading to sluggish or unrealistic motion. Modern implementations often use spatial partitioning (like quadtrees or grids) to efficiently identify neighbors in large-scale simulations."
    },
    {
        "title": "Impact on Computer Graphics and Science",
        "content": "The Boids model had an immediate and lasting impact on the field of computer graphics, most notably in the animation of massive battle scenes and wildlife in films like *Batman Returns* and *The Lion King*. Beyond entertainment, the model provided a foundation for the study of self-organizing systems in biology and physics.\n\nIn robotics, the principles of flocking are used to coordinate swarms of autonomous drones and underwater vehicles. In social science, similar models help explain human crowd dynamics and the spread of information through social networks. Reynolds' work remains one of the most cited and influential papers in the history of SIGGRAPH."
    }
]

data["concept_breakdown"] = [
    {
        "concept": "Boid",
        "description": "A simulated bird-like agent that follows local rules to achieve complex group behavior."
    },
    {
        "concept": "Separation",
        "description": "A steering behavior that prevents agents from colliding by applying a repulsive force from nearby neighbors."
    },
    {
        "concept": "Alignment",
        "description": "A steering behavior that matches an agent's velocity with its neighbors, ensuring uniform flock movement."
    },
    {
        "concept": "Cohesion",
        "description": "A steering behavior that pulls agents toward the center of their local neighborhood, maintaining group unity."
    },
    {
        "concept": "Emergence",
        "description": "The process where complex, large-scale patterns arise from the simple, local interactions of individual components."
    }
]

data["math_equations"] = [
    {
        "name": "Steering Force Vector",
        "latex": "\\vec{F}_{steering} = \\vec{v}_{desired} - \\vec{v}_{current}",
        "explanation": "Reynolds defines steering as a force applied to an agent's current velocity to reach a desired target state.",
        "symbols": [
            {"symbol": "\\vec{F}_{steering}", "meaning": "The resulting steering force vector"},
            {"symbol": "\\vec{v}_{desired}", "meaning": "The target velocity according to the flocking rules"},
            {"symbol": "\\vec{v}_{current}", "meaning": "The current velocity of the boid"}
        ]
    },
    {
        "name": "Cohesion Rule (Center of Mass)",
        "latex": "\\vec{C} = \\frac{1}{N} \\sum_{i=1}^{N} \\vec{p}_i",
        "explanation": "The cohesion steering vector is directed toward the average position of all boids within the local neighborhood.",
        "symbols": [
            {"symbol": "\\vec{C}", "meaning": "The center of mass of the local neighborhood"},
            {"symbol": "\\vec{p}_i", "meaning": "The position of the i-th neighbor"},
            {"symbol": "N", "meaning": "The number of neighbors in the perception radius"}
        ]
    }
]

data["figure_explanations"] = [
    {
        "figure_index": 1,
        "explanation": "Visual demonstration of the three boids rules showing how individual force vectors combine to produce complex flocking patterns."
    }
]

data["see_also"] = [
    {"topic": "Particle Systems", "description": "A technique in computer graphics that uses large numbers of small particles to simulate fuzzy phenomena like fire and clouds."},
    {"topic": "Artificial Life", "description": "The study of systems related to life, its processes, and its evolution through simulations using computer models and robotics."},
    {"topic": "Swarm Intelligence", "description": "The collective behavior of decentralized, self-organized systems, typically natural or artificial."},
    {"topic": "Emergent Behavior", "description": "Complex patterns and properties that arise from the interaction of simpler entities."}
]

data["glossary_terms"] = [
    {"term": "Boid", "definition": "A term coined by Craig Reynolds to describe a simulated bird-like agent."},
    {"term": "Separation", "definition": "A steering rule that keeps flockmates from colliding."},
    {"term": "Alignment", "definition": "A steering rule that causes flockmates to face the same direction."},
    {"term": "Cohesion", "definition": "A steering rule that keeps flockmates together by moving toward their center of mass."},
    {"term": "Agent-Based Model", "definition": "A class of computational models for simulating the actions and interactions of autonomous agents."}
]

with open(fetch_path, 'w') as f:
    json.dump(data, f, indent=2)
