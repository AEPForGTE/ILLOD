import pandas as pd
from MAIN.src import functionsPool
import os

# Get the directory path of the current file.
# Get the directory path of the parent directory of the current file.
# Set the tail of the path for the pure requirements data file.
# Create the full path for the pure requirements data file by concatenating the parent directory path and the tail path.
# Set the tail of the path for the LF-SF pairs (replacement data) file.
# Create the full path for the LF-SF pairs (replacement data) file by concatenating the parent directory path and the tail path.

dirname = os.path.dirname(__file__)
dirOfdir = os.path.split(dirname)[0]
tailOfReqDataPath = "/input_data/pure_requirements.csv"
requirementsFilePath = str(dirOfdir) + str(tailOfReqDataPath)
tailOfReplacementDataPath = "/input_data/LF-SF_Pairs.csv"
replacementDataFilePath = str(dirOfdir) + str(tailOfReplacementDataPath)



# This function generates modified requirements by replacing terms from the original dataset with their respective abbreviations.
# The number_of_replacements parameter determines the number of replacements to make for each requirement.

def generate_modified_requirements(number_of_replacements):
    # Read the original requirements data from a CSV file into a Pandas DataFrame.
    data = pd.read_csv(requirementsFilePath, names=['ID', 'dataset', 'requirement'], sep=';', encoding='utf8')

    # Convert the DataFrame into a list of lists.
    data_list = data.values.tolist()

    # Read the replacement data (term-abbreviation mapping) from a CSV file into a Pandas DataFrame.
    replacement_data = pd.read_csv(replacementDataFilePath, names=['term', 'abbv'], sep=';', encoding='utf8')

    # Convert the DataFrame into a list of lists.
    aeps_to_replace = replacement_data.values.tolist()

    # Call a function to create uncontrolled abbreviations in the requirements.
    # The returned data is in the form of a dictionary with keys as dataset names and values as lists of modified requirements.
    uncontr_aeps_data_as_dict = functionsPool.create_uncontrolled_abbreviations_in_requirements(data_list,
                                                                                                aeps_to_replace,
                                                                                                number_of_replacements)

    # Convert the dictionary values into a list.
    result_list = list(uncontr_aeps_data_as_dict.values())[1:]

    # Convert the list of modified requirements into a Pandas DataFrame.
    df = pd.DataFrame.from_dict(result_list)

    # Drop the first column of the DataFrame (corresponding to the internal id, which is not needed in the csv file).
    df.drop(columns=df.columns[0], axis=1, inplace=True)

    return df
