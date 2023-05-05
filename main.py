from MAIN.src import generate_uncontrolled_abbreviations
from MAIN.src import evaluate_illod
NUM_OF_REPLACEMENTS=100

def main():
    df_for_reqs_with_replacements = generate_uncontrolled_abbreviations.\
        generate_modified_requirements(NUM_OF_REPLACEMENTS)

    df_for_reqs_with_replacements.to_csv("MAIN/output_data/pure_modified_requirements.csv",
                                    sep=";",
                                    header=["Dataset", "Requirement_Text", "{replaced_term:inserted_abbreviation}"])


    df_evaluation = evaluate_illod.ten_fold_validation(NUM_OF_REPLACEMENTS)
    df_evaluation.to_csv("MAIN/output_data/evaluation_results.csv", sep=";")


if __name__ == "__main__":
    main()
