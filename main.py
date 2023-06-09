from MAIN.src import generate_uncontrolled_abbreviations
from MAIN.src import evaluate_illod
from MAIN.src import build_aep_groups
NUM_OF_REPLACEMENTS=100
import json



"""
The first task checks wether a additional file for AEP detection is given. It returns a list of detected AEP 
(Abbreviation Expansion Pairs) groups from that file. If the list is not empty, the function opens a
file named "found_AEP_groups" in the output folder and writes the JSON-encoded list to it.

The second task generates a modified version of the requirements data by replacing some terms with their corresponding 
abbreviations. This is done by calling the generate_modified_requirements() function from the 
generate_uncontrolled_abbreviations module with the NUM_OF_REPLACEMENTS parameter. The resulting dataframe is then saved
to a CSV file named "pure_modified_requirements.csv" with semicolon separators and header names.

Finally, the third tasks runs the ten_fold_validation() function from the evaluate_illod module is called with the NUM_OF_REPLACEMENTS 
parameter to evaluate the performance of ILLOD on the modified requirements data using ten-fold validation. 
The resulting dataframe is saved to a CSV file named "evaluation_results.csv" with semicolon separators.
"""

def main():
    # First task
    additional_aep_groups = build_aep_groups.check_for_additional_tasks()
    if additional_aep_groups:
        with open("MAIN/output_data/found_AEP_groups", 'w') as convert_file:
            convert_file.write(json.dumps(additional_aep_groups))

    # Second Task
    df_for_reqs_with_replacements = generate_uncontrolled_abbreviations.\
        generate_modified_requirements(NUM_OF_REPLACEMENTS)
    df_for_reqs_with_replacements.to_csv("MAIN/output_data/pure_modified_requirements.csv",
                                    sep=";",
                                    header=["Dataset", "Requirement_Text", "{replaced_term:inserted_abbreviation}"])

    # Third Task
    df_evaluation = evaluate_illod.ten_fold_validation(NUM_OF_REPLACEMENTS)
    df_evaluation.to_csv("MAIN/output_data/evaluation_results.csv", sep=";")


if __name__ == "__main__":
    main()
