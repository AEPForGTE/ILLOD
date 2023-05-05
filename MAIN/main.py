from MAIN.src import generate_uncontrolled_abbreviations
from MAIN.src import evaluate_illod
NUMBER_OF_REPLACEMENTS=100

def main():
    df_for_reqs_with_replacements = generate_uncontrolled_abbreviations.\
        generate_modified_requirements(NUMBER_OF_REPLACEMENTS)

    df_for_reqs_with_replacements.to_csv("output_data/replacement_output.csv",
                                    sep=";",
                                    header=["Dataset", "Requirement_Text", "{replaced_term:inserted_abbreviation}"])


    df_evaluation = evaluate_illod.ten_fold_validation(NUMBER_OF_REPLACEMENTS)
    df_evaluation.to_csv("output_data/evaluation_output.csv", sep=";")


if __name__ == "__main__":
    main()