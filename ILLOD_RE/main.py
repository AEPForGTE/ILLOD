from ILLOD_RE.src import generate_uncontrolled_abbreviations
from ILLOD_RE.src import evaluate_illod

def main():
    generate_uncontrolled_abbreviations.generate_modified_requirements(number_of_replacements=100)
    evaluate_illod.ten_fold_validation(number_of_replacements=100)

if __name__ == "__main__":
    main()