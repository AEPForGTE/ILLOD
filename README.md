# ILLOD: A Tool for Abbreviation-Expansion Pair Detection<br> in Natural Language Requirements

This repository provides methods (python sources), data, and evaluation results for the detection 
of abbreviation-expansion pairs (AEPs) in requirement sets, specifically for glossary term 
extraction and consolidation in requirement documents. 
This includes the identification of potential abbreviations with various styles in the requirements texts.
For AEP detection, the ILLOD(+) tool identifies 
if a term is a potential long form to a given abbreviation
based on syntactic features of both terms, i.a. **I**nitial **L**etters, term **L**engths, **O**rder, and **D**istribution of characters.
Corresponding research papers that discuss this approach are available 
here:
REFSQ2022 Conference [[1]](https://link.springer.com/chapter/10.1007/978-3-030-98464-9_6), IST Journal [[2]](https://www.sciencedirect.com/science/article/abs/pii/S0950584923000575).

The content provided can be used as follows:
 - to reproduce results presented in [[1]](https://link.springer.com/chapter/10.1007/978-3-030-98464-9_6) and [[2]](https://www.sciencedirect.com/science/article/abs/pii/S0950584923000575)
 - to use ILLOD(+) to detect AEPs
 - to use the provided algorithm for abbrevation detection
 - to retrieve and use the input data-set for other research with AEPs in requirements engineering or other contexts

The repository is organised as follows:

| DIRECTORY | DESCRIPTION                                       |
| ------ |---------------------------------------------------|
| MAIN | Data and sources to run ILLOD(+) and further AEP classifiers as well as experiments for their evaluation ([[2]](https://www.sciencedirect.com/science/article/abs/pii/S0950584923000575)) (depends on ILLOD_IST)        |
| ILLOD_IST | Notebooks and sources for experiments presented in [[2]](https://www.sciencedirect.com/science/article/abs/pii/S0950584923000575)           |
| ILLOD_REFSQ | Notebooks and sources for experiments presented in [[1]](https://link.springer.com/chapter/10.1007/978-3-030-98464-9_6) |

Instructions for loading and using ILLOD(+) on your local system will be described below. It is possible to execute ILLOD(+) on individual user data without requiring in-depth Python knowledge.

## Description
### Summary 
This repository includes data and methods (python sources) to run the following steps:

1) **Create a test data-set:** Replace long-form terms in a requirement set with abbreviations from predefined lists to create a modified 
requirement set.


2) **Replicate Evaluation:** Execute and evaluate different classifiers for AEP detection, using the modified 
requirement set based on the analysis of AEP group creation (clusters that link a single 
abbreviation with all the potential expansions associated with that abbreviation).


3) **Use ILLOD for custom data-set:** Optionally, extract AEP groups from a user-specified file.

Step (1) aims to simulate a scenario where the requirement set has a large number of undefined and uncontrolled
abbreviations, thereby representing a requirements set of weak quality.
The data provided consists of 1934 requirements from the [PURE](https://ieeexplore.ieee.org/document/8049173) dataset and a list of abbreviations for a subset of 518 terms extracted from those. The abbreviations are suggested by different persons in an uncontrolled way. 
An automated routine can be used to replace random long-form terms from the list with the corresponding abbreviations and create a testset that contains requirements with long and short forms respectively.
Such a dataset was used for the experiments on requirements texts presented in [[2]](https://www.sciencedirect.com/science/article/abs/pii/S0950584923000575) and can be generated for replication.
Where to find the respective files in the repository structure is described below.
In addition, the *ILLOD_REFSQ* subdirectory contains with *insertedAbbreviations.txt* a shorter list of 30 AEPs and with *Promise_constructed.CSV* a data-set where these long forms where replaced manually in requirements from the [PROMISE NFR dataset](http://ctp.di.fct.unl.pt/RE2017/downloads/datasets/nfr.arff) for the pilot experiment in [[1]](https://link.springer.com/chapter/10.1007/978-3-030-98464-9_6).
Further, both publication specific subdirectories contain *abbr_db.CSV* a list of 1786 AEPs from the field of information technology ((https://www.computerhope.com/jargon/acronyms.htm)), which was used for initial abbreviation detection optimization and to generate a synthetic data-set of AEPs hidden in unrelated text. 
 

Step (2) is the evaluation to assess the performance of different classifiers in detecting AEPs on a modified requirement data-set:
- LD (based on Levenshtein-Distance)
- JWS (based on Jaro–Winkler-Similarity)
- DC (based on Dice-Coefficient)
- FT (based on [FastText](http://dx.doi.org/10.1162/tacl_a_00051)) --- not included to main experiment
- ILLOD
- ILLOD+ A (ILLOD with recursive calls and extended character distribution analysis)
- ILLOD+ B (ILLOD+ A with syllable analysis)

In all cases this includes the same method to detect abbreviation candidates in the texts. (The version in *ILLOD_REFSQ* is simpler and does not cover small caps forms and bi-grams)

The following parameter are evaluated
- Number of AEP groups (abbreviations with at least one expansion candidate)
- Number of missed abbreviations (detection recall)
- Number of found abbreviations (inserted abbreviations with own AEP group)
- Number of matched abbreviations (total recall)
- Size of AEP groups
- Cost Effectiveness
- Duration of execution

Simple precision and recall can only be calculated for the synthetic dataset, where all true and false positive assignments are known and no additional "noise" abbreviations or expansion candidates come from other parts of the text. Here, the FastText-based classifier is included to the experiments, but shows long execution time and poor performance (c.f. *5) Section_6.4 -- Table_3.ipynb*) in the publication specific sub-directories).

Step (3) allows to use ILLOD for other datasets. For this, the user-specified file must be csv-formatted and contain the columns "ID" and "requirement", which are separated by a semicolon ";". 
This file has to be placed in the input_data folder.


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
| input_data/pure_requirements.csv | A csv file containing 1934 requirements from PURE dataset as describet in [[2]](https://www.sciencedirect.com/science/article/abs/pii/S0950584923000575)          |
| input_data/LF-SF_pairs.csv | A csv file with the proposed abbreviations (referred to as SF/short forms) for 518 terms (referred to as LF/long forms), extracted from *pure_requirements.csv* |
| main&#46;py             | The script that generates the output files                                                                                                                                   |
| requirements.txt        | A text file containing the required dependencies to run the artifact locally                                                                                                |


### System Requirements
To run ILLOD and the experiments, your system must meet the following requirements:
- On Linux:
    - Python 3.10
    - Pip 22.0.2
    - All other required libraries will be installed automatically when running pip install -r requirements_lin.txt.
- On Windows:
    - Python 3.11
    - Pip 23.1.2
    - All other required libraries will be installed automatically when running pip install -r requirements_win.txt.

All input datafiles are provided as .csv files that can be accesses by text or spreadsheet editor.

### Steps to Reproduce on Linux
To reproduce the results presented in the paper [[2]](https://www.sciencedirect.com/science/article/abs/pii/S0950584923000575), follow these steps:
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
python3 -m venv illod_venv
```

Activate the virtual environment:
```sh
source illod_venv/bin/activate
```

Install the required dependencies:
```sh
pip install -r requirements_lin.txt
```

Navigate to the root folder:
```sh
cd ..
```

Run the main&#46;py script to generate the output files:
```sh
python main.py
```

### Steps to Reproduce on Windows
To reproduce the results presented in the paper [[2]](https://www.sciencedirect.com/science/article/abs/pii/S0950584923000575), follow these steps:
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
python -m venv illod_venv
```

Activate the virtual environment:
```sh
.\illod_venv\Scripts\activate
```

Install the required dependencies:
```sh
pip install -r requirements_win.txt
```
Navigate to the root folder:
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

- The second function runs the ten fold validation function with the NUM_OF_REPLACEMENTS parameter 
  to evaluate the performance of ILLOD on the modified requirements data. 

- Finally, the third function checks whether an additional file for AEP detection is stored in the 
  input_data folder. It writes the list of detected AEP groups (Abbreviation Expansion Pairs) into the file "found_AEP_groups.json". 


After running main&#46;py, two new output files are created in the MAIN/output directory. Optionally, a third file is generated when an additional file for AEP detection is placed in the input_data folder by the user.

| FILE                            | DESCRIPTION |
|---------------------------------| ------ |
| pure_modified_requirements.csv  | A CSV file containing 1934 requirements from PURE dataset, where a given number of randomly chosen terms (long forms) were replaced by uncontrolled abbreviations (short forms).|
| evaluation_results.csv          | A CSV file containing detailed evaluation results showing how the ILLOD approach performed on detecting the inserted abbreviations.|
| Optional: found_AEP_groups.json | JSON-encoded file that contains detected AEP groups from the additional file. |

As substituted long forms are randomly choosen, the actual result values differ from those presented in [[2]](https://www.sciencedirect.com/science/article/abs/pii/S0950584923000575). However, the general average performance over several runs should remain comparable.
Values as presented in the paper can be found in the respective notebooks within the paper specific sub-directories, together with those for the syntetic experiment.
Yet, again, if executed again, values based on random selections will change in these notebooks, too.

## Related Publications

[1] Hasso, H., Großer, K., Aymaz, I., Geppert, H., Jürjens, J. (2022). Abbreviation-Expansion Pair Detection for Glossary Term Extraction. In: Gervasi, V., Vogelsang, A. (eds) Requirements Engineering: Foundation for Software Quality. REFSQ 2022. Lecture Notes in Computer Science, vol 13216. Springer, Cham. DOI: [10.1007/978-3-030-98464-9_6](https://doi.org/10.1007/978-3-030-98464-9_6)

[2] Hasso, H., Großer, K., Aymaz, I., Geppert, H., Jürjens, J. (2023). Enhanced Abbreviation–Expansion Pair Detection for Glossary Term Extraction. In: Information and Software Technology, vol 159 (July 2023), p. 107203. ISSN: 0950-5849. DOI: [10.1016/j.infsof.2023.107203](https://doi.org/10.1016/j.infsof.2023.107203)

## How to Cite

If you find this work useful and want to cite it in your research, you can use the following format:

Hasso, H., Großer, K., Aymaz, I., Geppert, H., Jürjens, J. (2023). ILLOD: Tool for Term Consolidation. DOI:

## License

Software under MIT License

Copyright (c) 2022-2023 Hussein Hasso, Katharina Großer, Iliass Aymaz, Hanna Geppert, Jan Jürjens

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
