# Collaborative-Networks-In-Machine-Learning

Citation networks are graphical networks composed of publications as nodes and citations as edges. They offer a unique look into scientific collaboration and the flow of knowledge within academia. In this repo, we examine the plausibility of using GNNs for node classification and link prediction on citation networks and apply this to a custom dataset of hardware ML papers. We also perform graphical analysis to determine various characteristics of existing datasets and for our new dataset.

## Motivation

As a part of the course ECE 381K - Machine Learning on Real World Networks, we examine methods for learning and optimization on real-life applications of systems represented by networks. As such, much of our learning is driven by this semester-long project examining the existing applications on these systems.

Supplied with existing networks such as Cora and CiteSeer, we are tasked with examining the efficacy of node classification and link prediction on these citation networks. However, since node classification and link prediction are well documented and explored on these networks, we lok towards creating a new dataset of papers in a relevant and related field, ML hardware, to define a similar network with potential applications in the academic or professional setting for learning on ML models.

As such, in these repo we establish a baseline performance for node classification and link prediction on the given datasets to better assess the performance of GNNs on the new database. In this regard we also experiment with a couple of different existing models (such as StellarGraph and DGL) to observe any potential polarizing differences in strength of model. We also introduce a new dataset, the PubMed Diabetes dataset, to provide additional variety of publication networks in topic, size, and characteristics. We then find characteristics of all of the datasets in terms of number of nodes, edges, and features, average degree, clustering coefficient, and more. Then, we apply these methods to our own dataset to see how it compares, optimizing the dataset through methods such as Principal Component Analysis to provide the strongest model. We also look at the homophily of our dataset to determine how distinct our given classes are.

## Build Status

Currently, the models and methods in this repo have all been tested and finalized, though opportunity for development could exist in modifying the existing datasets or models for further optimization or analysis of its qualities.

## Screenshots

As the saying goes, a picture is equal to a thousand words. Most people will be interested if there is a visual representation of what the project is about. It helps them understand better. A visual representation can be snapshots of the project or a video of the functioning of the project.

## Tech/Framework used

All of the code in this repo is in Python, either in the format of a Python file or in a Jupyter Notebook. Other than understanding Python, this repo also incorporates some knowledge of graph networks and data science fundamentals like graph characteristics and neural networks. This repository also focuses on Graph Neural Networks (GNNs), so basic understanding of these models will also be beneficial to understanding.

This repo uses common Python libraries for data science such as Pandas, Matplotlib, and Sci-Kit Learn, but also uses some libraries more related to network analysis and creation such as StellarGraph, NetworkX, and TensorFlow Keras. Additionally, this repo also utilizes the help of another GitHub repo with the purpose of utilizing spaCy for keyword extraction.

## Installation

This project can be run as a normal Jupyter Notebook after installing the necessary dependencies to retrieve the relevant results. An Anaconda environment can be helpful in installing many of these packages.

## How to Use?

Each file in the repo can be run as either a standard Python file or Jupyter Notebook. Deliberation on the organization and roles of each file are explained below.

### Organization

The data folder of the project contains the data files used, separated by the dataset that they are a part of, CiteSeer, Cora, MAG (used experimentally but left out for size), WoS, and updated WoS. Each of these contain csv files for the data and their original data formats if applicable.

The model folder contains the GNN models used for node classification and link prediction on each model. Some models have been divided between two files (such as some models for DGL), but the basic organization still applies. In this regard, models exist for CiteSeer, Cora, MAG, PubMed, and WoS. These files also contain some of the code used for finding the characteristics of a network, since formatting the data into a NetworkX graph (used for the network characteristics) can be computationally expensive. Since the same code was used for the updated WoS graph, the same files were used and only the newest data is available. For the smaller dataset, the code can be rerun by passing the alternative file location to the correct cell in the Jupyter Notebook.

The parsing folder contains files used to parse the data files provided, in addition to some of the code for examining outliers or homophily within the networks.

### Code

The data folder has no executable code, only information storage.

The model folder is separated by dataset. Each dataset folder has a class and link file that corresponds to node classification and link prediction respectively. Each file also uses some subset of GNN models provided by StellarGraph, DGL, or a GNN from scratch, sometimes separated into different files. Each file will open the file of the corresponding dataset to put it into a compatible format such as Pandas, then splitting the data into the appropriate training or testing sets of papers, classifications, and features for use on the models. Link prediction will use an edge splitter to create these partitions. As such, the allowable parameters for these files reflect those of a neural network - learning rate, epochs, dropout rate, batch size, and hidden layers can be changed in regards to their respective qualities. For example, learning rate is a positive floating point number that can be made smaller at the cost of run time, but larger values will limit performance. The number of epochs, batch size, and hidden layers (a pair of two integers in a vector) can also be set to any positive integer value for some trade-off between performance and run-time. Dropout rate can be set in the range of 0 to 1, with zero being no output and 1 being no dropout.

Each file also includes code for a visualization of the graph in NetworkX, where the parameters taken are visual, and thus can be changed according to personal preference.

For the wos folder, link prediction and node classification are done within the same file, while additional operations are included that are not for the other datasets. The updated WoS file uses a larger dataset, only analyzes the largest subcomponent of the graph, and applies additional operations as follows. T-sne is performed to provide a visualization of the classes of the dataset with a parameter of n_components=2, which is appropriate for 2-D visualizations. Other parameters were not explored but may be experimented with if desired. PCA is also performed to reduce the number of features in the model, since the original WoS dataset had well over 4000, having the potential for extra variance. PCA uses a parameter of n_components=0.8 to explain 80% variance. As such, this parameter can be changed within 0-1 to test the representation of different quantities of variance in the dataset, or a positive integer to reduce to a specific number of features. Other than that, the allowable parameters are similar to the other files.

The files for parsing take no parameters except for the file names for which they are associated. As such, different file formats may not be compatible with the specific files without reorganization or rewriting of code.

## Credits

Special thanks to Professor Radu Marculescu and Mustafa Munir for their continued support throughout the semester and their guidance in the project!

Provided Resource:
https://relational.fit.cvut.cz/dataset/CORA
https://relational.fit.cvut.cz/dataset/CiteSeer
https://www.dgl.ai/
https://arxiv.org/abs/1609.02907

Additional Resources:

- ‘Node Classification on Cora’, url: https://paperswithcode.com/sota/node-classification-on-cora.
- T. Ucar, ‘NESS: Node Embeddings from Static SubGraphs’, in arXiv, 2023, url: https://doi.org/10.48550/arXiv.2303.08958.
- L. Pan, C. Shi, and I. Dokmanić, ‘Neural Link Prediction with Walk Pooling’, in International Conference on Learning Representations 2022, 2022, url: https://doi.org/10.48550/arXiv.2110.04375.
- National Library of Medicine, ‘Pubmed’, url: https://relational.fit.cvut.cz/dataset/PubMed_Diabetes
- Clarivate, ‘Web of Science’, 2023, url: https://www.webofscience.com/wos/woscc/basic-search.
- A. D. Wade, ‘The semantic scholar academic graph (s2ag)’, in Companion Proceedings of the Web Conference 2022, 2022, pp. 739–739.
- A. Sinha et al., ‘An overview of microsoft academic service (mas) and applications’, in Proceedings of the 24th international conference on world wide web, 2015, pp. 243–246.
- Jo SH, Chang T, Ebong I, Bhadviya BB, Mazumder P, Lu W. ‘Nanoscale memristor device as synapse in neuromorphic systems,’ in Nano Lett., 10(4):1297-301, 2010, doi: 10.1021/nl904092h.
- V. Sze, Y. -H. Chen, T. -J. Yang and J. S. Emer, "Efficient Processing of Deep Neural Networks: A Tutorial and Survey," in Proceedings of the IEEE, vol. 105, no. 12, pp. 2295-2329, Dec. 2017, doi: 10.1109/JPROC.2017.2761740.
- Honnibal, M. & Montani, I., keyword-spaCy, Natural language understanding with Bloom embeddings, convolutional neural networks and incremental parsing, 2017, url: https://github.com/wjbmattingly/keyword-spacy
