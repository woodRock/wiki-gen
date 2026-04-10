import json
import os

paper_id = "c761c14ce3874fb4134180f68904f1710106ca8b"
fetch_path = f"/Users/woodj/.gemini/tmp/wiki-gen/{paper_id}.fetch.json"

with open(fetch_path, 'r') as f:
    data = json.load(f)

data["lead_paragraph"] = "KRILLSCAN is an automated, open-source Python-based software developed to process and analyze echosounder data from the Antarctic krill fishery. It addresses the need for rapid, transparent, and reproducible biomass estimation, enabling near-real-time data analysis and transfer from fishing vessels of opportunity. The software automates noise removal, bottom detection, and swarm identification, achieving a high correlation (0.96) with traditional manual scrutinization while compressing data by up to 100 times for satellite transmission."

data["main_concept"] = "KRILLSCAN Automated Processing Software"

data["infobox_data"] = {
    "architecture_type": "Automated Processing Pipeline (Python-based)",
    "key_innovation": "Open-source automation of krill swarm detection and 100x data compression for remote monitoring.",
    "performance_metric": "0.96 correlation with manual LSSS analysis; 6% NASC underestimation.",
    "computational_efficiency": "Near-real-time processing (faster than data generation) on standard consumer hardware."
}

data["sections"] = [
    {
        "title": "Automated Processing Pipeline",
        "content": "KRILLSCAN utilizes a dual-thread architecture to handle echosounder data in real-time. One thread performs an IO loop that scans for new proprietary Simrad .raw files, while a parallel communications loop manages data transmission. The software employs standardized scientific Python modules, including 'echopy' and 'pyecholab2', to clean the raw signal by removing impulse and background noise.\n\nAfter noise removal, the volume backscatter matrices for each frequency (typically 38 and 120 kHz) are loaded into memory. This automated pipeline ensures that data is processed faster than it is generated, a critical requirement for onboard deployment on fishing vessels where specialized scientific personnel may not be present."
    },
    {
        "title": "Krill Swarm Detection and Integration",
        "content": "A core component of KRILLSCAN is its swarm detection algorithm, based on the SHAPES method. This algorithm identifies contiguous patches of backscatter that exceed a predefined threshold (set to -70 dB for krill). It employs a series of image morphological operations, specifically erosion and dilation, to suppress noise and refine the outlines of detected swarms.\n\nThe software integrates the backscatter within these detection masks to calculate the Nautical Area Scattering Coefficient (NASC), a standard metric for biomass distribution. [[Figure 3]] shows the graphical interface where these masks are overlaid on the echogram for visual verification."
    },
    {
        "title": "Data Compression and Satellite Transfer",
        "content": "To overcome the bandwidth limitations of satellite communication in the Southern Ocean, KRILLSCAN implements aggressive data compression. Processed raw echograms are stored in the open NetCDF format in 10-minute 'snippets'. These files, along with 1-minute averaged NASC tables, can be compressed up to 100 times compared to the original raw data.\n\nThis reduction allows for a 4-hour survey block to be transmitted as a 2–5 MiB file via email. This capability enables remote monitoring and quality control by shore-based scientists, allowing fishing vessels to act as 'platforms of opportunity' for continuous ecosystem monitoring. [[Figure 2]] illustrates this remote data flow."
    },
    {
        "title": "Comparative Validation with Manual Scrutinization",
        "content": "The accuracy of KRILLSCAN was tested against traditional manual scrutinization using the Large Scale Survey System (LSSS). Analysis of data from Norwegian krill surveys (2011–2023) showed that KRILLSCAN's automated NASC estimates were strongly correlated (0.96) with manual results. While the software slightly underestimated total NASC by approximately 6%, this offset was consistent across the encountered biomass range.\n\nThis consistency, combined with the reproducibility of open-source algorithms, offers a significant advantage over manual analysis, which can be prone to operator bias. [[Figure 5]] displays the strong linear relationship between the automated and manual results across various survey years.",
        "figure_index": 5
    }
]

data["concept_breakdown"] = [
    {
        "concept": "Nautical Area Scattering Coefficient (NASC)",
        "description": "A standard unit ($m^2/nmi^2$) used in fisheries acoustics to quantify the total sound backscattered from a specific area, serving as a proxy for biological biomass."
    },
    {
        "concept": "SHAPES Algorithm",
        "description": "A morphological processing technique used to identify and isolate contiguous biological aggregations, such as krill swarms, from background noise and other acoustic targets."
    },
    {
        "concept": "NetCDF",
        "description": "The Network Common Data Form; a self-describing, machine-independent data format used by KRILLSCAN to ensure interoperability and open access to processed acoustic data."
    },
    {
        "concept": "Adaptive Feedback Management (FBM)",
        "description": "A fisheries management strategy that uses real-time data to dynamically adjust catch limits and spatial allocations based on current stock status."
    },
    {
        "concept": "Platforms of Opportunity",
        "description": "Non-scientific vessels, such as commercial fishing boats, that are equipped with automated systems to collect valuable scientific data during their normal operations."
    }
]

data["math_equations"] = [
    {
        "name": "Nautical Area Scattering Coefficient (NASC)",
        "latex": "s_A = 4\\pi (1852)^2 \\int_{z_1}^{z_2} s_v dz",
        "explanation": "The NASC formula integrates the volume backscattering coefficient ($s_v$) over a specific depth range ($z_1$ to $z_2$) to produce a standard area-based measure of backscatter.",
        "symbols": [
            {"symbol": "s_A", "meaning": "Nautical Area Scattering Coefficient ($m^2/nmi^2$)"},
            {"symbol": "s_v", "meaning": "Volume backscattering coefficient"},
            {"symbol": "dz", "meaning": "Depth interval"}
        ]
    },
    {
        "name": "Coefficient of Variation (CV)",
        "latex": "CV = \\frac{\\sigma}{\\mu}",
        "explanation": "Used to assess the relative variability and agreement between the automated KRILLSCAN results and manual LSSS scrutinization.",
        "symbols": [
            {"symbol": "\\sigma", "meaning": "Standard deviation of the NASC differences"},
            {"symbol": "\\mu", "meaning": "Mean NASC value"}
        ]
    }
]

data["figure_explanations"] = [
    {
        "figure_index": 2,
        "explanation": "Data flow chart showing the end-to-end process from onboard raw data collection to KRILLSCAN processing, satellite transfer, and final shore-based biomass estimation."
    },
    {
        "figure_index": 3,
        "explanation": "Screenshot of the KRILLSCAN Graphical User Interface, demonstrating the red swarm detection masks overlaid on multifrequency echograms and real-time NASC graphs."
    },
    {
        "figure_index": 5,
        "explanation": "Regression analysis comparing LSSS and KRILLSCAN results, confirming a 0.96 correlation and establishing the reliability of the automated system."
    }
]

data["see_also"] = [
    {"topic": "Euphausia superba", "description": "The Antarctic krill, a keystone species of the Southern Ocean ecosystem and the primary focus of this software."},
    {"topic": "CCAMLR", "description": "The international commission responsible for the sustainable management of Antarctic marine living resources."},
    {"topic": "LSSS", "description": "The proprietary Large Scale Survey System software used as the gold-standard benchmark for acoustic data analysis."},
    {"topic": "Open-Source Science", "description": "The movement towards making scientific research and data, including processing software like KRILLSCAN, accessible to all."}
]

data["glossary_terms"] = [
    {"term": "NASC", "definition": "Nautical Area Scattering Coefficient; the standard integrated measure of acoustic backscatter used in fisheries."},
    {"term": "Scrutinization", "definition": "The detailed expert review of acoustic data to identify and quantify biological targets."},
    {"term": "NetCDF", "definition": "An open data format for array-oriented scientific data."},
    {"term": "Morphological Operations", "definition": "Image processing techniques like erosion and dilation used to refine the shapes of detected objects."},
    {"term": "Trigger Level", "definition": "A precautionary catch limit that, once reached, triggers specific management actions or closures."}
]

with open(fetch_path, 'w') as f:
    json.dump(data, f, indent=2)
