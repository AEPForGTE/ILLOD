#!/usr/bin/env python
# coding: utf-8

# In[1]:

import re
import spacy
nlp = spacy.load("en_core_web_sm")
from string import punctuation

stop_words = ["the", "and", "i", "for", "as", "an", "a", "if", "any", "all", "one", "on", "new", "out", "we", "to", "at", "by", "from"]

def portion_of_capital_letters(w):
    upper_cases = ''.join([c for c in w if c.isupper()])
    return len(upper_cases)/len(w)

def abbv_detect(sent):
    abv = set()
    for word in sent.split():
        if (len(word) <= 13 and portion_of_capital_letters(word) >= 0.29):
            if len([c for c in word if c.isupper()]) == 1 and word[0].isupper() and word.lower() in stop_words:
                continue
            abv.add(word.strip(punctuation))
    return abv

def normalize_nc(nc):
    doc = nlp(nc)
    cleaned_nc = ""
    for token in doc:
        if token.pos_ != "DET":
            cleaned_nc = cleaned_nc + " " + token.lemma_
            cleaned_nc = re.sub(r"[\([{})\]]", "", cleaned_nc)
            cleaned_nc = cleaned_nc.strip()
    return cleaned_nc

def nc_detect(req):
    noun_chunks_set = set()
    doc = nlp(req)
    for nc_ in doc.noun_chunks:
        noun_chunks_set.add(nc_.text)

    composed_terms = set()
    for nc1 in noun_chunks_set:
        for nc2 in noun_chunks_set:
            comp_term1 = nc1 + " of " + nc2
            comp_term2 = nc1 + " and " + nc2
            if comp_term1 in req:
                composed_terms.add(comp_term1)
            if comp_term2 in req:
                composed_terms.add(comp_term2)
    found_terms = noun_chunks_set.union(composed_terms)
    
    cleaned_terms = []
    for t in found_terms:
        cleaned_terms.append(normalize_nc(t))
    return set(cleaned_terms)

