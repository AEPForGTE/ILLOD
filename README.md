# ILLOD: Tool for Term Consolidation

## What is it?
Providing precise definitions of all project specific terms is a crucial task in requirements engineering. In order to support the glossary building process, many previous tools rely on the assumption that the requirements set has a certain level of quality. Yet, the parallel detection and correction of quality weaknesses in the context of glossary terms is beneficial to requirements definition. We focus on detection of uncontrolled usage of abbreviations by identification of abbreviation-expansion pair (AEP) candidates. We compare our feature-based approach (ILLOD+) to other similarity measures to detect AEPs and propose how to extend the glossary term extraction (GTE) and synonym clustering with AEP-specific methods.

This repo provides data and evaluation results from our research in abbreviation-expansion pair detection for glossary term extraction (AEPForGTE). It also provides an implementation of ILLOD and its extension ILLOD+. In ILLOD+ the detection of AEPs is refined through recursive calls and a more sophisticated character distribution analysis, it achieves higher recall and precision. In ILLOD+ the detection of AEPs is refined through recursive calls and a more sophisticated character distribution analysis, it achieves higher recall and precision.

ILLOD is a binary classifier for abbreviation-expansion detection (it checks Initial Letters, term Lengths, Order, and Distribution of characters). It checks for two given terms whether they are compatible as abbreviation-expansion pair. It extends the algorithm of Schwartz and Hearst [1], that we re-implemented in Python to make it usable for cross-comparisons, where abbreviations and possible expansions appear in different sentences/ requirements.

ILLOD is a feature based classifier and proves to be more accurate than approaches based on syntactic or semantic similarity. Therefore, it can be a useful extension for term clustering tools for synonym detection.

This repo is organised as follows:

| DIRECTORY | DESCRIPTION |
| ------ | ------ |
| ILLOD_IST | Notebooks and Sources for IST Journal submission |
| ILLOD_REFSQ | Notebooks and Sources for REFSQ2022 conference submission |
| MAIN | Data and Sources for Reproduction Purposes |

## Artifact generation
This section explains how ILLOD artefacts can be generated and used on your local system.

### Summary
The MAIN directory contains all necessary data and implementations to install and run ILLOD on your local system.
By running the main script, two CSV files are created in the subdirectory MAIN/output.
- modified_requirements.csv
- evaluation_results.csv


### Description of Artifact

| FILE                    | DESCRIPTION                                               |
|-------------------------|-----------------------------------------------------------|
| input_data/pure_requirements.csv | A csv file containing 1934 requirements from PURE dataset |
| input_data/LF-SF_pairs.csv | A csv file containing 518 LF-SF pairs                     |
| main&#46;py             | The script that generates the output files                |
| src                     | Folder containing sources to run ILLOD and its evaluation |
| requirements.txt        | A text file containing the required dependencies          |

### System Requirements
To successfully run the ILLOD_RE artifact, the following system requirements must be met: 
- Python 3.8 or higher
- Pip (to install Python dependencies)
- All other required libraries will be installed automatically when running pip install -r requirements.txt.


### Steps to Reproduce
To reproduce the results presented in the paper, follow these steps:
Clone the repository:
```sh
git clone https://github.com/AEPForGTE/ILLOD
```
Navigate to the MAIN directory:
```sh
cd MAIN
```

Create a new virtual environment for the project:
```sh
python3 -m venv venv
```

Activate the virtual environment:
```sh
source venv/bin/activate
```

Install the required dependencies:
```sh
pip install -r requirements.txt
```

Nvigate to the root folder:
```sh
cd ..
```

Run the main&#46;py script to generate the output files:
```sh
python main.py
```

After running main.py, two new output files are created in the MAIN/output directory:

| FILE | DESCRIPTION |
| ------ | ------ |
| pure_modified_requirements.csv | A CSV file containing 1934 requirements from PURE dataset, where a given number of randomly chosen terms (long forms) were replaced by uncontrolled abbreviations (short forms).|
| evaluation_results.csv | A CSV file containing detailed evaluation results showing how the ILLOD approach performed on detecting the inserted abbreviations.|

By default, the main routine replaces 100 long forms with abbreviations. This value can be changed by modifying the NUM_OF_REPLACEMENTS variable in main&#46;py. Note that only values between 0 and 400 are allowed. 
