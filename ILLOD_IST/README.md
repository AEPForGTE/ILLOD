# ILLOD_IST Repository

### Summary

This Git repository provides data and evaluation results from our research in abbreviation-expansion pair (AEP) detection for glossary term extraction (AEPForGTE). The project aims to support the glossary building process for requirement specifications and includes an implementation of ILLOD.

### ILLOD - Initial Letters, term Lengths, Order, and Distribution of characters
ILLOD is a binary classifier specifically designed for abbreviation-expansion detection. It checks the compatibility of two given terms as an abbreviation-expansion pair by considering their initial letters, term lengths, order, and distribution of characters. The algorithm builds upon the work presented in [1], which we re-implemented in Python to facilitate cross-comparisons where abbreviations and possible expansions appear in different sentences or requirements.


ILLOD operates as a feature-based classifier and has shown to be more accurate than approaches based on syntactic or semantic similarity. It provides a valuable extension for term clustering tools used in synonym detection.

### Repository Structure
The notebooks in this repository are organized according to the chapter structure in the associated research paper. Each notebook computes the various tables and key figures mentioned in the paper. These experiments demonstrate ILLOD's ability to effectively extract abbreviations and match their expansions in real-world scenarios. Furthermore, ILLOD is well-suited for augmenting previous term clusters with clusters that combine AEP candidates.

### Usage
To utilize the AEPForGTE project and ILLOD implementation, depending on your operating system run 
steps (1) to (6)
as described in the 
[README.md](https://github.com/AEPForGTE/ILLOD/blob/main/README.md) at the root.

As seventh step start jupyter-notebook:
```sh
jupyter-notebook
```

- Review the notebooks in the repository to understand the research methodology and experiments conducted.
- Use the provided data and evaluation results to support glossary building processes for requirement specifications.
- Apply the ILLOD algorithm for abbreviation-expansion detection by utilizing the Python implementation provided.

Please refer to the associated research paper and code documentation for more detailed information on the project and implementation.

### References
[1] Hasso, H., Großer, K., Aymaz, I., Geppert, H., Jürjens, J. (2023). Enhanced Abbreviation–Expansion Pair Detection for Glossary Term Extraction. In: Information and Software Technology, vol 159 (July 2023), p. 107203. ISSN: 0950-5849. DOI: [10.1016/j.infsof.2023.107203](https://doi.org/10.1016/j.infsof.2023.107203)

### License
Software under MIT License

Copyright (c) 2022-2023 Hussein Hasso, Katharina Großer, Iliass Aymaz, Hanna Geppert, Jan Jürjens

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
