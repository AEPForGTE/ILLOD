# ILLOD: Tool for Term Consolidation
## Overview
This repository provides data, methods (python sources) and evaluation results for the detection 
of abbreviation-expansion pairs (AEPs) in requirement sets, specifically for glossary term 
extraction in requirements engineering documents. The corresponding research papers are availiable 
here:
[REFSQ2022 Conference](https://link.springer.com/chapter/10.1007/978-3-030-98464-9_6), [Elsevir IST Journal](https://www.sciencedirect.com/science/article/abs/pii/S0950584923000575).

This repository is organised as follows:

| DIRECTORY | DESCRIPTION                                       |
| ------ |---------------------------------------------------|
| ILLOD_IST | Notebooks and Sources for [IST article](https://www.sciencedirect.com/science/article/abs/pii/S0950584923000575).            |
| ILLOD_REFSQ | Notebooks and Sources for REFSQ2022 contribution. |
| MAIN | Data and Sources for Reproduction Purposes        |

Instructions for loading and using the ILLOD (Initial Letters, term Lengths, Order, and Distribution of characters) artifact on your local system will be described below. The artifact also allows the execution of ILLOD on individual user data without requiring in-depth Python knowledge.

## Description of Artifact
### Summary 
This artifact includes data and methods (python sources) to run the following steps:

1) Replace long-form terms with abbreviations from predefined lists to create a modified 
requirement set.


2) Execute and evaluate different classifiers for AEP detection, using the modified 
requirement set.


3) Optionally, the artifact allows for extraction of AEP groups (clusters that link a single 
abbreviation with all the potential expansions associated with that abbreviation) from a user-specified file. For this, the user-specified file must be csv-formatted and contain the columns "ID" and "requirement", which are separated by a semicolon ";". 
This file has to be placed in the input_data folder.

Step (1) aims to simulate a scenario where the requirement set has a large number of undefined 
abbreviations, thereby representing a weak requirements set qualitatively.
The evaluation process (2) assesses the performance of these classifiers in detecting AEPs.

In the specific context of our [IST](https://www.sciencedirect.com/science/article/abs/pii/S0950584923000575) paper, the methods described in the artifact were 
applied to an experiment involving 1934 requirements from the [PURE](https://ieeexplore.ieee.org/document/8049173) dataset. Different individuals suggested abbreviations for a subset of 518 terms, and an automated routine was used to replace long-form terms with the corresponding abbreviations.


### Structure
The MAIN directory, which contains the essential parts of the ILLOD artifact, is structured as 
follows:

| SUBDIRECTORY | DESCRIPTION                                                                                                                                                                                         |
|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| input_data   | This subdirectory contains files needed to run (1) and (3)                                                                                                                                          |
| output_data  | After execution of ILLOD, this subdirectory will contain generated files with found AEP groups (clusters that link a single abbreviation with all the potential expansions associated with that abbreviation). |
| src          | Python sources to run ILLOD for reproduction purposes on requirements from PURE dataset and on additional user data.                                                                                |


The following files are included in the ILLOD artifact:

| FILE                    | DESCRIPTION                                                                                                                                                                  |
|-------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| input_data/pure_requirements.csv | A csv file containing 1934 requirements from PURE dataset as describet in the [IST](https://www.sciencedirect.com/science/article/abs/pii/S0950584923000575) paper.          |
| input_data/LF-SF_pairs.csv | A csv file with the proposed abbreviations (also referred to as SF or short forms) for 518 terms (referred to as LF or long forms), extracted from "pure_requirements.csv".. |
| main&#46;py             | The script that generates the output files                                                                                                                                   |
| requirements.txt        | A text file containing the required dependencies to run the artifact locally.                                                                                                |


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

### Results

Running main&#46;py executes 3 subroutines.

- The first function generates a modified version of the requirements data by replacing some terms 
  with their corresponding abbreviations. By default, the main routine replaces 100 long forms with abbreviations. This value can be changed by modifying the NUM_OF_REPLACEMENTS variable in main.py. Note that only values between 0 and 400 are allowed.

- The 3rd function runs the ten fold validation function with the NUM_OF_REPLACEMENTS parameter 
  to evaluate the performance of ILLOD on the modified requirements data. 

- Finally, the third function checks whether an additional file for AEP detection is stored in the 
  input_data folder. It writes the list of detected AEP groups (Abbreviation Expansion Pairs) into the file "found_AEP_groups.json". 


After running main&#46;py, two new output files are created in the MAIN/output directory. Optionally, a third file is generated when an additional file for AEP detection is placed in the input_data folder by the user.

| FILE                            | DESCRIPTION |
|---------------------------------| ------ |
| pure_modified_requirements.csv  | A CSV file containing 1934 requirements from PURE dataset, where a given number of randomly chosen terms (long forms) were replaced by uncontrolled abbreviations (short forms).|
| evaluation_results.csv          | A CSV file containing detailed evaluation results showing how the ILLOD approach performed on detecting the inserted abbreviations.|
| Optional: found_AEP_groups.json | JSON-encoded file that contains detected AEP groups from the additional file. |

## How to Cite

If you find this work useful and want to cite it in your research, you can use the following format:

## License

Software under MIT License

Copyright (c) 2022-2023

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

All non-software data files within the project are published under the CC-BY 4.0 license (https://creativecommons.org/licenses/by/4.0/)
