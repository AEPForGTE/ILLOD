import pandas as pd
import random
import functions


def replace_term_with_abb_in_given_req(req_text, cleaned_nc, abb):
    set_of_term_pairs = functions.nc_detect(req_text)
    for item in set_of_term_pairs:
        if item[1] == cleaned_nc:
            return req_text.replace(item[0], abb)
    return req_text


def replace_phrase_with_abb(nc_to_reqID_map, reqs_dict, replacement_sample):
    list_of_term_occurances = nc_to_reqID_map[replacement_sample[0]]
    rand_int = random.randint(1, len(list_of_term_occurances) - 1)
    random_pick_of_occurances = random.choices(list_of_term_occurances, k=rand_int)
    changed_data_dict = {}

    for _id in random_pick_of_occurances:
        for key in reqs_dict:
            if key == _id:
                _new_req = replace_term_with_abb_in_given_req(reqs_dict[key]["requirement"], replacement_sample[0], replacement_sample[1])
                changed_data_dict[_id] = {"id": reqs_dict[key]["id"],
                                          "dataset": reqs_dict[key]["dataset"],
                                          "requirement": _new_req}
                if "replaced_term" in changed_data_dict[_id].keys():
                    changed_data_dict[_id]["replaced_term"][replacement_sample[0]] = replacement_sample[1]
                else:
                    d = {replacement_sample[0]: replacement_sample[1]}
                    changed_data_dict[_id]["replaced_term"] = d



    updated = {}
    for _key in reqs_dict.keys():
        if _key not in changed_data_dict.keys():
            updated[_key] = reqs_dict[_key]
        else:
            updated[_key] = changed_data_dict[_key]
    return updated


def create_uncontrolled_abbreviations_in_requirements(data_list, terms_to_be_replaced, number_of_abbreviations):
    nc_to_reqID_map = functions.generate_nc_to_reqID_map(data_list)
    list_of_replacements = []
    for sample in terms_to_be_replaced:
        if not (sample[1] != sample[1]):
            if sample[0] in nc_to_reqID_map.keys() and len(nc_to_reqID_map[sample[0]]) >= 2:
                list_of_replacements.append(sample)
    list_of_replacements = random.sample(list_of_replacements, number_of_abbreviations)


    changed_data_dict = {}
    for sample in data_list:
        changed_data_dict[sample[0] + "_" + sample[1]] = {"id": sample[0],
                                                          "dataset": sample[1],
                                                          "requirement": sample[2],
                                                          "replaced_term": {}}


    for r_sample in list_of_replacements:
        changed_data_dict = replace_phrase_with_abb(nc_to_reqID_map, changed_data_dict, r_sample)

    return changed_data_dict


def generate_modified_requirements(number_of_replacements):
    filePath = "pure_dataset.csv"
    data = pd.read_csv(filePath, names=['ID', 'dataset', 'requirement'], sep=';', encoding='utf8')
    data_list = data.values.tolist()

    replacement_data = pd.read_csv("SF-LF-Pairs.csv", names=['term', 'abbv'], sep=';', encoding='utf8')
    aeps_to_replace = replacement_data.values.tolist()

    uncontr_aeps_data  = create_uncontrolled_abbreviations_in_requirements(data_list, aeps_to_replace, number_of_replacements)
    pd.DataFrame.from_dict(uncontr_aeps_data).T.to_csv("output.csv", sep=";")
