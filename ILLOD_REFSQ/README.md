# ILLOD_REFSQ Repository

### Summary
The ILLOD approach was presented for the first time at REFSQ 2022 [1].


ILLOD functions as a feature-based classifier to match abbreviation-expansion pairs, outperforming 
approaches relying on syntactic or semantic similarity. It serves as a valuable enhancement for term clustering tools employed in synonym identification.

### Repository Structure
The notebooks in this repository are organized according to the chapter structure in the associated research paper. Each notebook computes the various tables and key figures mentioned in the paper. These experiments demonstrate ILLOD's ability to effectively extract abbreviations and match their expansions in real-world scenarios. Furthermore, ILLOD is well-suited for augmenting previous term clusters with clusters that combine AEP candidates.

### Usage
To use the AEPForGTE project and the ILLOD implementation, carry out steps (1) to (6), depending on the operating system, as described in the [README.md](https://github.com/AEPForGTE/ILLOD/blob/main/README.md)  in the root directory.

As seventh step start jupyter-notebook:
```sh
jupyter-notebook
```

- Review the notebooks in the repository to understand the research methodology and experiments conducted.
- Use the provided data and evaluation results to support glossary building processes for requirement specifications.
- Apply the ILLOD algorithm for abbreviation-expansion detection by utilizing the Python implementation provided.

Please refer to the associated research paper and code documentation for more detailed information on the project and implementation.

### References
[1] Hasso, H., Großer, K., Aymaz, I., Geppert, H., Jürjens, J. (2022). Abbreviation-Expansion Pair Detection for Glossary Term Extraction. In: Gervasi, V., Vogelsang, A. (eds) Requirements Engineering: Foundation for Software Quality. REFSQ 2022. Lecture Notes in Computer Science, vol 13216. Springer, Cham. DOI: [10.1007/978-3-030-98464-9_6](https://doi.org/10.1007/978-3-030-98464-9_6)


### License
Software under MIT License

Copyright (c) 2021-2022 Hussein Hasso, Katharina Großer, Iliass Aymaz, Hanna Geppert, Jan Jürjens

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
