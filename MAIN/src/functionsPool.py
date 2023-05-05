import random
import re
import spacy
nlp = spacy.load("en_core_web_sm")



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
        current_ID = sample[0] + "_" + sample[1]
        set_of_nc_tuples_in_sent = nc_detect(sample[2])

        for term_tuple in set_of_nc_tuples_in_sent:
            cleaned_term = term_tuple[1]
            if cleaned_term in nc_to_reqID_map.keys():
                ID_list_so_far = nc_to_reqID_map[cleaned_term]
                if current_ID not in ID_list_so_far:
                    ID_list_so_far.append(current_ID)
                nc_to_reqID_map[cleaned_term] = ID_list_so_far
            else:
                nc_to_reqID_map[cleaned_term] = [current_ID]
    return nc_to_reqID_map



def replace_term_with_abb_in_given_req(req_text, cleaned_nc, abb):
    set_of_term_pairs = nc_detect(req_text)
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
    nc_to_reqID_map = generate_nc_to_reqID_map(data_list)
    list_of_replacements = []
    for sample in terms_to_be_replaced:
        if not (sample[1] != sample[1]):
            if sample[0] in nc_to_reqID_map.keys() and len(nc_to_reqID_map[sample[0]]) >= 2:
                list_of_replacements.append(sample)
    list_of_replacements = random.sample(list_of_replacements, number_of_abbreviations)


    changed_data_dict = {}
    for sample in data_list:
        if sample[0] + "_" + sample[1] == "ID_dataset":
            d = "{replaced_term:inserted_abbreviation}"
        else:
            d = {}
        changed_data_dict[sample[0] + "_" + sample[1]] = {"id": sample[0],
                                                          "dataset": sample[1],
                                                          "requirement": sample[2],
                                                          "replaced_term": d}


    for r_sample in list_of_replacements:
        changed_data_dict = replace_phrase_with_abb(nc_to_reqID_map, changed_data_dict, r_sample)

    return changed_data_dict