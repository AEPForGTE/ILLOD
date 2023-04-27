import pandas as pd
from ILLOD_RE.src import functionsPool
import os

dirname = os.path.dirname(__file__)
dirOfdir = os.path.split(dirname)[0]
tailOfReqDataPath = "/data/pure_requirements.csv"
requirementsFilePath = str(dirOfdir) + str(tailOfReqDataPath)
tailOfReplacementDataPath = "/data/SF-LF-Pairs.csv"
replacementDataFilePath = str(dirOfdir) + str(tailOfReplacementDataPath)


def generate_modified_requirements(number_of_replacements):
    data = pd.read_csv(requirementsFilePath, names=['ID', 'dataset', 'requirement'], sep=';', encoding='utf8')
    data_list = data.values.tolist()

    replacement_data = pd.read_csv(replacementDataFilePath, names=['term', 'abbv'], sep=';', encoding='utf8')
    aeps_to_replace = replacement_data.values.tolist()

    uncontr_aeps_data_as_dict  = functionsPool.\
        create_uncontrolled_abbreviations_in_requirements(data_list, aeps_to_replace, number_of_replacements)

    result_list = []
    for key in uncontr_aeps_data_as_dict.keys():
        result_list.append(uncontr_aeps_data_as_dict[key])
    result_list = result_list[1:]
    df = pd.DataFrame.from_dict(result_list)
    df.drop(columns=df.columns[0], axis=1, inplace=True)
    df.to_csv("output.csv", sep=";", header=["Dataset", "Requirement_Text", "{replaced_term:inserted_abbreviation}"])
