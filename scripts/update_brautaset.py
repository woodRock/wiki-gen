import json
import os

paper_id = "212113693909cb7369ff6c5ac19705fd41bdfbe5"
fetch_path = f"/Users/woodj/.gemini/tmp/wiki-gen/{paper_id}.fetch.json"

with open(fetch_path, 'r') as f:
    data = json.load(f)

data["lead_paragraph"] = "This paper introduces a deep learning strategy for automated acoustic target classification in multifrequency echosounder data using a convolutional neural network (CNN) based on the U-Net architecture. By learning spatial and frequency features directly from raw data, the method addresses the limitations of manual species identification and predefined feature extraction in acoustic trawl surveys. Tested on over a decade of Norwegian sandeel survey data, the model achieved an F1 score of 0.87 in distinguishing sandeel schools from other species and background, significantly outperforming traditional school classification algorithms."

data["main_concept"] = "U-Net for Acoustic Target Classification"

data["infobox_data"] = {
    "architecture_type": "Modified U-Net (Encoder-Decoder with Skip Connections)",
    "key_innovation": "End-to-end automatic feature learning from multifrequency (18, 38, 120, 200 kHz) echograms.",
    "performance_metric": "F1 score of 0.87 (overall) and 0.94 (sandeel vs. other schools).",
    "computational_efficiency": "Pixel-wise segmentation allowing for variable input sizes and efficient processing of large survey datasets."
}

data["sections"] = [
    {
        "title": "Multifrequency Acoustic Data Preprocessing",
        "content": "Acoustic trawl surveys utilize echosounders to record backscattered soundwaves, which are essential for estimating fish abundance. In this study, data from four standard frequencies (18, 38, 120, and 200 kHz) were collected during the Norwegian sandeel surveys between 2007 and 2018. To ensure consistency across different vessel settings, the data were interpolated into a common time-range grid based on the 200-kHz resolution.\n\nThis preprocessing transforms the volume backscattering coefficient (sv) values into a four-channel 'image,' where each pixel represents a specific depth and time coordinate across the four frequencies. Missing pings were detected and filled with zero-intensity values (mapped to -75 dB) to maintain the temporal integrity of the echograms.\n\nThe resulting dataset allows the convolutional neural network to treat multifrequency echosounder data similarly to a multispectral image, enabling the simultaneous analysis of frequency response and morphological features of fish schools. [[Figure 1]] shows how these channels are combined.",
        "figure_index": 1
    },
    {
        "title": "U-Net Architecture for Echosounder Segmentation",
        "content": "The researchers employed a modified U-Net architecture, a type of fully convolutional network (FCN) consisting of an encoder and a decoder. The encoder path maps the input image to a low-resolution representation, capturing high-level abstract features, while the decoder path recovers the spatial resolution to produce a pixel-wise classification map.\n\nA defining feature of the U-Net is the use of skip connections between corresponding layers of the encoder and decoder. These connections allow the network to pass high-resolution spatial information directly to the decoding stages, which is critical for the precise localization of small or irregularly shaped fish schools within the water column. [[Figure 4]] illustrates the overall architecture.\n\nContrary to the original U-Net, batch normalization layers were inserted between each convolutional layer and its activation function. This modification helps stabilize the training process by reducing internal covariate shift, leading to faster convergence and better generalization on unseen survey data.",
        "figure_index": 4
    },
    {
        "title": "Balanced Sampling and Handling Class Imbalance",
        "content": "A major challenge in training deep learning models for acoustic surveys is the extreme class imbalance; in the sandeel dataset, approximately 99.8% of pixels were classified as background, with only 0.1% each for sandeel and other fish species. To address this, the study implemented a balanced sampling strategy during training.\n\nRandom 256x256 pixel crops were drawn from the echograms with specific probabilities to ensure the network was exposed to enough instances of fish schools and the seabed. This prevented the model from defaulting to a 'background-only' prediction and helped it learn the specific features of rare classes.\n\nAdditionally, a weighted cross-entropy loss function was used, assigning higher penalties to misclassifications of sandeel and other fish species compared to background pixels. This further incentivized the network to prioritize the accurate identification of fish schools over the dominant background class."
    },
    {
        "title": "Performance and Comparison with Traditional Methods",
        "content": "The performance of the U-Net model was evaluated against a traditional automated processing pipeline (the Korona pipeline in LSSS). The U-Net achieved an overall F1 score of 0.87 on the test set, while the benchmark method obtained a significantly lower F1 score of 0.77.\n\nSpecifically, the network demonstrated high accuracy in separating sandeel schools from schools of other species, achieving an F1 score of 0.94. This indicates that the deep learning approach successfully captured the distinct multifrequency signatures and morphological differences between species. [[Figure 6]] shows the precision-recall curves across different years.\n\nThe results show that the automated deep learning strategy is more robust than traditional threshold-based school detection algorithms, particularly in complex environments where fish schools are located close to the seabed or among other biological noise.",
        "figure_index": 6
    }
]

data["concept_breakdown"] = [
    {
        "concept": "U-Net Encoder-Decoder",
        "description": "A symmetrical neural network architecture where the encoder compresses input data into abstract features and the decoder reconstructs it into a high-resolution classification map."
    },
    {
        "concept": "Skip Connections",
        "description": "Connections that relay low-level spatial features from the encoder to the decoder, ensuring that fine details lost during compression are preserved for accurate pixel-wise labeling."
    },
    {
        "concept": "Multifrequency Interpolation",
        "description": "The process of aligning acoustic data from multiple frequencies onto a single coordinate grid, allowing them to be processed as multiple channels of a single image."
    },
    {
        "concept": "Weighted Cross Entropy",
        "description": "A variant of the standard loss function that adjusts for class imbalance by assigning different importance to errors based on the frequency of the class in the training data."
    },
    {
        "concept": "Morphological Closing",
        "description": "A binary image processing operation used to fill small gaps in manual annotations, creating more continuous and accurate training labels for the fish schools."
    }
]

data["math_equations"] = [
    {
        "name": "F1 Score",
        "latex": "F1 = 2 \\cdot \\frac{\\text{precision} \\cdot \\text{recall}}{\\text{precision} + \\text{recall}}",
        "explanation": "The F1 score is the harmonic mean of precision and recall, providing a single metric to evaluate the balance between false positives and false negatives.",
        "symbols": [
            {"symbol": "\\text{precision}", "meaning": "Proportion of predicted positives that are correct"},
            {"symbol": "\\text{recall}", "meaning": "Proportion of actual positives that are correctly identified"}
        ]
    },
    {
        "name": "Weighted Cross-Entropy Loss",
        "latex": "L = -\\sum_{c=1}^{C} w_c y_c \\log(\\hat{y}_c)",
        "explanation": "A loss function used to train classifiers on imbalanced data by weighting the penalty for misclassifying rare classes higher than common ones.",
        "symbols": [
            {"symbol": "w_c", "meaning": "Weight assigned to class c"},
            {"symbol": "y_c", "meaning": "True label for class c (one-hot encoded)"},
            {"symbol": "\\hat{y}_c", "meaning": "Predicted probability for class c"}
        ]
    },
    {
        "name": "Area-Backscattering Coefficient",
        "latex": "s_a = \\int_{z_1}^{z_2} s_v dz",
        "explanation": "The area-backscattering coefficient ($s_a$), calculated by integrating the volume backscattering coefficient ($s_v$) over a depth range, used to estimate fish biomass.",
        "symbols": [
            {"symbol": "s_a", "meaning": "Area-backscattering coefficient"},
            {"symbol": "s_v", "meaning": "Volume backscattering coefficient"},
            {"symbol": "dz", "meaning": "Change in depth"}
        ]
    }
]

data["figure_explanations"] = [
    {
        "figure_index": 1,
        "explanation": "Comparison of four frequency echograms (18, 38, 120, 200 kHz) alongside manual annotations and model predictions, demonstrating the network's effectiveness in segmenting sandeel schools."
    },
    {
        "figure_index": 2,
        "explanation": "Illustration of how manual bounding box annotations are refined using intensity thresholds and morphological operations to create high-quality training labels."
    },
    {
        "figure_index": 4,
        "explanation": "The modified U-Net architecture diagram, showing the input of 4x256x256 crops, the contracting encoder path, the bottleneck with 1024 features, and the expanding decoder path with skip connections."
    },
    {
        "figure_index": 6,
        "explanation": "Precision-recall curves for sandeel classification across different survey years, showing the consistency of the model's performance on various datasets."
    }
]

data["see_also"] = [
    {"topic": "Simrad EK60", "description": "The scientific echosounder system used to collect the multifrequency data analyzed in this paper."},
    {"topic": "Large Scale Survey System (LSSS)", "description": "The software used for manual processing and annotation of the acoustic survey data."},
    {"topic": "Ammodytes marinus", "description": "The specific species of sandeel that was the focus of the Norwegian acoustic surveys."},
    {"topic": "Convolutional Neural Network", "description": "The class of deep learning models that forms the basis of the U-Net architecture used in this study."}
]

data["glossary_terms"] = [
    {"term": "Echogram", "definition": "A visual representation of underwater acoustic returns, with intensity shown over time (horizontal) and depth (vertical)."},
    {"term": "Backscattering", "definition": "The reflection of acoustic waves back towards the source after hitting a target like a fish or the seabed."},
    {"term": "Pixel-wise Segmentation", "definition": "The process of assigning a specific category label to every individual pixel in an image or data grid."},
    {"term": "Sandeel", "definition": "A small, swim-bladder-less fish that often burrows in the seabed and forms dense schools in the water column."},
    {"term": "Internal Covariate Shift", "definition": "The change in the distribution of network activations due to the update of parameters during training, addressed by batch normalization."}
]

with open(fetch_path, 'w') as f:
    json.dump(data, f, indent=2)
