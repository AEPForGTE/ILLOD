"""
The code reads in a CSV file containing requirements and extracts abbreviations from the requirements.
It then identifies terms that appear in the requirements and categorizes them as either containing an abbreviation or not.
The code then loops through each abbreviation and identifies terms that match the abbreviation,
either by containing the abbreviation or by having a match between the abbreviation and the term using a certain function.
The matched terms are then added to a dictionary with the abbreviation as the key.
Finally, the dictionary is printed and converted into a pandas DataFrame before being returned.
"""

from ILLOD_IST import Function_Pool
import pandas as pd
from os import listdir
from os.path import isfile, join

def check_for_additional_tasks():
    path = "MAIN/input_data/"
    file_names = [f for f in listdir(path) if isfile(join(path, f))]
    if len(file_names) == 3:
        file_names.remove('LF-SF_Pairs.csv')
        file_names.remove('pure_requirements.csv')
        file_to_be_checked = file_names[0]
        return detect_aep_groups(path+"/"+ file_to_be_checked)
    else:
        return None


def detect_aep_groups(file_path):
    data = pd.read_csv(file_path, names=['ID', 'requirement'], sep=';', encoding='utf8')
    data_list = data['requirement'].to_list()

    abbreviations = Function_Pool.extract_abbs(data_list)
    terms = set()
    for req in data_list:
        current_term_tuples = Function_Pool.nc_detect(req)
        ots  = [t[1] for t in current_term_tuples]
        terms = terms.union(set(ots))

    terms_with_abbs = []
    ordinary_terms = []
    for term in terms:
        abbv_not_found = True
        for token in term.split():
            if Function_Pool.check_if_abbv(token, []) and len(token)>=2:
                terms_with_abbs.append(term)
                abbv_not_found = False
        if abbv_not_found and len(token)>=2:
            ordinary_terms.append(term)


    result_dict = {}
    for abbv in abbreviations:
        aep_candidates = []
        for term in ordinary_terms:
            if Function_Pool.illod_plus(abbv, term, -1):
                aep_candidates.append(term)
        for term in terms_with_abbs:
            if abbv in term and len(term) > len(abbv):
                aep_candidates.append(term)
        if len(aep_candidates) > 0:
            result_dict[abbv] = aep_candidates

    return result_dict