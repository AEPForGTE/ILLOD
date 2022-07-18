#!/usr/bin/env python
# coding: utf-8

# In[7]:


import string

def clear_special_characters(s1, s2):
    invalidcharacters = set(string.punctuation)
    if any(char in invalidcharacters for char in s1):
        s1_ = s1.lower().translate(str.maketrans('', '', string.punctuation))
    else:
        s1_ = s1
    if any(char in invalidcharacters for char in s2):
        s2_ = s2.lower().translate(str.maketrans('', '', string.punctuation))
    else:
        s2_ = s2
    return s1_, s2_

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
    sanitized_abbv, sanitized_term = clear_special_characters(abb_lower, term_lower) 
    sanitized_term_without_stopswords = stop_words_handling(sanitized_term)
    initial_letters_of_tokens_of_sanitized_term_without_stopswords = ''.join([c[0] for c in sanitized_term_without_stopswords.split()])
    return sanitized_abbv, initial_letters_of_tokens_of_sanitized_term_without_stopswords, sanitized_term_without_stopswords

def check_initial_letters(a, t):
    initial_letters_of_tokens_of_t = ''.join([c[0] for c in t.split()])
    if initial_letters_of_tokens_of_t == a or initial_letters_of_tokens_of_t.upper() == a:
        return True
    
def check_length_consistency(a, t):
    length_consistency = False
    if len(t.split()) <= len(a):
        length_consistency = True
    return length_consistency

def check_order(a, t):
    abbv_reversed = a.lower()[::-1]
    term_reversed = t.lower()[::-1]
    len_of_term = len(t)
    
    pos_memory = 0
    pos_memory_list = []
    order_matching_string_rev = ""
    
    for j, char_from_abbv in enumerate(abbv_reversed):
        if j == len(abbv_reversed) - 1 and len(pos_memory_list) > 0 and pos_memory == len(term_reversed):
            break
        else:
            for i, char_from_term in enumerate(term_reversed[pos_memory:]):
                if char_from_abbv == char_from_term:
                    order_matching_string_rev = order_matching_string_rev + char_from_abbv
                    pos_memory = pos_memory + i + 1
                    pos_memory_list.append(len_of_term - pos_memory)
                    break
    if order_matching_string_rev == abbv_reversed:
        return True, pos_memory_list[::-1]
    else:
        return False, []

def check_distribution_of_matching_characters(pos_of_chars_list, t):
    term_intervals = []
    len_of_term = len(t)
    i = 0
    while i < len_of_term:
        sublist = []
        j = i
        while j < len_of_term and t[j] != " ":
            sublist.append(j)
            j = j+ 1
        i = j+1
        term_intervals.append(sublist)
        
    splitted_term = t.split()      
    
    containment_list = []
    for i, interval in enumerate(term_intervals):
        contanment_sublist = []
        for pos in pos_of_chars_list:
            if (pos in interval) and (splitted_term[i][0] == t[pos]):
                contanment_sublist.append(0)
            elif pos in interval:
                contanment_sublist.append(interval.index(pos))
        if len(contanment_sublist) == 0:
            contanment_sublist.append(-1)
        containment_list.append(contanment_sublist)
    
    result_of_distribution_check = False
    if len(containment_list) <= 1:
        result_of_distribution_check = True
    elif len (containment_list) >= 2:
        non_zero_count = 0
        for sublist in containment_list[1:]:
            if len(sublist) == 1 and 0 not in sublist:
                non_zero_count += 1
        if non_zero_count == 0:
            result_of_distribution_check = True
    
    return result_of_distribution_check


def illod(abbv, term, threshold=None):
    if (abbv[0].lower() == term[0].lower()):
        a_cleaned, t_cleaned, cleaned_t_without_stopswords = clean_string_pair_and_reduce_expansion(abbv, term)

        if check_initial_letters(abbv, term):
            return True

        if a_cleaned == t_cleaned:
            return True
        
        length_consistency = check_length_consistency(a_cleaned, cleaned_t_without_stopswords)
        order, pos_of_chars_list = check_order(a_cleaned, cleaned_t_without_stopswords)
        distribution = check_distribution_of_matching_characters(pos_of_chars_list, cleaned_t_without_stopswords)


        if length_consistency and order and distribution:
            return True
        else:
            return False
    else:
        return False

