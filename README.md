# ILLOD: Tool for Term Consolidation

## What is it?
Effective requirements engineering requires providing precise definitions for all project-specific terms. One of the critical tasks in this process is building a glossary. However, many existing tools for glossary term extraction assume a certain level of quality in the requirements set, which may not always be the case. Therefore, detecting and correcting quality weaknesses in the context of glossary terms is crucial to ensure successful requirements definition.

Our research focuses on detecting uncontrolled usage of abbreviations by identifying abbreviation-expansion pair (AEP) candidates. To achieve this, we have developed a feature-based approach called **ILLOD**, a binary classifier that checks **I**nitial **L**etters, term **L**engths, **O**rder, and **D**istribution of characters. Our method is aimed at extending glossary term extraction (GTE) and synonym clustering with AEP-specific methods. We have also compared our approach with other common similarity measures to evaluate its effectiveness.

This repository provides data and evaluation results from our research in AEP detection for glossary term extraction. We also offer an implementation of ILLOD and its extension, ILLOD+. It determines whether two given terms are compatible as an abbreviation-expansion pair. ILLOD is based on the algorithm of Schwartz and Hearst [SOURCE]. We re-implemented it in Python to enable cross-comparisons where abbreviations and possible expansions appear in different sentences or requirements.

ILLOD has proven to be more accurate than approaches based on syntactic or semantic similarity. Therefore, it can be a valuable extension for term clustering tools for synonym detection. ILLOD+ refines the detection of AEPs through recursive calls and a more sophisticated character distribution analysis, achieving higher recall and precision.

In summary, our approach provides an effective solution for detecting uncontrolled abbreviation usage, allowing for a more accurate glossary building process and improving the overall quality of requirements definition.

This repo is organised as follows:

| DIRECTORY | DESCRIPTION |
| ------ | ------ |
| ILLOD_IST | Notebooks and Sources for IST Journal submission |
| ILLOD_REFSQ | Notebooks and Sources for REFSQ2022 conference submission |
| MAIN | Data and Sources for Reproduction Purposes |

## Artifact generation
This section outlines the steps to generate and use the ILLOD (Initial Letters, term Lengths, Order, and Distribution of characters) artifact on your local system.

### Summary
The ILLOD artifact is generated by running the main script, which is located at the root directory. Running the script creates two CSV files in the MAIN/output subdirectory. The purpose of the artifact is to enable easy replication of the data and evaluation findings presented in our contribution to the IST Journal.

### Description of Artifact
The following files are included in the ILLOD artifact:
| FILE                    | DESCRIPTION                                               |
|-------------------------|-----------------------------------------------------------|
| input_data/pure_requirements.csv | A csv file containing 1934 requirements from PURE dataset |
| input_data/LF-SF_pairs.csv | A csv file containing 518 LF-SF pairs                     |
| main&#46;py             | The script that generates the output files                |
| requirements.txt        | A text file containing the required dependencies          |

### System Requirements
To run the ILLOD artifact, your system must meet the following requirements:
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

Running main&#46;py executes 3 tasks.

- The 1st task checks wether an additional file for AEP detection is given. It returns a list of detected AEP (Abbreviation Expansion Pairs) groups from that file.

- The 2nd task generates a modified version of the requirements data by replacing some terms with their corresponding abbreviations.

- Finally, the 3rd tasks runs the ten fold validation function with the NUM_OF_REPLACEMENTS parameter to evaluate the performance of ILLOD on the modified requirements data. 


After running main&#46;py, two new output files are created in the MAIN/output directory. A third file is optionally generated when an additional file for AEP detection is placed in the input folder by the user.


| FILE                            | DESCRIPTION |
|---------------------------------| ------ |
| pure_modified_requirements.csv  | A CSV file containing 1934 requirements from PURE dataset, where a given number of randomly chosen terms (long forms) were replaced by uncontrolled abbreviations (short forms).|
| evaluation_results.csv          | A CSV file containing detailed evaluation results showing how the ILLOD approach performed on detecting the inserted abbreviations.|
| Optional: found_AEP_groups.json | JSON-encoded file that contains detected AEP groups from the additional file. |



By default, the main routine replaces 100 long forms with abbreviations. This value can be changed by modifying the NUM_OF_REPLACEMENTS variable in main&#46;py. Note that only values between 0 and 400 are allowed. 

