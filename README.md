# ILLOD
This git repo provides data and evaluation results from our research in abbreviation-expansion pair detection for glossary term extraction (AEPForGTE). It is intended to support the glossary building process for requirement specifications. It also provides an implementation of ILLOD.

ILLOD is a binary classifier for abbreviation-expansion detection (it checks Initial Letters, term Lengths, Order, and Distribution of characters). It checks for two given terms whether they are compatible as abbreviation-expansion pair. It extends the algorithm of [1], that we re-implemented in Python to make it usable for cross-comparisons, where abbreviations and possible expansions appear in different sentences/ requirements.

ILLOD is a feature based classifier and proves to be more accurate than approaches based on syntactic or semantic similarity.  Therefore, it can be a useful extension for term clustering tools for synonym detection.

The notebooks are arranged according to the chapter structure in the paper. The various tables and key figures presented and mentioned in the paper are computed here.  

[1]  Schwartz, A.S., Hearst, M.A.: A simple algorithm for identifying abbreviation definitions in biomedical text. In: Biocomputing 2003, pp. 451–462. World Scientific(2002)
