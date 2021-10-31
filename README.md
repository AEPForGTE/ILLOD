# ILLOD

ILLOD, a binary classifier for abbreviation-expansion detection. It checks wether two terms are compatible as abbreviation-expansion pair. It extends the algorithm of [1], that we re-implemented in Python to make it usable for cross-comparisons, where abbreviations and possible expansions appear in different sentences/ requirements. ILLOD checks initial letters, term lengths, order, and distribution of characters.

ILLOD is a feature based classifier and proves to be more accurate than approaches based on syntactic or semantic similarity. Therefore it can beneficially extend term clustering tools for synonym detection.

[1]  Schwartz, A.S., Hearst, M.A.: A simple algorithm for identifying abbreviation def-initions in biomedical text. In: Biocomputing 2003, pp. 451–462. World Scientific(2002)
