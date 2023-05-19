# ILLOD: Tool for Term Consolidation
## Summary
This repository provides data and evaluation results from our research in 
abbreviation-expansion pair (AEP) detection for glossary term extraction for 
requirements engineering documents. Corresponding research papers are availiable here:
[REFSQ2022 Conference](https://link.springer.com/chapter/10.1007/978-3-030-98464-9_6), [Elsevir IST Journal](https://www.sciencedirect.com/science/article/abs/pii/S0950584923000575).

This repository is organised as follows:

| DIRECTORY | DESCRIPTION                                                              |
| ------ |--------------------------------------------------------------------------|
| ILLOD_IST | Notebooks and Sources for IST Journal submission (Link to Readme)        |
| ILLOD_REFSQ | Notebooks and Sources for REFSQ2022 conference submission  (Link Readme) |
| MAIN | Data and Sources for Reproduction Purposes                               |

Steps needed to load and use the ILLOD (Initial Letters, term Lengths, Order, and Distribution of characters) 
artifact on your local system will be described below. The Artefact also enables the execution of 
ILLOD on individual user data without in-depth Python knowledge. 

## Description of Artifact
### Structure
The MAIN directory, which contains the essential parts of the ILLOD artifact, is structured as 
follows:

| SUBDIRECTORY | DESCRIPTION                                                                                                          |
|--------------|----------------------------------------------------------------------------------------------------------------------|
| input_data   | This subdirectory contains files on which ILLOD is executed to detect AEP groups.                                    |
| output_data  | After execution of ILLOD, this subdirectory will contain generated files with found AEP groups.                      |
| src          | Python sources to run ILLOD for reproduction purposes on requirements from PURE dataset and on additional user data. |

### Summary
This artifact contains data and methods (python sources) for evaluating the detection of 
abbreviation-expansion pairs (AEPs) in requirement sets. It involves replacing long-form terms with abbreviations from 
predefined lists to create changed requirement sets. 
The evaluation process aims to simulate uncontrolled abbreviation usage and test 
different classifiers. 

In [IST] the methods were applied to an experiment with 1934 requirements 
from the PURE dataset. Different individuals suggested abbreviations for a subset of 
abbreviations for 518 terms and an automated routine was used to substitute long-form terms 
with abbreviations. 

The following files are included in the ILLOD artifact:

| FILE                    | DESCRIPTION                                                                                                                                                                         |
|-------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| input_data/pure_requirements.csv | A csv file containing 1934 requirements from PURE dataset as describet in our [Elsevir IST Journal](https://www.sciencedirect.com/science/article/abs/pii/S0950584923000575) paper. |
| input_data/LF-SF_pairs.csv | A csv file containing the suggested abbreviations for 518 terms, extracted from "pure_requirements.csv".                                                                            |
| main&#46;py             | The script that generates the output files                                                                                                                                          |
| requirements.txt        | A text file containing the required dependencies                                                                                                                                    |


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

- The first function checks whether an additional file for AEP detection is stored in the input_data folder. It writes the list of detected AEP groups (Abbreviation Expansion Pairs) into the file "found_AEP_groups.json". 

- The 2nd function generates a modified version of the requirements data by replacing some terms with their corresponding abbreviations. By default, the main routine replaces 100 long forms with abbreviations. This value can be changed by modifying the NUM_OF_REPLACEMENTS variable in main.py. Note that only values between 0 and 400 are allowed.

- Finally, the 3rd function runs the ten fold validation function with the NUM_OF_REPLACEMENTS parameter to evaluate the performance of ILLOD on the modified requirements data. 


After running main&#46;py, two new output files are created in the MAIN/output directory. A third file is optionally generated when an additional file for AEP detection is placed in the input folder by the user.


| FILE                            | DESCRIPTION |
|---------------------------------| ------ |
| pure_modified_requirements.csv  | A CSV file containing 1934 requirements from PURE dataset, where a given number of randomly chosen terms (long forms) were replaced by uncontrolled abbreviations (short forms).|
| evaluation_results.csv          | A CSV file containing detailed evaluation results showing how the ILLOD approach performed on detecting the inserted abbreviations.|
| Optional: found_AEP_groups.json | JSON-encoded file that contains detected AEP groups from the additional file. |
