# ibmTrain.py
# 
# This file produces 3 classifiers using the NLClassifier IBM Service
# 
# TODO: You must fill out all of the functions in this file following 
#               the specifications exactly. DO NOT modify the headers of any
#               functions. Doing so will cause your program to fail the autotester.
#
#               You may use whatever libraries you like (as long as they are available
#               on CDF). You may find json, request, or pycurl helpful.
#

###IMPORTS###################################
import csv, requests, json, sys
from requests.auth import HTTPBasicAuth

###HELPER FUNCTIONS##########################

class TrainingException(Exception):
    """Exception raised when there is an issue training a classifier"""

def convert_training_csv_to_watson_csv_format(input_csv_name, group_id, output_csv_name): 
# Converts an existing training csv file. The output file should
# contain only the 11,000 lines of your group's specific training set.
#
# Inputs:
#       input_csv - a string containing the name of the original csv file
#               ex. "my_file.csv"
#
#       output_csv - a string containing the name of the output csv file
#               ex. "my_output_file.csv"
#
# Returns:
#       None

    with open(input_csv_name, 'r') as read_file:
        reader = csv.reader(read_file, delimiter=',')
        data = list(reader)
        first_half = data[group_id * 5500 : (group_id + 1) * 5500]
        last_half = data[800000 + group_id * 5500 : 800000 + (group_id + 1) * 5500]
        filtered_data = first_half + last_half
        with open(output_csv_name, 'w') as write_file:
            writer = csv.writer(write_file, delimiter=',')
            for row in filtered_data:
                score = row[0]
                # Remove double quotes, escape tab characters
                tweet = row[5].replace('"', '').replace('\t', '\\t')
                writer.writerow([tweet, score])

    return

def extract_subset_from_csv_file(input_csv_file, n_lines_to_extract, output_file_prefix='ibmTrain'):
    # Extracts n_lines_to_extract lines from a given csv file and writes them to 
    # an outputfile named ibmTrain#.csv (where # is n_lines_to_extract).
    #
    # Inputs: 
    #       input_csv - a string containing the name of the original csv file from which
    #               a subset of lines will be extracted
    #               ex. "my_file.csv"
    #       
    #       n_lines_to_extract - the number of lines to extract from the csv_file, as an integer
    #               ex. 500
    #
    #       output_file_prefix - a prefix for the output csv file. If unspecified, output files 
    #               are named 'ibmTrain#.csv', where # is the input parameter n_lines_to_extract.
    #               The csv must be in the "watson" 2-column format.
    #               
    # Returns:
    #       None

    output_csv_file = "{0}{1}.csv".format(output_file_prefix, n_lines_to_extract)
    with open(input_csv_file, 'r') as read_file:
        with open(output_csv_file, 'w') as write_file:
            lines = list(read_file)
            middle_index = len(lines)/2
            subset = lines[:n_lines_to_extract]+lines[middle_index:middle_index+n_lines_to_extract]
            write_file.writelines(subset)

    return
        
def create_classifier(username, password, n, input_file_prefix='ibmTrain'):
    # Creates a classifier using the NLClassifier service specified with username and password.
    # Training_data for the classifier provided using an existing csv file named
    # ibmTrain#.csv, where # is the input parameter n.
    #
    # Inputs:
    #       username - username for the NLClassifier to be used, as a string
    #
    #       password - password for the NLClassifier to be used, as a string
    #
    #       n - identification number for the input_file, as an integer
    #               ex. 500
    #
    #       input_file_prefix - a prefix for the input csv file, as a string.
    #               If unspecified data will be collected from an existing csv file 
    #               named 'ibmTrain#.csv', where # is the input parameter n.
    #               The csv must be in the "watson" 2-column format.
    #
    # Returns:
    #       A dictionary containing the response code of the classifier call, will all the fields 
    #       specified at
    #       http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/natural-language-classifier/api/v1/?curl#create_classifier
    #   
    #
    # Error Handling:
    #       This function should throw an exception if the create classifier call fails for any reason
    #       or if the input csv file does not exist or cannot be read.
    #

    filename = "{0}{1}.csv".format(input_file_prefix, n)
    try:
        with open(filename, 'r') as f:
            training_metadata = {
                "language": "en",
                "name": "Classifier {0}".format(n)
            }

            r = requests.post(
                'https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers',
                auth=HTTPBasicAuth(username, password),
                files={
                    'training_data': (filename, f)
                },
                data={
                    'training_metadata': json.dumps(training_metadata)
                }
            )

            if r.status_code != 200:
                raise TrainingException("Error creating classifier '{0}' (Code: {1})".format(filename, r.status_code))
            else:
                classifier_id = r.json()['classifier_id']
                print "Created classifier '{0}' (Code: {1}) - ID: {2}".format(filename, r.status_code, classifier_id)

    except IOError:
        raise TrainingException("Error opening file '{0}'".format(filename))

    return
        
if __name__ == "__main__":
        
    ### STEP 1: Convert csv file into two-field watson format
    input_csv_name = '../data/trainingandtestdata/training.1600000.processed.noemoticon.csv'

    #DO NOT CHANGE THE NAME OF THIS FILE
    output_csv_name = 'training_11000_watson_style.csv'

    group_id = 5
    convert_training_csv_to_watson_csv_format(input_csv_name, group_id, output_csv_name)

    ### STEP 2: Save 3 subsets in the new format into ibmTrain#.csv files
    extract_subset_from_csv_file(output_csv_name, 500)
    extract_subset_from_csv_file(output_csv_name, 2500)
    extract_subset_from_csv_file(output_csv_name, 5000)

    ### STEP 3: Create the classifiers using Watson
    username = 'USERNAME'
    password = 'PASSWORD'
    try:
        create_classifier(username, password, 500)
        create_classifier(username, password, 2500)
        create_classifier(username, password, 5000)

    except TrainingException as e:
        sys.exit(e)
