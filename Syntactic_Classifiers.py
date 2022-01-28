#!/usr/bin/env python
# coding: utf-8

# In[11]:


import string
import jellyfish


def dice_coefficient(a, b):
    """dice coefficient 2nt/(na + nb)."""
    a_bigrams = set(a.lower())
    b_bigrams = set(b.lower())
    overlap = len(a_bigrams & b_bigrams)
    return overlap * 2.0 / (len(a_bigrams) + len(b_bigrams))


def clean_string(s):
    s_lower = s.lower()
    invalidcharacters = set(string.punctuation)
    if any(char in invalidcharacters for char in s):
        s_ = s_lower.translate(str.maketrans('', '', string.punctuation))
    else:
        s_ = s_lower
    return s_


def stop_words_handling(term):
    splitted_term = term.split()
    stop_words = set(["for", "and", "of", "in", "via", "be"])
    if splitted_term[0] in stop_words:
        stop_words = stop_words - set([splitted_term[0]])
    for sw in stop_words:
        while sw in splitted_term:
            splitted_term.remove(sw)
    sanitized_term = " ".join([w for w in splitted_term]) 
    return sanitized_term


def clean_string_pair_and_reduce_expansion(abb, term):
    abb_lower = abb.lower()
    term_lower = term.lower()
    sanitized_abbv = clean_string(abb_lower)
    sanitized_term = clean_string(term_lower)   
    sanitized_term_without_stopswords = stop_words_handling(sanitized_term)
    initial_letters_of_tokens_of_sanitized_term_without_stopswords = ''.join([c[0] for c in sanitized_term_without_stopswords.split()])
    return sanitized_abbv, initial_letters_of_tokens_of_sanitized_term_without_stopswords


def levensthein_distance_on_reduction_of_expansion(a, term, threshold):
    a_, t_ = clean_string_pair_and_reduce_expansion(a, term)
    return jellyfish.levenshtein_distance(a_, t_) <= threshold

def levensthein_similarity(a, term, threshold):
    a_, t_ = clean_string_pair_and_reduce_expansion(a, term)
    return 1 - (jellyfish.levenshtein_distance(a_, t_)/ max(len(a_), len(t_))) >= threshold
    
def jaro_winkler_similarity_on_reduction_of_expansion(a, term, threshold):
    a_, t_ = clean_string_pair_and_reduce_expansion(a, term)
    return jellyfish.jaro_winkler_similarity(a_, t_) >= threshold

    
def dice_coefficient_on_reduction_of_expansion(a, term, threshold):
    a_, t_ = clean_string_pair_and_reduce_expansion(a, term)
    return dice_coefficient(a_, t_) >= threshold


	
def ld_classifier(a, term):
    a_, t_ = clean_string_pair_and_reduce_expansion(a, term)
    return jellyfish.levenshtein_distance(a_, t_) <= 1.0

    
def jws_classifier(a, term):
    a_, t_ = clean_string_pair_and_reduce_expansion(a, term)
    return jellyfish.jaro_winkler_similarity(a_, t_) >= 0.79

    
def dc_classifier(a, term):
    a_, t_ = clean_string_pair_and_reduce_expansion(a, term)
    return dice_coefficient(a_, t_) >= 0.76


