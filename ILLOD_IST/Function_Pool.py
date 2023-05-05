#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import string
import jellyfish
import pandas as pd
import random
import math
import wordninja
import spacy
import re
import itertools
from spacy_syllables import SpacySyllables
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("syllables", after="tagger")

from spylls.hunspell import Dictionary
spellchecker = Dictionary.from_files('en_US')

from string import punctuation

################################# Helper Functions and Syntactic Similarity Measures

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
    if len(term.split()) < 2:
        return term
    else:
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

def levensthein_similarity_on_reduction_of_expansion(a, term, threshold):
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





############################################### ILLOD+

#def read_data_and_prepare_stop_words():
#    stop_words = set(["for", "and", "of", "in", "&", "via", "be", "over", "the", "et", "to"])
#
#    extensions_data = pd.read_csv('extension_pairs.csv', names=['original', 'extended'], sep=',', encoding='utf8')
#    orig = list(extensions_data['original'].values)
#    extended_words_raw = list(extensions_data['extended'].values)
#    extended_words = [w.strip() for w in extended_words_raw]
#    extension_dict = dict()
#    for i, key in enumerate(orig):
#        extension_dict[key] = extended_words[i]

#    stop_words = stop_words.union(set(extended_words))
#    return extension_dict, stop_words

#def extend_term(t):
#    t_clean = re.sub("(\w)(\W)(\w)", r"\1 \3", t)
#    t_splitted = t_clean.split()
#    t_splitted = list(filter(None, t_splitted))
#    for w in t_splitted:
#        if w in extension_dict.keys():
#            t_splitted = list(map(lambda x: x.replace(w, extension_dict[w]), t_splitted))
#    result = " ".join(w.strip() for w in t_splitted)
#    if len(result) >=2 and "ex" == result[:2].lower():
#        result = "xex" + result[2:]
#    return result


#extension_dict, stop_words = read_data_and_prepare_stop_words()



extension_cands = [("ex", "x_ex"), (" to ", " 2to "), (" one ", " 1one "), (" two ", " 2two "), (" three ", " 3three" ), 
(" one", " 1one"), (" two", " 2two"), ("-to-", "-2to-"), ("-one-", "-1one-"), ("-two-", "-2two-"),
("-three-", "-3three-" ), (" one", " 1one"), (" two", " 2two"), (" three", " 3three"), 
(" four", " 4four"), (" 1 ", " 1one "), (" 2 ", " 2two "), (" 3 ", " 3three "), (" and ", " &and "), 
(" & ", " &and "), (" & ", " &and "), (" + ", " +plus ")]

def extend_term(t):
    extended_t = t
    for pair in extension_cands:
        if pair[0] in t:
            extended_t = extended_t.replace(pair[0], pair[1])
    return extended_t


# PREPROCESSING
def lower_aep_candidate_pairs (a, t):
    return " ".join(w.lower().strip() for w in a.split()), " ".join(w.lower().strip() for w in t.split())


def clear_special_characters(s, replace_with_whitespace=None):
    if replace_with_whitespace:
        chars = re.escape(string.punctuation)
        s_ = re.sub(r'['+chars+']', ' ', s)
        return " ".join([w for w in s_.split()])
    else:
        invalidcharacters = set(string.punctuation)
        if any(char in invalidcharacters for char in s):
            s_ = s.lower().translate(str.maketrans('', '', string.punctuation))
            s_ = " ".join(w for w in s_.split())
        else:
            s_ = s
        return s_


def check_length_consistency(a, t):
    return len(t.split()) <= len(a) + 2


def check_initial_letters(abbv, term):
    initial_letters_of_tokens_of_t = ''.join([c[0] for c in term.split()])
    return initial_letters_of_tokens_of_t.lower() == abbv.lower()

def check_order_rtl(a, t):
    abbv_reversed = a.lower()[::-1]
    term_reversed = t.lower()[::-1]
    len_of_term = len(t)
    
    pos_memory = 0
    pos_memory_list = []
    order_matching_string_rev = ""
    first_letter_of_term_already_reached = False
    
    for j, char_from_abbv in enumerate(abbv_reversed):
        if j == len(abbv_reversed) - 1:
            if char_from_abbv == term_reversed[-1] and first_letter_of_term_already_reached:
                continue
            elif char_from_abbv == term_reversed[-1]:
                order_matching_string_rev = order_matching_string_rev + char_from_abbv
                pos_memory_list.append(0)
        else:
            for i, char_from_term in enumerate(term_reversed[pos_memory:]):
                remained_term_to_be_checked = term_reversed[pos_memory:]
                if char_from_abbv == char_from_term:
                    order_matching_string_rev = order_matching_string_rev + char_from_abbv
                    pos_memory = pos_memory + i + 1
                    pos_memory_list.append(len_of_term - pos_memory)
                    if i+1 == len(remained_term_to_be_checked):
                        first_letter_of_term_already_reached = True
                    break
                
    if order_matching_string_rev == abbv_reversed:
        return True, pos_memory_list[::-1]
    else:
        return False, pos_memory_list[::-1]

def check_order_ltr(a, t):
    abbv = a.lower()
    term = t.lower()
    
    pos_memory = 0
    pos_memory_list = []
    order_matching_string = ""
    
    for j, char_from_abbv in enumerate(abbv):
        for i, char_from_term in enumerate(term[pos_memory:]):
            if char_from_abbv == char_from_term:
                order_matching_string = order_matching_string + char_from_abbv
                pos_memory = pos_memory + i + 1 
                pos_memory_list.append(pos_memory-1)
                break
    return order_matching_string == abbv, pos_memory_list


def detect_all_valid_distributions(a, t, ltr_positions, rtl_positions):
    valid_distr = []
    for i, char_a in enumerate(a):
        left_bound_for_char_a = ltr_positions[i]
        right_bound_for_char_a = rtl_positions[i]
        findings_for_char_a = []
        for j, char_t in enumerate(t):
            if char_a == char_t and left_bound_for_char_a <= j and j <= right_bound_for_char_a:
                findings_for_char_a.append(j)
        valid_distr.append(findings_for_char_a)
    
    proper_valid_distributions = list(itertools.product(*valid_distr))
    filtered_valid_distributions = []
    for entry in proper_valid_distributions:
        if (all(entry[i] <= entry[i+1] for i in range(len(entry)-1))):
            filtered_valid_distributions.append(list(entry))
    return filtered_valid_distributions            



# Distribution PLus

def check_if_abbv_and_term_share_subsequence(position_list, minimum_lenth_of_shared_subsequence):
    copy_pl = position_list.copy()
    copy_pl.append(position_list[-1]+1)
    longest_consequtive_subsequence = []
    tmp_sequence = []
    pos_memory = 0
    for pos in copy_pl:
        if pos != pos_memory + 1:
            tmp_sequence = []
        elif pos == pos_memory + 1:
            tmp_sequence.append(pos_memory)
            if len(tmp_sequence) > len(longest_consequtive_subsequence):
                longest_consequtive_subsequence = tmp_sequence
        pos_memory = pos
    return len(longest_consequtive_subsequence)>=minimum_lenth_of_shared_subsequence        


def check_on_IL_of_syllables(a, t):
    term_ = re.sub('\d+', '', t)
    term_ = re.sub('\'', '', term_)
    doc = nlp(term_)
    syllables_list = [token._.syllables for token in doc]
    # print(syllables_list)
    syllables_list_flat = []
    for sl in syllables_list:
        for s in sl:
            syllables_list_flat.append(s)
    initial_letters_of_all_term_syllables = "".join(s[0].lower() for s in syllables_list_flat)
    return check_order_ltr(a, initial_letters_of_all_term_syllables)[0]


def check_distribution_on_token_syllables(term, sublist):
    abbv = "".join(term[pos] for pos in sublist)
    term_ = re.sub('\d+', '', term)
    term_ = re.sub('\'', '', term_)
    term_ = " ".join(w for w in wordninja.split(clear_special_characters(term_, replace_with_whitespace = True)))
    doc = nlp(term_)
    syllables_list = [token._.syllables for token in doc]
    syllables_list_flat = []
    for sl in syllables_list:
        for s in sl:
            syllables_list_flat.append(s)
    initial_letters_of_all_term_syllables = "".join(s[0].lower() for s in syllables_list_flat)
    return len(check_order_ltr(abbv.lower(), initial_letters_of_all_term_syllables)[1])==len(abbv)


def generate_containment_list(t, positions_of_char_from_a_in_t):
    splitted_term = t.split()
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
    
    containment_list = []
    for i, interval in enumerate(term_intervals):
        contanment_sublist = []
        for j, pos in enumerate(positions_of_char_from_a_in_t):
            if (pos in interval) and (splitted_term[i][0].lower() == t[pos].lower()) and j==0:
                contanment_sublist.append(0)
            elif (pos in interval) and (splitted_term[i][:2] == "x_" and t[pos] == "e"):
                contanment_sublist.append(0)
            elif pos in interval:
                contanment_sublist.append(interval.index(pos))
        if len(contanment_sublist) == 0:
            contanment_sublist.append(-1)
        containment_list.append(contanment_sublist)

    return containment_list


def check_if_distribution_fits(t, actual_position_list, containment_list, th):
    stop_words = set(["for", "and", "of", "in", "&", "via", "be", "&and", "over", "the", "et", "to", "2to"])
    splitted_term = t.split()
    a = "".join([t[pos] for pos in actual_position_list])
    if check_if_abbv_and_term_share_subsequence(actual_position_list, minimum_lenth_of_shared_subsequence = 4):
        return True
    
    result_of_distribution_check = False
    if len(containment_list) <= 1: #Regel 3
        t_ = " ".join(w for w in wordninja.split(clear_special_characters(t, replace_with_whitespace = True)))
        if t_ == t:
            if th ==-2:
                return check_on_IL_of_syllables(a, t_)
            else:
                return True
        else:
            a = "".join(t[p] for p in actual_position_list)
            return illod_plus(a, t_, th)
        
        
    elif len (containment_list) >= 2:
        
        non_zero_count = 0
        for i, sublist in enumerate(containment_list[1:]):
            if len(sublist) == 1 and 0 not in sublist:
                if splitted_term[i+1] not in stop_words: # Regel1 + Regel 2 
                    non_zero_count += 1
                if splitted_term[i+1] in stop_words and sublist[0] == len(splitted_term[i+1])-1: # Regel 2
                    non_zero_count += 1
                # NEU # Regel noch zu beschreiben, da Integration noch nicht sicher
                if sublist[0] == len(splitted_term[i+1])-1:
                    non_zero_count += 1
                # NEU END
            if len(sublist) > 1 and 0 not in sublist and i < len(containment_list)-1: # Regel 4
                if not check_distribution_on_token_syllables(splitted_term[i+1], sublist):
                    non_zero_count += 1
        if non_zero_count == 0:
            result_of_distribution_check = True
            
    return result_of_distribution_check


def check_if_good_distribution_exists(a, t, ltr_positions, rtl_positions, th):
    splitted_t = t.split()
    if ltr_positions != rtl_positions:
        list_of_valid_distributions = detect_all_valid_distributions(a, t, ltr_positions, rtl_positions)
        for distribution in list_of_valid_distributions:
            tmp_containment_list = generate_containment_list(t, distribution)
            if check_if_distribution_fits(t, distribution, tmp_containment_list, th):
                return True
        return False
    else:
        cont_list = generate_containment_list(t, rtl_positions)
        return check_if_distribution_fits(t, rtl_positions, cont_list, th)

def portion_of_capital_letters(w):
    upper_cases = ''.join([c for c in w if c.isupper()])
    return len(upper_cases)/len(w)
    
def illod_plus(a,t, th):
    if (a[0].lower() == t[0].lower()) or "ex" in t.lower():
        if len(a) > 15 and portion_of_capital_letters(a)>=0.9:
            return False
        
        a_, t_ = lower_aep_candidate_pairs(a, t)
        
        a_c, t_c = clear_special_characters(a_), clear_special_characters(t_)
        if a_c != a or t_c != t:
            if illod_plus(a_c,t_c, th):
                return True

        t_extended = extend_term(t_)
        if check_initial_letters(a_,t_) or check_initial_letters(a_, t_extended):
            return True
        


        rtl_order, rtl_positions = check_order_rtl(a_, t_extended)
        if rtl_order:
            ltr_order, ltr_positions = check_order_ltr(a_, t_extended)
            length_consistency = check_length_consistency(a_, t_extended)
            good_distribution_exists = check_if_good_distribution_exists(a_, t_extended, ltr_positions, rtl_positions, th)
            #return length_consistency and good_distribution_exists
            return good_distribution_exists
        else:
            return False
    else:
        return False


################################################ Overall Extraction of abbreviations


stop_words = ["the", "and", "i", "for", "as", "an", "a", "if", "any", "all", "one", "on",
              "new", "out", "we", "to", "at", "by", "from"]

def portion_of_capital_letters(w):
    upper_cases = ''.join([c for c in w if c.isupper()])
    return len(upper_cases)/len(w)

def check_if_word_is_capital_letter_abbv(word):
    if len(word) < 1:
        return False
    if (len(word) <= 13 and portion_of_capital_letters(word) >= 0.29):
        if len([c for c in word if c.isupper()]) == 1 and word[0].isupper() and word.lower() in stop_words:
            return False
        else:
            return True
    return False

def get_additional_candidates(req):
    m = re.findall(r"(?:\w+\.)+(?!$)", req)
    cleaned_list_of_candidates = [item for item in m if not spellchecker.lookup(item)]
    return cleaned_list_of_candidates

def check_if_word_is_lower_letter_abbv(word, candidates):
    if len(word)<=1 and word != "a":
        return True
    if (not spellchecker.lookup(' '.join(re.findall(r"[\w\-]+", word))) or
        word in candidates) and word.islower() and len(word) < 7:
        return True
    word = re.sub("(\w)(\W)(\w)", r"\1 \3", word)
    if len(word.split()) >= 2 and word[-1] != "s":
        return any([check_if_word_is_lower_letter_abbv(tok, candidates) for tok in word.split()])
    return False

def check_if_abbv(word, cands):
    return check_if_word_is_capital_letter_abbv(word) or check_if_word_is_lower_letter_abbv(word, cands)

def no_numbers_and_special_chars(abbv_cand):
    if not abbv_cand.isdigit():
        if not (len(abbv_cand) == 1 and not abbv_cand.isalnum()):
            #set_of_detected_abbreviations.add(cleaned_abbv.strip(punctuation))
            s = ''.join([i for i in abbv_cand if not i.isdigit()])
            if any([c.isalnum() for c in s]):
                return True
    return False


def extract_abbs(sents):
    set_of_detected_abbreviations = set()
    for sent in sents:
        cands = get_additional_candidates(sent)
        bigrams = [b for b in zip(sent.split(" ")[:-1], sent.split(" ")[1:])]
        redundancies = set()
        abbvs=set()
        for bigr in bigrams:
            if check_if_abbv(bigr[0], cands) and check_if_abbv(bigr[1], cands) and bigr[0] not in [".", ","]:
                if no_numbers_and_special_chars(bigr[0]) and no_numbers_and_special_chars(bigr[1]):
                    cleaned_abbv_from_brackets = re.sub(r"[\([{})\]]", "", bigr[0] + " " + bigr[1])
                    if ", " not in cleaned_abbv_from_brackets and ". " not in cleaned_abbv_from_brackets:
                        abbvs.add(cleaned_abbv_from_brackets.strip(punctuation))
                        redundancies.add(bigr[0])
                        redundancies.add(bigr[1])
        for word in sent.split():
            if check_if_abbv(word, cands):
                cleaned_abbv_from_brackets = re.sub(r"[\([{})\]]", "", word)
                if cleaned_abbv_from_brackets not in redundancies and no_numbers_and_special_chars(cleaned_abbv_from_brackets):
                    abbvs.add(cleaned_abbv_from_brackets.strip(punctuation))
        set_of_detected_abbreviations = set_of_detected_abbreviations.union(abbvs)
    return set_of_detected_abbreviations


##################### NC-Extraction + Generation of new validation input_data (100 uncontrolled abbreviations in PURE dataset)


def normalize_nc(nc):
    doc = nlp(nc)
    cleaned_nc = ""
    for token in doc:
        if token.pos_ != "DET" or token.text in ["such", ""]:
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
  
    term_pairs = []
    for original_term in found_terms:
        term_pairs.append((original_term, normalize_nc(original_term)))
    return set(term_pairs)




def generate_nc_to_reqID_map(data_list):
    nc_to_reqID_map = {}
    for sample in data_list[1:]:
        current_ID = sample[1] + "_" + sample[0]
        set_of_nc_tuples_in_sent = nc_detect(sample[2])

        for term_tuple in set_of_nc_tuples_in_sent:
            term = term_tuple[1]
            if term in nc_to_reqID_map.keys():
                ID_list_so_far = nc_to_reqID_map[term]
                if current_ID not in ID_list_so_far:
                    ID_list_so_far.append(current_ID)
                nc_to_reqID_map[term] = ID_list_so_far
            else:
                nc_to_reqID_map[term] = [current_ID]
    return nc_to_reqID_map




def replace_term_with_abb_in_given_req (req_text, cleaned_nc, abb):
    set_of_term_pairs = nc_detect(req_text)
    req_text_=""
    for item in set_of_term_pairs:
        if item[1] == cleaned_nc:
            req_text_ = req_text.replace(item[0], abb)
            break
    return req_text_


def replace_phrase_with_abb(nc_to_reqID_map, reqs_list, replacement_sample):
    list_of_term_occurances = nc_to_reqID_map[replacement_sample[0]]
    rand_int = random.randint(1, len(list_of_term_occurances)-1)
    random_pick_of_occurances = random.choices(list_of_term_occurances, k=rand_int)
    changed_data_dict = {}
    
    for _id in random_pick_of_occurances:
        for req in reqs_list:
            if req[1] + "_" +req[0] == _id:
                _new_req = replace_term_with_abb_in_given_req(req[2], replacement_sample[0], replacement_sample[1])
                changed_data_dict[_id] = _new_req
    
    updated_list = []
    for req in reqs_list:
        if req[1] + "_" +req[0] not in changed_data_dict.keys():
            updated_list.append(req)
        else:
            updated_list.append([req[0], req[1], changed_data_dict[req[1] + "_" +req[0]]])
    return updated_list




def create_uncontrolled_abbreviations_in_requirements(data_list, terms_to_be_replaced, number_of_abbreviations):
    nc_to_reqID_map = generate_nc_to_reqID_map(data_list)
    list_of_replacements = []
    for sample in terms_to_be_replaced:
        if not (sample[1] != sample[1]):
            if sample[0] in nc_to_reqID_map.keys()and len(nc_to_reqID_map[sample[0]]) >= 2:
                list_of_replacements.append(sample)
    list_of_replacements = random.sample(list_of_replacements, number_of_abbreviations)
    
    changed_data_list = data_list.copy()
    for r_sample in list_of_replacements:
        changed_data_list = replace_phrase_with_abb(nc_to_reqID_map, changed_data_list, r_sample)
    
    return changed_data_list, list_of_replacements 
