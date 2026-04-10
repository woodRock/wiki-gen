import json
import os

paper_id = "bf92c4f6a3c42cafafed18cbd2ae8a85c5cd09b3"
fetch_path = f"/Users/woodj/.gemini/tmp/wiki-gen/{paper_id}.fetch.json"

with open(fetch_path, 'r') as f:
    data = json.load(f)

data["lead_paragraph"] = "This seminal paper establishes standardized empirical equations for fish target strength (TS) at 38 kHz, a critical parameter for converting echo integrator data into fish abundance. By synthesizing in situ measurements from dual-beam, split-beam, and single-beam systems across multiple species, the study provides robust regressions for physoclist (closed swimbladder) and clupeoid (open swimbladder) fishes. These equations, backed by theoretical modeling and caged-fish studies, have become foundational for acoustic biomass estimation in marine science."

data["main_concept"] = "Standard Target Strength Equations for Fisheries Acoustics"

data["infobox_data"] = {
    "architecture_type": "Empirical Regression Analysis (Linearized TS-Length relationship)",
    "key_innovation": "Derivation of universal TS-length equations for different swimbladder types at 38 kHz.",
    "performance_metric": "Regression standard errors typically between 1.0 and 2.5 dB.",
    "computational_efficiency": "Direct application of logarithmic formulas to echosounder data for real-time abundance estimation."
}

data["sections"] = [
    {
        "title": "Echo Integration and Target Strength Fundamentals",
        "content": "Fish target strength is a key quantity in the acoustic assessment of fish abundance. It is essential for expressing echo integrator measurements as quantities of fish. The calibrated output signal from the echosounder is squared and integrated over a defined range interval. The result is proportional to the sum of the backscattering cross sections of the observed scatterers.\n\nTarget Strength (TS) is the logarithmic expression of the backscattering cross section. If individual echoes overlap, the integrator measures the cumulative backscattering cross section, which can then be converted to numbers of fish by dividing by the appropriate mean backscattering cross section."
    },
    {
        "title": "In Situ Measurement Systems",
        "content": "The study reviews three primary methods for determining target strength in the field. The dual-beam system, introduced in 1974, uses two concentric circular beams to compensate for beam pattern loss by observing the ratio of echo strengths. The split-beam system, introduced in 1984, divides the transducer into quadrants and uses phase differences to specify the target direction and compensate for beam pattern.\n\nSingle-beam systems can also be used, though they require a larger number of measurements to solve an integral equation, typically using linearized solutions like the Craig and Forbes method to derive target strength from echo intensity distributions."
    },
    {
        "title": "Physoclist vs. Clupeoid Regression Models",
        "content": "A major biological difference affecting target strength is the swimbladder type. Physoclists, such as cod and pollock, have closed swimbladders and can regulate gas volume for buoyancy. Clupeoids, such as herring and sprat, are physostomes with open swimbladders that lack precise gas regulation.\n\nRegression analysis of in situ data reveals that physoclists exhibit significantly higher target strengths—approximately 4.5 dB more than comparably sized clupeoids. This difference is consistent across different measurement methods and is primarily attributed to the acoustic properties of the different swimbladder morphologies."
    },
    {
        "title": "Validation and Theoretical Consistency",
        "content": "The in situ measurements were validated against 'ex situ' data, including tethered-single-fish measurements, caged-fish studies, and theoretical computations. Theoretical models based on the physical form of the swimbladder yielded results remarkably consistent with empirical observations, determining equations like TS = 20 log L - 66.9 for certain gadoids.\n\nThe convergence of these diverse datasets—distinguished by time, place, and species—provides high confidence in the derived standard equations, despite the inherent variability caused by fish behavior and orientation."
    }
]

data["concept_breakdown"] = [
    {
        "concept": "Target Strength (TS)",
        "description": "A logarithmic measure of the proportion of incident sound energy reflected back to the source by an underwater target, typically a fish."
    },
    {
        "concept": "Physoclistous Fish",
        "description": "Fish with a closed swimbladder (e.g., cod, haddock) that can regulate their buoyancy by producing or resorbing gas, usually resulting in higher acoustic reflectivity."
    },
    {
        "concept": "Clupeoid Fish",
        "description": "Fish with an open swimbladder connected to the alimentary canal (e.g., herring, sprat), which typically results in lower target strengths compared to physoclists."
    },
    {
        "concept": "Dual-Beam System",
        "description": "A method of measuring target strength directly by comparing the echo received on a narrow central beam and a wider concentric beam."
    },
    {
        "concept": "Split-Beam System",
        "description": "An advanced acoustic technique that uses the phase difference between signals received by different quadrants of a transducer to locate a fish and measure its target strength."
    }
]

data["math_equations"] = [
    {
        "name": "Target Strength Definition",
        "latex": "TS = 10 \\log_{10}(\\sigma / 4\\pi)",
        "explanation": "Defines target strength in terms of the backscattering cross-section ($\\sigma$).",
        "symbols": [
            {"symbol": "TS", "meaning": "Target Strength in decibels (dB)"},
            {"symbol": "\\sigma", "meaning": "Backscattering cross-section"}
        ]
    },
    {
        "name": "Physoclist Standard Equation",
        "latex": "TS = 20 \\log_{10}(L) - 67.4",
        "explanation": "Standard empirical regression for physoclistous fish at 38 kHz.",
        "symbols": [
            {"symbol": "L", "meaning": "Mean fish length in centimeters (cm)"}
        ]
    },
    {
        "name": "Clupeoid Standard Equation",
        "latex": "TS = 20 \\log_{10}(L) - 71.9",
        "explanation": "Standard empirical regression for clupeoid fish (herring and sprat) at 38 kHz.",
        "symbols": [
            {"symbol": "L", "meaning": "Mean fish length in centimeters (cm)"}
        ]
    }
]

data["figure_explanations"] = [
    {
        "figure_index": 1,
        "explanation": "Comparison of regression lines for physoclist and clupeoid fishes, showing the distinct 4.5 dB difference in acoustic reflectivity."
    }
]

data["see_also"] = [
    {"topic": "Backscattering Cross-Section", "description": "The equivalent area of a target that would scatter sound equally in all directions."},
    {"topic": "Simrad EK60", "description": "A modern echosounder system that utilizes the split-beam principles established in this paper."},
    {"topic": "Echo Integration", "description": "The mathematical process of summing acoustic returns to estimate the total biomass of fish schools."},
    {"topic": "Swimbladder", "description": "The gas-filled organ in most fish that is responsible for 90% or more of their acoustic backscatter."}
]

data["glossary_terms"] = [
    {"term": "In Situ", "definition": "Measurements taken in the natural environment of the subject, as opposed to controlled laboratory conditions."},
    {"term": "Physoclist", "definition": "A fish with a closed swimbladder organ."},
    {"term": "Clupeoid", "definition": "A member of the fish family Clupeidae, including herrings and sprats."},
    {"term": "Tilt Angle", "definition": "The orientation of a fish's longitudinal axis relative to the horizontal plane."},
    {"term": "38 kHz", "definition": "The standard operational frequency for scientific echosounder surveys of commercial fish stocks."}
]

with open(fetch_path, 'w') as f:
    json.dump(data, f, indent=2)
