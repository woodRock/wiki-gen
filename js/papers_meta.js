window.PAPERS_META = {
  "530dab86cb8034bc12a32d21508aaa3f2cc00aa1": {
    "title": "LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels",
    "authors": "Lucas Maes, Quentin Le Lidec, Damien Scieur et al.",
    "year": 2026,
    "venue": "N/A",
    "cc": 1,
    "abstract": "Joint Embedding Predictive Architectures (JEPAs) offer a compelling framework for learning world models in compact latent spaces, yet existing methods remain fragile, relying on complex multi-term losses, exponential moving averages, pre-trained encoders, or auxiliary supervision to avoid representation collapse. In this work, we introduce LeWorldModel (LeWM), the first JEPA that trains stably end",
    "paperId": "530dab86cb8034bc12a32d21508aaa3f2cc00aa1"
  },
  "7318a804566baadc9f4b4ca8255f78744e749a32": {
    "title": "QJL: 1-Bit Quantized JL Transform for KV Cache Quantization with Zero Overhead",
    "authors": "A. Zandieh, Majid Daliri, Insu Han",
    "year": 2024,
    "venue": "AAAI Conference on Artificial Intelligence",
    "cc": 24,
    "abstract": "Serving LLMs requires substantial memory due to the storage requirements of Key-Value (KV) embeddings in the KV cache, which grows with sequence length. An effective approach to compress KV cache is quantization. However, traditional quantization methods face significant memory overhead due to the need to store quantization constants (at least a zero point and a scale) in full precision per data b",
    "paperId": "7318a804566baadc9f4b4ca8255f78744e749a32"
  },
  "ee57e4d7a125f4ca8916284a857c3760d7d378d3": {
    "title": "Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture",
    "authors": "Mahmoud Assran, Quentin Duval, Ishan Misra et al.",
    "year": 2023,
    "venue": "Computer Vision and Pattern Recognition",
    "cc": 719,
    "abstract": "This paper demonstrates an approach for learning highly semantic image representations without relying on hand-crafted data-augmentations. We introduce the Image-based Joint-Embedding Predictive Architecture (I-JEPA), a non-generative approach for self-supervised learning from images. The idea behind I-JEPA is simple: from a single context block, predict the representations of various target block",
    "paperId": "ee57e4d7a125f4ca8916284a857c3760d7d378d3"
  },
  "ef9485a2522f64bca0f5cf67edc28a11984790e8": {
    "title": "PolarQuant: Quantizing KV Caches with Polar Transformation",
    "authors": "Insu Han, Praneeth Kacham, Amin Karbasi et al.",
    "year": 2025,
    "venue": "arXiv.org",
    "cc": 8,
    "abstract": "Large language models (LLMs) require significant memory to store Key-Value (KV) embeddings in their KV cache, especially when handling long-range contexts. Quantization of these KV embeddings is a common technique to reduce memory consumption. This work introduces PolarQuant, a novel quantization method employing random preconditioning and polar transformation. Our method transforms the KV embeddi",
    "paperId": "ef9485a2522f64bca0f5cf67edc28a11984790e8"
  },
  "65780e86fa36e354da618499f8b4616ac87838bf": {
    "title": "TurboQuant: Online Vector Quantization with Near-optimal Distortion Rate",
    "authors": "A. Zandieh, Majid Daliri, Majid Hadian et al.",
    "year": 2025,
    "venue": "arXiv.org",
    "cc": 9,
    "abstract": "Vector quantization, a problem rooted in Shannon's source coding theory, aims to quantize high-dimensional Euclidean vectors while minimizing distortion in their geometric structure. We propose TurboQuant to address both mean-squared error (MSE) and inner product distortion, overcoming limitations of existing methods that fail to achieve optimal distortion rates. Our data-oblivious algorithms, sui",
    "paperId": "65780e86fa36e354da618499f8b4616ac87838bf"
  },
  "204e3073870fae3d05bcbc2f6a8e263d9b72e776": {
    "title": "Attention is All you Need",
    "authors": "Ashish Vaswani, Noam Shazeer, Niki Parmar et al.",
    "year": 2017,
    "venue": "Neural Information Processing Systems",
    "cc": 171923,
    "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experi",
    "paperId": "204e3073870fae3d05bcbc2f6a8e263d9b72e776"
  },
  "8ba856e1c993f43f9c65bf7b9a5f00f157cc212c": {
    "title": "Training Agents Inside of Scalable World Models",
    "authors": "Danijar Hafner, Wilson Yan, Timothy P. Lillicrap",
    "year": 2025,
    "venue": "arXiv.org",
    "cc": 55,
    "abstract": "World models learn general knowledge from videos and simulate experience for training behaviors in imagination, offering a path towards intelligent agents. However, previous world models have been unable to accurately predict object interactions in complex environments. We introduce Dreamer 4, a scalable agent that learns to solve control tasks by reinforcement learning inside of a fast and accura",
    "paperId": "8ba856e1c993f43f9c65bf7b9a5f00f157cc212c"
  },
  "c064de2c71ebc5cf05493f49dc312b033c36b3b9": {
    "title": "Genie: Generative Interactive Environments",
    "authors": "Jake Bruce, Michael Dennis, Ashley Edwards et al.",
    "year": 2024,
    "venue": "International Conference on Machine Learning",
    "cc": 469,
    "abstract": "We introduce Genie, the first generative interactive environment trained in an unsupervised manner from unlabelled Internet videos. The model can be prompted to generate an endless variety of action-controllable virtual worlds described through text, synthetic images, photographs, and even sketches. At 11B parameters, Genie can be considered a foundation world model. It is comprised of a spatiotem",
    "paperId": "c064de2c71ebc5cf05493f49dc312b033c36b3b9"
  },
  "0d0cf5f64c052aa7edc5bb638203616a620557f6": {
    "title": "VICReg: Variance-Invariance-Covariance Regularization for Self-Supervised Learning",
    "authors": "Adrien Bardes, J. Ponce, Yann LeCun",
    "year": 2021,
    "venue": "International Conference on Learning Representations",
    "cc": 1187,
    "abstract": "Recent self-supervised methods for image representation learning are based on maximizing the agreement between embedding vectors from different views of the same image. A trivial solution is obtained when the encoder outputs constant vectors. This collapse problem is often avoided through implicit biases in the learning architecture, that often lack a clear justification or interpretation. In this",
    "paperId": "0d0cf5f64c052aa7edc5bb638203616a620557f6"
  },
  "41cca0b0a27ba363ca56e7033569aeb1922b0ac9": {
    "title": "Recurrent World Models Facilitate Policy Evolution",
    "authors": "David R Ha, J. Schmidhuber",
    "year": 2018,
    "venue": "Neural Information Processing Systems",
    "cc": 1185,
    "abstract": "A generative recurrent neural network is quickly trained in an unsupervised manner to model popular reinforcement learning environments through compressed spatio-temporal representations. The world model's extracted features are fed into compact and simple policies trained by evolution, achieving state of the art results in various environments. We also train our agent entirely inside of an enviro",
    "paperId": "41cca0b0a27ba363ca56e7033569aeb1922b0ac9"
  },
  "988ef01812555a4e2a5810bd245a71f31896b36c": {
    "title": "LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics",
    "authors": "Randall Balestriero, Yann LeCun",
    "year": 2025,
    "venue": "arXiv.org",
    "cc": 38,
    "abstract": "Learning manipulable representations of the world and its dynamics is central to AI. Joint-Embedding Predictive Architectures (JEPAs) offer a promising blueprint, but lack of practical guidance and theory has led to ad-hoc R&D. We present a comprehensive theory of JEPAs and instantiate it in {\\bf LeJEPA}, a lean, scalable, and theoretically grounded training objective. First, we identify the isotr",
    "paperId": "988ef01812555a4e2a5810bd245a71f31896b36c"
  },
  "b49c1adc847c8e2cb9f1b97358366e4887e532ce": {
    "title": "DINOv3",
    "authors": "Oriane Sim'eoni, Huy V. Vo, Maximilian Seitzer et al.",
    "year": 2025,
    "venue": "N/A",
    "cc": 551,
    "abstract": "Self-supervised learning holds the promise of eliminating the need for manual data annotation, enabling models to scale effortlessly to massive datasets and larger architectures. By not being tailored to specific tasks or domains, this training paradigm has the potential to learn visual representations from diverse sources, ranging from natural to aerial images -- using a single algorithm. This te",
    "paperId": "b49c1adc847c8e2cb9f1b97358366e4887e532ce"
  },
  "235303a8bc1e4892efd525a38ead657422d8a519": {
    "title": "Transformers are Sample Efficient World Models",
    "authors": "Vincent Micheli, Eloi Alonso, Franccois Fleuret",
    "year": 2022,
    "venue": "International Conference on Learning Representations",
    "cc": 286,
    "abstract": "Deep reinforcement learning agents are notoriously sample inefficient, which considerably limits their application to real-world problems. Recently, many model-based methods have been designed to address this issue, with learning in the imagination of a world model being one of the most prominent approaches. However, while virtually unlimited interaction with a simulated environment sounds appeali",
    "paperId": "235303a8bc1e4892efd525a38ead657422d8a519"
  },
  "775f42ed458b8c5b0f2094ea4ff5b64c557b1a34": {
    "title": "A Path Towards Autonomous Machine Intelligence Version 0.9.2, 2022-06-27",
    "authors": "Yann LeCun, Courant",
    "year": 2022,
    "venue": "N/A",
    "cc": 709,
    "abstract": "",
    "paperId": "775f42ed458b8c5b0f2094ea4ff5b64c557b1a34"
  },
  "02f4516502bc0d05fb8971687f37c5f319ca2704": {
    "title": "Diffusion for World Modeling: Visual Details Matter in Atari",
    "authors": "Eloi Alonso, Adam Jelley, Vincent Micheli et al.",
    "year": 2024,
    "venue": "Neural Information Processing Systems",
    "cc": 194,
    "abstract": "World models constitute a promising approach for training reinforcement learning agents in a safe and sample-efficient manner. Recent world models predominantly operate on sequences of discrete latent variables to model environment dynamics. However, this compression into a compact discrete representation may ignore visual details that are important for reinforcement learning. Concurrently, diffus",
    "paperId": "02f4516502bc0d05fb8971687f37c5f319ca2704"
  },
  "bbc3981589948f7c9d14a20980a50e8065d732c6": {
    "title": "Efficient World Models with Context-Aware Tokenization",
    "authors": "Vincent Micheli, Eloi Alonso, Franccois Fleuret",
    "year": 2024,
    "venue": "International Conference on Machine Learning",
    "cc": 23,
    "abstract": "Scaling up deep Reinforcement Learning (RL) methods presents a significant challenge. Following developments in generative modelling, model-based RL positions itself as a strong contender. Recent advances in sequence modelling have led to effective transformer-based world models, albeit at the price of heavy computations due to the long sequences of tokens required to accurately simulate environme",
    "paperId": "bbc3981589948f7c9d14a20980a50e8065d732c6"
  },
  "f81a1b4510631d14b5b565c4701ee056f8d5c72f": {
    "title": "CodePlan: Repository-Level Coding using LLMs and Planning",
    "authors": "Ramakrishna Bairi, Atharv Sonwane, Aditya Kanade et al.",
    "year": 2023,
    "venue": "Proc. ACM Softw. Eng.",
    "cc": 186,
    "abstract": "Software engineering activities such as package migration, fixing error reports from static analysis or testing, and adding type annotations or other specifications to a codebase, involve pervasively editing the entire repository of code. We formulate these activities as repository-level coding tasks. Recent tools like GitHub Copilot, which are powered by Large Language Models (LLMs), have succeed",
    "paperId": "f81a1b4510631d14b5b565c4701ee056f8d5c72f"
  },
  "dc52b09089704ebd6f471177474bc29741c50023": {
    "title": "Fast Transformer Decoding: One Write-Head is All You Need",
    "authors": "Noam Shazeer",
    "year": 2019,
    "venue": "arXiv.org",
    "cc": 717,
    "abstract": "Multi-head attention layers, as used in the Transformer neural sequence model, are a powerful alternative to RNNs for moving information across and between sequences. While training these layers is generally fast and simple, due to parallelizability across the length of the sequence, incremental inference (where such paralleization is impossible) is often slow, due to the memory-bandwidth cost of ",
    "paperId": "dc52b09089704ebd6f471177474bc29741c50023"
  },
  "42a14d824caa3348046eb34c37e2ab7985faa7a3": {
    "title": "High-throughput Generative Inference of Large Language Models with a Single GPU",
    "authors": "Ying Sheng, Lianmin Zheng, Binhang Yuan et al.",
    "year": 2023,
    "venue": "International Conference on Machine Learning",
    "cc": 635,
    "abstract": "The high computational and memory requirements of large language model (LLM) inference make it feasible only with multiple high-end accelerators. Motivated by the emerging demand for latency-insensitive tasks with batched processing, this paper initiates the study of high-throughput LLM inference using limited resources, such as a single commodity GPU. We present FlexGen, a high-throughput generat",
    "paperId": "42a14d824caa3348046eb34c37e2ab7985faa7a3"
  },
  "a3e000e0d7f64c1d094c2a8bf6f43992cbabe91b": {
    "title": "KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache",
    "authors": "Zirui Liu, Jiayi Yuan, Hongye Jin et al.",
    "year": 2024,
    "venue": "International Conference on Machine Learning",
    "cc": 402,
    "abstract": "Efficiently serving large language models (LLMs) requires batching of many requests to reduce the cost per request. Yet, with larger batch sizes and longer context lengths, the key-value (KV) cache, which stores attention keys and values to avoid re-computations, significantly increases memory demands and becomes the new bottleneck in speed and memory usage. Additionally, the loading of the KV cac",
    "paperId": "a3e000e0d7f64c1d094c2a8bf6f43992cbabe91b"
  },
  "b085968c4362fb286ad6c5ef71a5db9630da0498": {
    "title": "KVQuant: Towards 10 Million Context Length LLM Inference with KV Cache Quantization",
    "authors": "Coleman Hooper, Sehoon Kim, Hiva Mohammadzadeh et al.",
    "year": 2024,
    "venue": "Neural Information Processing Systems",
    "cc": 445,
    "abstract": "LLMs are seeing growing use for applications which require large context windows, and with these large context windows KV cache activations surface as the dominant contributor to memory consumption during inference. Quantization is a promising approach for compressing KV cache activations; however, existing solutions fail to represent activations accurately in sub-4-bit precision. Our work, KVQuan",
    "paperId": "b085968c4362fb286ad6c5ef71a5db9630da0498"
  },
  "104b0bb1da562d53cbda87aec79ef6a2827d191a": {
    "title": "Llama 2: Open Foundation and Fine-Tuned Chat Models",
    "authors": "Hugo Touvron, Louis Martin, Kevin R. Stone et al.",
    "year": 2023,
    "venue": "arXiv.org",
    "cc": 16348,
    "abstract": "In this work, we develop and release Llama 2, a collection of pretrained and fine-tuned large language models (LLMs) ranging in scale from 7 billion to 70 billion parameters. Our fine-tuned LLMs, called Llama 2-Chat, are optimized for dialogue use cases. Our models outperform open-source chat models on most benchmarks we tested, and based on our human evaluations for helpfulness and safety, may be",
    "paperId": "104b0bb1da562d53cbda87aec79ef6a2827d191a"
  },
  "b31a5884a8ebe96b6300839b28608b97f8f8ef76": {
    "title": "LongBench: A Bilingual, Multitask Benchmark for Long Context Understanding",
    "authors": "Yushi Bai, Xin Lv, Jiajie Zhang et al.",
    "year": 2023,
    "venue": "Annual Meeting of the Association for Computational Linguistics",
    "cc": 1096,
    "abstract": "Although large language models (LLMs) demonstrate impressive performance for many language tasks, most of them can only handle texts a few thousand tokens long, limiting their applications on longer sequence inputs, such as books, reports, and codebases. Recent works have proposed methods to improve LLMs' long context capabilities by extending context windows and more sophisticated memory mechanis",
    "paperId": "b31a5884a8ebe96b6300839b28608b97f8f8ef76"
  },
  "9f0fe125af3cfbad99f1f2a6ada0daf61eef92b1": {
    "title": "How Long Can Context Length of Open-Source LLMs truly Promise?",
    "authors": "Dacheng Li, \u2217. RulinShao, Anze Xie et al.",
    "year": null,
    "venue": "N/A",
    "cc": 108,
    "abstract": "",
    "paperId": "9f0fe125af3cfbad99f1f2a6ada0daf61eef92b1"
  },
  "f608011b0f50a14bb2949c186a7c632a099aa75b": {
    "title": "WKVQuant: Quantizing Weight and Key/Value Cache for Large Language Models Gains More",
    "authors": "Yuxuan Yue, Zhihang Yuan, Haojie Duanmu et al.",
    "year": 2024,
    "venue": "arXiv.org",
    "cc": 75,
    "abstract": "Large Language Models (LLMs) face significant deployment challenges due to their substantial memory requirements and the computational demands of auto-regressive text generation process. This paper addresses these challenges by focusing on the quantization of LLMs, a technique that reduces memory consumption by converting model parameters and activations into low-bit integers. We critically analyz",
    "paperId": "f608011b0f50a14bb2949c186a7c632a099aa75b"
  },
  "dfa0de5cae63eacd675339fc81b13479c51bb153": {
    "title": "Lessons from the Trenches on Reproducible Evaluation of Language Models",
    "authors": "Stella Biderman, Hailey Schoelkopf, Lintang Sutawika et al.",
    "year": 2024,
    "venue": "arXiv.org",
    "cc": 127,
    "abstract": "Effective evaluation of language models remains an open challenge in NLP. Researchers and engineers face methodological issues such as the sensitivity of models to evaluation setup, difficulty of proper comparisons across methods, and the lack of reproducibility and transparency. In this paper we draw on three years of experience in evaluating large language models to provide guidance and lessons ",
    "paperId": "dfa0de5cae63eacd675339fc81b13479c51bb153"
  },
  "bb8222ae651ac100923dbb0b9cd6fd01b9e196cd": {
    "title": "Instruction-Tuning Llama-3-8B Excels in City-Scale Mobility Prediction",
    "authors": "Peizhi Tang, Chuang Yang, Tong Xing et al.",
    "year": 2024,
    "venue": "HuMob-Challenge@SIGSPATIAL",
    "cc": 16,
    "abstract": "Human mobility prediction plays a critical role in applications such as disaster response, urban planning, and epidemic forecasting. Traditional methods often rely on designing crafted, domain-specific models, and typically focus on short-term predictions, which struggle to generalize across diverse urban environments. In this study, we introduce Llama-3-8B-Mob, a large language model fine-tuned w",
    "paperId": "bb8222ae651ac100923dbb0b9cd6fd01b9e196cd"
  },
  "6b94cde5d7f04cc411394c115868ad20b1dbf456": {
    "title": "FinMind-Y-Me at the Regulations Challenge Task: Financial Mind Your Meaning based on THaLLE",
    "authors": "Pantid Chantangphol, Pornchanan Balee, Kantapong Sucharitpongpan et al.",
    "year": 2025,
    "venue": "COLING Workshops",
    "cc": 4,
    "abstract": "",
    "paperId": "6b94cde5d7f04cc411394c115868ad20b1dbf456"
  },
  "27d391d65ab42c30dc35595213ba6585633afa5d": {
    "title": "CoLT5: Faster Long-Range Transformers with Conditional Computation",
    "authors": "J. Ainslie, Tao Lei, Michiel de Jong et al.",
    "year": 2023,
    "venue": "Conference on Empirical Methods in Natural Language Processing",
    "cc": 92,
    "abstract": "Many natural language processing tasks benefit from long inputs, but processing long documents with Transformers is expensive -- not only due to quadratic attention complexity but also from applying feedforward and projection layers to every token. However, not all tokens are equally important, especially for longer documents. We propose CoLT5, a long-input Transformer model that builds on this in",
    "paperId": "27d391d65ab42c30dc35595213ba6585633afa5d"
  },
  "1dff6b1b35e2d45d4db57c8b4e4395486c3e365f": {
    "title": "Token Merging: Your ViT But Faster",
    "authors": "Daniel Bolya, Cheng-Yang Fu, Xiaoliang Dai et al.",
    "year": 2022,
    "venue": "International Conference on Learning Representations",
    "cc": 892,
    "abstract": "We introduce Token Merging (ToMe), a simple method to increase the throughput of existing ViT models without needing to train. ToMe gradually combines similar tokens in a transformer using a general and light-weight matching algorithm that is as fast as pruning while being more accurate. Off-the-shelf, ToMe can 2x the throughput of state-of-the-art ViT-L @ 512 and ViT-H @ 518 models on images and ",
    "paperId": "1dff6b1b35e2d45d4db57c8b4e4395486c3e365f"
  },
  "9653c070724e44f023e8cc3ec79f0b9e6d59480d": {
    "title": "iBOT: Image BERT Pre-Training with Online Tokenizer",
    "authors": "Jinghao Zhou, Chen Wei, Huiyu Wang et al.",
    "year": 2021,
    "venue": "arXiv.org",
    "cc": 1022,
    "abstract": "The success of language Transformers is primarily attributed to the pretext task of masked language modeling (MLM), where texts are first tokenized into semantically meaningful pieces. In this work, we study masked image modeling (MIM) and indicate the advantages and challenges of using a semantically meaningful visual tokenizer. We present a self-supervised framework iBOT that can perform masked ",
    "paperId": "9653c070724e44f023e8cc3ec79f0b9e6d59480d"
  },
  "1f0376cde28008e77a4fb541f2c6a95abe943b1a": {
    "title": "Predicting Structured Data",
    "authors": "G. Bakir, T. Hofmann, B. Scholkopf et al.",
    "year": 2007,
    "venue": "N/A",
    "cc": 72,
    "abstract": "",
    "paperId": "1f0376cde28008e77a4fb541f2c6a95abe943b1a"
  },
  "7ee0981e2e39d2864dbbe8af540046ba8388d63a": {
    "title": "Enhanced Solar-to-Heat Efficiency of Photothermal Materials Containing an Additional Light-Reflection Layer for Solar-Driven Interfacial Water Evaporation",
    "authors": "Yukang Fan, Zhuoyue Tian, Fei Wang et al.",
    "year": 2021,
    "venue": "N/A",
    "cc": 59,
    "abstract": "Solar-driven interfacial evaporation integrating inexhaustible solar energy and abundant seawater to address the scarcity of freshwater is a green and sustainable solution, but its industrial appli...",
    "paperId": "7ee0981e2e39d2864dbbe8af540046ba8388d63a"
  },
  "722ad6ac92286507437b31486f47987d6ece05c9": {
    "title": "BEiT: BERT Pre-Training of Image Transformers",
    "authors": "Hangbo Bao, Li Dong, Furu Wei",
    "year": 2021,
    "venue": "International Conference on Learning Representations",
    "cc": 3579,
    "abstract": "We introduce a self-supervised vision representation model BEiT, which stands for Bidirectional Encoder representation from Image Transformers. Following BERT developed in the natural language processing area, we propose a masked image modeling task to pretrain vision Transformers. Specifically, each image has two views in our pre-training, i.e, image patches (such as 16x16 pixels), and visual tok",
    "paperId": "722ad6ac92286507437b31486f47987d6ece05c9"
  },
  "8f2bca9d684005675e294b33c26481e36f528cdb": {
    "title": "data2vec: A General Framework for Self-supervised Learning in Speech, Vision and Language",
    "authors": "Alexei Baevski, Wei-Ning Hsu, Qiantong Xu et al.",
    "year": 2022,
    "venue": "International Conference on Machine Learning",
    "cc": 1097,
    "abstract": "While the general idea of self-supervised learning is identical across modalities, the actual algorithms and objectives differ widely because they were developed with a single modality in mind. To get us closer to general self-supervised learning, we present data2vec, a framework that uses the same learning method for either speech, NLP or computer vision. The core idea is to predict latent repres",
    "paperId": "8f2bca9d684005675e294b33c26481e36f528cdb"
  },
  "3387e9dedb7accc3c248d194b012cab0ab5ab0b8": {
    "title": "Context Autoencoder for Self-supervised Representation Learning",
    "authors": "Xiaokang Chen, Mingyu Ding, Xiaodi Wang et al.",
    "year": 2022,
    "venue": "International Journal of Computer Vision",
    "cc": 475,
    "abstract": "We present a novel masked image modeling (MIM) approach, context autoencoder (CAE), for self-supervised representation pretraining. We pretrain an encoder by making predictions in the encoded representation space. The pretraining tasks include two tasks: masked representation prediction\u2014predict the representations for the masked patches, and masked patch reconstruction\u2014reconstruct the masked patch",
    "paperId": "3387e9dedb7accc3c248d194b012cab0ab5ab0b8"
  },
  "e866cadc660cb4ba98d03a363b99523923fb149b": {
    "title": "The coefficient of determination R-squared is more informative than SMAPE, MAE, MAPE, MSE and RMSE in regression analysis evaluation",
    "authors": "D. Chicco, M. Warrens, Giuseppe Jurman",
    "year": 2021,
    "venue": "PeerJ Computer Science",
    "cc": 4114,
    "abstract": "Regression analysis makes up a large part of supervised machine learning, and consists of the prediction of a continuous independent target from a set of other predictor variables. The difference between binary classification and regression is in the target range: in binary classification, the target can have only two values (usually encoded as 0 and 1), while in regression the target can have mul",
    "paperId": "e866cadc660cb4ba98d03a363b99523923fb149b"
  },
  "0f416c637a5a78435e6b12ebf1ce891224de0edc": {
    "title": "Scaling Speech Technology to 1, 000+ Languages",
    "authors": "Vineel Pratap, Andros Tjandra, Bowen Shi et al.",
    "year": 2023,
    "venue": "Journal of machine learning research",
    "cc": 578,
    "abstract": "Expanding the language coverage of speech technology has the potential to improve access to information for many more people. However, current speech technology is restricted to about one hundred languages which is a small fraction of the over 7,000 languages spoken around the world. The Massively Multilingual Speech (MMS) project increases the number of supported languages by 10-40x, depending on",
    "paperId": "0f416c637a5a78435e6b12ebf1ce891224de0edc"
  },
  "38f93092ece8eee9771e61c1edaf11b1293cae1b": {
    "title": "Bootstrap Your Own Latent: A New Approach to Self-Supervised Learning",
    "authors": "Jean-Bastien Grill, Florian Strub, Florent Altch'e et al.",
    "year": 2020,
    "venue": "Neural Information Processing Systems",
    "cc": 8296,
    "abstract": "We introduce Bootstrap Your Own Latent (BYOL), a new approach to self-supervised image representation learning. BYOL relies on two neural networks, referred to as online and target networks, that interact and learn from each other. From an augmented view of an image, we train the online network to predict the target network representation of the same image under a different augmented view. At the ",
    "paperId": "38f93092ece8eee9771e61c1edaf11b1293cae1b"
  },
  "6c2916ca7e3cf4ad846d3e08f6446f1550c3076f": {
    "title": "Stock Price Forecast Based on LSTM Neural Network",
    "authors": "Qiang Jiang, Chengli Tang, Chen Chen et al.",
    "year": 2018,
    "venue": "Proceedings of the Twelfth International Conference on Management Science and Engineering Management",
    "cc": 42,
    "abstract": "",
    "paperId": "6c2916ca7e3cf4ad846d3e08f6446f1550c3076f"
  },
  "ac3ee98020251797c2b401e1389461df88e52e62": {
    "title": "Empirical Evaluation of Gated Recurrent Neural Networks on Sequence Modeling",
    "authors": "Junyoung Chung, \u00c7aglar G\u00fcl\u00e7ehre, Kyunghyun Cho et al.",
    "year": 2014,
    "venue": "arXiv.org",
    "cc": 14430,
    "abstract": "In this paper we compare different types of recurrent units in recurrent neural networks (RNNs). Especially, we focus on more sophisticated units that implement a gating mechanism, such as a long short-term memory (LSTM) unit and a recently proposed gated recurrent unit (GRU). We evaluate these recurrent units on the tasks of polyphonic music modeling and speech signal modeling. Our experiments re",
    "paperId": "ac3ee98020251797c2b401e1389461df88e52e62"
  },
  "f475e99542dbdfca962d36f7af0fc4854042495c": {
    "title": "A Framework for Evaluating Predictive Models Using Synthetic Image Covariates and Longitudinal Data",
    "authors": "S. Deltadahl, Andreu Vall, Vijay Ivaturi et al.",
    "year": 2024,
    "venue": "Proceedings of the American Conference of Pharmacometrics 2024",
    "cc": 1,
    "abstract": "Objectives We present a novel framework to synthesize data sets with complex covariates, such as medical images, linked to simulated longitudinal patient outcomes. This allows us to evaluate and refine predictive models by providing training data where true relationships are known. Our implementation focuses on generating optical coherence tomography (OCT) scans, but the framework is adaptable to ",
    "paperId": "f475e99542dbdfca962d36f7af0fc4854042495c"
  },
  "43428880d75b3a14257c3ee9bda054e61eb869c0": {
    "title": "Convolutional Sequence to Sequence Learning",
    "authors": "Jonas Gehring, Michael Auli, David Grangier et al.",
    "year": 2017,
    "venue": "International Conference on Machine Learning",
    "cc": 3500,
    "abstract": "The prevalent approach to sequence to sequence learning maps an input sequence to a variable length output sequence via recurrent neural networks. We introduce an architecture based entirely on convolutional neural networks. Compared to recurrent models, computations over all elements can be fully parallelized during training and optimization is easier since the number of non-linearities is fixed ",
    "paperId": "43428880d75b3a14257c3ee9bda054e61eb869c0"
  },
  "c6850869aa5e78a107c378d2e8bfa39633158c0c": {
    "title": "Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation",
    "authors": "Yonghui Wu, M. Schuster, Z. Chen et al.",
    "year": 2016,
    "venue": "arXiv.org",
    "cc": 7208,
    "abstract": "Neural Machine Translation (NMT) is an end-to-end learning approach for automated translation, with the potential to overcome many of the weaknesses of conventional phrase-based translation systems. Unfortunately, NMT systems are known to be computationally expensive both in training and in translation inference. Also, most NMT systems have difficulty with rare words. These issues have hindered NM",
    "paperId": "c6850869aa5e78a107c378d2e8bfa39633158c0c"
  },
  "1518039b5001f1836565215eb047526b3ac7f462": {
    "title": "Neural Machine Translation of Rare Words with Subword Units",
    "authors": "Rico Sennrich, B. Haddow, Alexandra Birch",
    "year": 2015,
    "venue": "Annual Meeting of the Association for Computational Linguistics",
    "cc": 8574,
    "abstract": "Neural machine translation (NMT) models typically operate with a fixed vocabulary, but translation is an open-vocabulary problem. Previous work addresses the translation of out-of-vocabulary words by backing off to a dictionary. In this paper, we introduce a simpler and more effective approach, making the NMT model capable of open-vocabulary translation by encoding rare and unknown words as sequen",
    "paperId": "1518039b5001f1836565215eb047526b3ac7f462"
  },
  "b60abe57bc195616063be10638c6437358c81d1e": {
    "title": "Deep Recurrent Models with Fast-Forward Connections for Neural Machine Translation",
    "authors": "Jie Zhou, Ying Cao, Xuguang Wang et al.",
    "year": 2016,
    "venue": "Transactions of the Association for Computational Linguistics",
    "cc": 222,
    "abstract": "Neural machine translation (NMT) aims at solving machine translation (MT) problems using neural networks and has exhibited promising results in recent years. However, most of the existing NMT models are shallow and there is still a performance gap between a single NMT model and the best conventional MT system. In this work, we introduce a new type of linear connections, named fast-forward connecti",
    "paperId": "b60abe57bc195616063be10638c6437358c81d1e"
  },
  "510e26733aaff585d65701b9f1be7ca9d5afc586": {
    "title": "Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer",
    "authors": "Noam Shazeer, Azalia Mirhoseini, Krzysztof Maziarz et al.",
    "year": 2017,
    "venue": "International Conference on Learning Representations",
    "cc": 4236,
    "abstract": "The capacity of a neural network to absorb information is limited by its number of parameters. Conditional computation, where parts of the network are active on a per-example basis, has been proposed in theory as a way of dramatically increasing model capacity without a proportional increase in computation. In practice, however, there are significant algorithmic and performance challenges. In this",
    "paperId": "510e26733aaff585d65701b9f1be7ca9d5afc586"
  },
  "b1175c2344c7acf7d0048650204506384a2e5184": {
    "title": "From KMMLU-Redux to Pro: A Professional Korean Benchmark Suite for LLM Evaluation",
    "authors": "Seokhee Hong, SunKyoung Kim, Guijin Son et al.",
    "year": 2025,
    "venue": "Conference on Empirical Methods in Natural Language Processing",
    "cc": 2,
    "abstract": "The development of Large Language Models (LLMs) requires robust benchmarks that encompass not only academic domains but also industrial fields to effectively evaluate their applicability in real-world scenarios. In this paper, we introduce two Korean expert-level benchmarks. KMMLU-Redux, reconstructed from the existing KMMLU, consists of questions from the Korean National Technical Qualification e",
    "paperId": "b1175c2344c7acf7d0048650204506384a2e5184"
  },
  "254fc73a839810a7155acf17e047110c29dc068d": {
    "title": "Self-chats from Large Language Models Make Small ChatPal Better Anonymous ACL submission",
    "authors": "Gabriel Forgues, J. Pineau, Peng Gao et al.",
    "year": null,
    "venue": "N/A",
    "cc": 0,
    "abstract": "",
    "paperId": "254fc73a839810a7155acf17e047110c29dc068d"
  },
  "f52de7242e574b70410ca6fb70b79c811919fc00": {
    "title": "Learning Accurate, Compact, and Interpretable Tree Annotation",
    "authors": "Slav Petrov, Leon Barrett, R. Thibaux et al.",
    "year": 2006,
    "venue": "Annual Meeting of the Association for Computational Linguistics",
    "cc": 990,
    "abstract": "We present an automatic approach to tree annotation in which basic nonterminal symbols are alternately split and merged to maximize the likelihood of a training treebank. Starting with a simple X-bar grammar, we learn a new grammar whose nonterminals are subsymbols of the original nonterminals. In contrast with previous work, we are able to split various terminals to different degrees, as appropri",
    "paperId": "f52de7242e574b70410ca6fb70b79c811919fc00"
  },
  "174bbdb96252454cbb40a9c4e53335996235a008": {
    "title": "Fast and Accurate Shift-Reduce Constituent Parsing",
    "authors": "Muhua Zhu, Yue Zhang, Wenliang Chen et al.",
    "year": 2013,
    "venue": "Annual Meeting of the Association for Computational Linguistics",
    "cc": 221,
    "abstract": "",
    "paperId": "174bbdb96252454cbb40a9c4e53335996235a008"
  },
  "2fcab57cf4cd55e3c12ac1a7ca50a83337804235": {
    "title": "Allowing humans to interactively guide machines where to look does not always improve human-AI team's classification accuracy",
    "authors": "G. Nguyen, Mohammad Reza Taesiri, Sunnie S. Y. Kim et al.",
    "year": 2024,
    "venue": "XAI4CV",
    "cc": 8,
    "abstract": "Via thousands of papers in Explainable AI (XAI), attention maps \\cite{vaswani2017attention} and feature importance maps \\cite{bansal2020sam} have been established as a common means for finding how important each input feature is to an AI's decisions. It is an interesting, unexplored question whether allowing users to edit the feature importance at test time would improve a human-AI team's accuracy",
    "paperId": "2fcab57cf4cd55e3c12ac1a7ca50a83337804235"
  },
  "4181c334559c8fb23fed35dea9cb9e03b1b28289": {
    "title": "CONTROLLED SHUNT REACTORS IN BULK ELECTRIC NETWORKS",
    "authors": "V. Kuchanskyy",
    "year": 2020,
    "venue": "PUBLIC COMMUNICATION IN SCIENCE: PHILOSOPHICAL, CULTURAL, POLITICAL, ECONOMIC AND IT CONTEXT - VOLUME 2",
    "cc": 0,
    "abstract": "[3] Lan, Z., Chen, M., Goodman, S., Gimpel, K., Sharma, P. & Soricut, R. (2019). ALBERT: A Lite BERT for Self-supervised Learning of Language Representations. Proceedings of the 2019 International Conference on Learning Representations (ICLR 2019). May, 2019. New Orleans, United States of America. [4] Sanh, V., Debut, L., Chaumond, J. & Wolf, T. (2019). DistilBERT, a distilled version of BERT: sma",
    "paperId": "4181c334559c8fb23fed35dea9cb9e03b1b28289"
  },
  "f3cda72a9d0cf081edc29aec0c5e7b3175996f00": {
    "title": "On the Analysis and Distillation of Emergent Outlier Properties in Pre-trained Language Models",
    "authors": "Tianyang Zhao, Kunwar Yashraj Singh, Srikar Appalaraju et al.",
    "year": 2025,
    "venue": "North American Chapter of the Association for Computational Linguistics",
    "cc": 2,
    "abstract": "A small subset of dimensions within language Transformers\u2019 representation spaces emerge as \"outliers\" during pretraining, encoding critical knowledge sparsely. We extend previous findings on emergent outliers to Encoder-Decoder Transformers and instruction-finetuned models, and tackle the problem of distilling a student Transformer from a larger teacher Trans-former. Knowledge distillation reduces",
    "paperId": "f3cda72a9d0cf081edc29aec0c5e7b3175996f00"
  },
  "39d9c3f1cd4bd5069713e50dc7301570575fc055": {
    "title": "Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and Next Generation Agentic Capabilities",
    "authors": "Gheorghe Comanici, Eric Bieber, Mike Schaekermann et al.",
    "year": 2025,
    "venue": "arXiv.org",
    "cc": 2415,
    "abstract": "In this report, we introduce the Gemini 2.X model family: Gemini 2.5 Pro and Gemini 2.5 Flash, as well as our earlier Gemini 2.0 Flash and Flash-Lite models. Gemini 2.5 Pro is our most capable model yet, achieving SoTA performance on frontier coding and reasoning benchmarks. In addition to its incredible coding and reasoning skills, Gemini 2.5 Pro is a thinking model that excels at multimodal unde",
    "paperId": "39d9c3f1cd4bd5069713e50dc7301570575fc055"
  },
  "3a6edf9f8e58d5b4053e6d454112f4864c3343cb": {
    "title": "Multilingual Machine Translation with Open Large Language Models at Practical Scale: An Empirical Study",
    "authors": "Menglong Cui, Pengzhi Gao, Wei Liu et al.",
    "year": 2025,
    "venue": "North American Chapter of the Association for Computational Linguistics",
    "cc": 39,
    "abstract": "Large language models (LLMs) have shown continuously improving multilingual capabilities, and even small-scale open-source models have demonstrated rapid performance enhancement. In this paper, we systematically explore the abilities of open LLMs with less than ten billion parameters to handle multilingual machine translation (MT) tasks. We conduct comprehensive evaluations on six popular LLMs and",
    "paperId": "3a6edf9f8e58d5b4053e6d454112f4864c3343cb"
  },
  "f9fa002f2f09fd2465902a3e1511b8d918f52b3e": {
    "title": "Constraints on spin-0 dark matter mediators and invisible Higgs decays using ATLAS 13\u00a0TeV pp collision data with two top quarks and missing transverse momentum in the final state",
    "authors": "G. Aad, B. Abbott, D. Abbott et al.",
    "year": 2022,
    "venue": "The European Physical Journal C",
    "cc": 25,
    "abstract": "This paper presents a statistical combination of searches targeting final states with two top quarks and invisible particles, characterised by the presence of zero, one or two leptons, at least one jet originating from a b -quark and missing transverse momentum. The analyses are searches for phenomena beyond the Standard Model consistent with the direct production of dark matter in pp collisions a",
    "paperId": "f9fa002f2f09fd2465902a3e1511b8d918f52b3e"
  },
  "163b4d6a79a5b19af88b8585456363340d9efd04": {
    "title": "GPT-4 Technical Report",
    "authors": "OpenAI Josh Achiam, Steven Adler, S. Agarwal et al.",
    "year": 2023,
    "venue": "N/A",
    "cc": 23345,
    "abstract": "We report the development of GPT-4, a large-scale, multimodal model which can accept image and text inputs and produce text outputs. While less capable than humans in many real-world scenarios, GPT-4 exhibits human-level performance on various professional and academic benchmarks, including passing a simulated bar exam with a score around the top 10% of test takers. GPT-4 is a Transformer-based mo",
    "paperId": "163b4d6a79a5b19af88b8585456363340d9efd04"
  },
  "11bffac6cc4b3143a68ffe1bcf7d4a9be601516a": {
    "title": "Quantization distortion in pulse-count modulation with nonuniform spacing of levels",
    "authors": "P. F. Panter, W. Dite",
    "year": 1951,
    "venue": "Proceedings of the IRE",
    "cc": 237,
    "abstract": "",
    "paperId": "11bffac6cc4b3143a68ffe1bcf7d4a9be601516a"
  },
  "71a9901f5c3eaa4f5694b7eedbcbb143d287a0ea": {
    "title": "ARC-AGI-2: A New Challenge for Frontier AI Reasoning Systems",
    "authors": "Fran\u00e7ois Chollet, Mike Knoop, Gregory Kamradt et al.",
    "year": 2025,
    "venue": "arXiv.org",
    "cc": 101,
    "abstract": "The Abstraction and Reasoning Corpus for Artificial General Intelligence (ARC-AGI), introduced in 2019, established a challenging benchmark for evaluating the general fluid intelligence of artificial systems via a set of unique, novel tasks only requiring minimal prior knowledge. While ARC-AGI has spurred significant research activity over the past five years, recent AI progress calls for benchmar",
    "paperId": "71a9901f5c3eaa4f5694b7eedbcbb143d287a0ea"
  }
};
