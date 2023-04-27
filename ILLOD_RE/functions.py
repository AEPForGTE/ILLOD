import spacy
import re
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