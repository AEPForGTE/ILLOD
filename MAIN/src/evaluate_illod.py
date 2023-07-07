from ILLOD_IST import Function_Pool
from ILLOD_IST import ILLOD
import time
import os
import pandas as pd

dirname = os.path.dirname(__file__)
dirOfdir = os.path.split(dirname)[0]
tailOfReqDataPath = "/input_data/pure_requirements.csv"
requirementsFilePath = str(dirOfdir) + str(tailOfReqDataPath)
tailOfReplacementDataPath = "/input_data/LF-SF_Pairs.csv"
replacementDataFilePath = str(dirOfdir) + str(tailOfReplacementDataPath)


def generate_aep_candidates_and_groups(found_abbs,
                                       ordinary_terms,
                                       terms_that_contain_abbs,
                                       aep_classifier,
                                       threshold):
    dict_for_aep_groups = {}
    for a in found_abbs:
        for ot in ordinary_terms:
            if aep_classifier(a, ot, threshold):
                if a in dict_for_aep_groups.keys():
                    dict_for_aep_groups[a].append(ot)
                else:
                    dict_for_aep_groups[a] = [ot]

    for a in found_abbs:
        for ttca in terms_that_contain_abbs:
            if a in ttca.split():
                if a in dict_for_aep_groups.keys():
                    dict_for_aep_groups[a].append(ttca)
                else:
                    dict_for_aep_groups[a] = [ttca]
    return dict_for_aep_groups


def evaluate_aep_detection_approach(found_abbreviations, list_of_replacements, ordinary_terms, terms_that_contain_abbs, clf, threshold):
    start_time = time.time()
    dict_for_aep_groups = generate_aep_candidates_and_groups(found_abbreviations,
                                                             ordinary_terms,
                                                             terms_that_contain_abbs,
                                                             clf,
                                                             threshold)
    end_time = time.time()
    duration = end_time - start_time
    abbreviations_detected = []
    matched_pairs = []
    for aep in list_of_replacements: # inserted_abbreviations is a global variable
        if aep[1] in dict_for_aep_groups.keys():
            abbreviations_detected.append(aep[1])
            if aep[0] in dict_for_aep_groups[aep[1]]:
                matched_pairs.append(aep)
    abbv_set_of_inserted_abbvs = set([p[1] for p in list_of_replacements])
    missed_abbreviations = abbv_set_of_inserted_abbvs - found_abbreviations

    sum_of_lengths = 0
    for key in dict_for_aep_groups.keys():
        sum_of_lengths = sum_of_lengths + len(dict_for_aep_groups[key])
    average_size_of_AEP_group = sum_of_lengths/len(dict_for_aep_groups.keys())
    cost_effectiveness = average_size_of_AEP_group/len(matched_pairs)
    return (len(dict_for_aep_groups),
            len(abbreviations_detected),
            len(missed_abbreviations),
            len(matched_pairs),
            average_size_of_AEP_group,
            cost_effectiveness,
            duration)


def determine_sets_for_term_types(set_of_abbreviations, set_of_terms):
    # compliant with section 7.2: terms_that_contain_abbreviations = T \ OT
    set_of_cleaned_terms = set([term_tuple[1] for term_tuple in set_of_terms])
    terms_that_contain_abbreviations = set()

    for term in set_of_cleaned_terms:
        for abb in set_of_abbreviations:
            if abb in term.split():
                terms_that_contain_abbreviations.add(term)

    ordinary_terms = set_of_cleaned_terms - terms_that_contain_abbreviations

    return ordinary_terms, terms_that_contain_abbreviations


def ten_fold_validation(number_of_replacements):
    data = pd.read_csv(requirementsFilePath, names=['ID', 'dataset', 'requirement'], sep=';', encoding='utf8')
    data_list = data.values.tolist()
    replacement_data = pd.read_csv(replacementDataFilePath, names=['term', 'abbv'], sep=';', encoding='utf8')
    aeps_to_replace = replacement_data.values.tolist()
    print("Running iterations for 10-fold validation ...")

    overall_results = []
    for i in range(0, 10):
        print("iteration number: " + str(i+1))
        uncontr_aeps_data, list_of_replacements = \
            Function_Pool.create_uncontrolled_abbreviations_in_requirements\
                (data_list, aeps_to_replace, number_of_replacements)
        terms = set()
        for req in uncontr_aeps_data:
            terms = terms.union(Function_Pool.nc_detect(req[2]))
        found_abbreviations = Function_Pool.extract_abbs([req[2] for req in uncontr_aeps_data])
        ordinary_terms, terms_that_contain_abbs = determine_sets_for_term_types(found_abbreviations, terms)
        result_memo = []
        th_list = [0.52, 0.76, 0.70, -1, -1, -2]
        for j, clf in enumerate([Function_Pool.levensthein_similarity_on_reduction_of_expansion,
            Function_Pool.jaro_winkler_similarity_on_reduction_of_expansion,
            Function_Pool.dice_coefficient_on_reduction_of_expansion,
            ILLOD.illod,
            Function_Pool.illod_plus,
            Function_Pool.illod_plus]):
            result_memo.append(evaluate_aep_detection_approach(found_abbreviations,
                                                               list_of_replacements,
                                                               ordinary_terms,
                                                               terms_that_contain_abbs,
                                                               clf,
                                                               threshold = th_list[j]))
        overall_results.append(result_memo)
    print(overall_results)

    approaches = ["LD", "JWS", "DC", "ILLOD", "ILLOD_A", "ILLOD_B"]
    output_list =[]
    for result in overall_results:
        for i, subresult in enumerate(result):
            d = {}
            d["Approach"] = approaches[i]
            d["Number of AEP groups"] = subresult[0]
            d["found abbreviations"] = subresult[1]
            d["missed abbreviations"] = subresult[2]
            d["matched abbreviations"] = subresult[3]
            d["Size of AEP groups"] = subresult[4]
            d["Cost Effectiveness"] = subresult[5]
            d["Duration"] = subresult[6]
            output_list.append(d)
    df = pd.DataFrame.from_dict(output_list)
    return df
