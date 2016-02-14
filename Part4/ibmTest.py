# ibmTest.py
# 
# This file tests all 3 classifiers using the NLClassifier IBM Service
# previously created using ibmTrain.py
# 
# TODO: You must fill out all of the functions in this file following 
# 		the specifications exactly. DO NOT modify the headers of any
#		functions. Doing so will cause your program to fail the autotester.
#
#		You may use whatever libraries you like (as long as they are available
#		on CDF). You may find json, request, or pycurl helpful.
#		You may also find it helpful to reuse some of your functions from ibmTrain.py.
#

import requests, sys
from requests.auth import HTTPBasicAuth

class TestingException(Exception):
    """Exception raised when there is an issue testing a classifier"""

def get_classifier_ids(username,password):
	# Retrieves a list of classifier ids from a NLClassifier service 
	# an outputfile named ibmTrain#.csv (where # is n_lines_to_extract).
	#
	# Inputs: 
	# 	username - username for the NLClassifier to be used, as a string
	#
	# 	password - password for the NLClassifier to be used, as a string
	#
	#		
	# Returns:
	#	a list of classifier ids as strings
	#
	# Error Handling:
	#	This function should throw an exception if the classifiers call fails for any reason
	#
	
	# Get a list of all classifiers (assuming only one instance of 'Classifier 500',
	# 'Classifier 2500', and 'Classifier 5000' are the appropriate classifiers).
	try:
		r = requests.get(
	        'https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers',
	        auth=HTTPBasicAuth(username, password)
	    )
    except requests.exceptions.RequestException as e:
        raise TestingException("Requests error: {0}".format(e))

    if r.status_code != 200:
    	raise TestingException("Error getting classifier IDs (Code: {0})".format(r.status_code))

	classifiers = [c for c in r.json()['classifiers'] if c['name'] in valid_classifier_names]

	# Ensure there's 1 instance of each classifier type
	valid_classifier_names = ["Classifier {0}".format(i) for i in (500, 2500, 5000)]
	classifier_names = [c['name'] for c in classifiers]
	if set(classifier_names) != set(valid_classifier_names) and len(classifier_names) != len(valid_classifier_names):
		raise TestingException('Single instances of each the required classifiers were not found')
	
	return [c['classifier_id'] for c in classifiers]
	

def assert_all_classifiers_are_available(username, password, classifier_id_list):
	# Asserts all classifiers in the classifier_id_list are 'Available' 
	#
	# Inputs: 
	# 	username - username for the NLClassifier to be used, as a string
	#
	# 	password - password for the NLClassifier to be used, as a string
	#
	#	classifier_id_list - a list of classifier ids as strings
	#		
	# Returns:
	#	None
	#
	# Error Handling:
	#	This function should throw an exception if the classifiers call fails for any reason AND 
	#	It should throw an error if any classifier is NOT 'Available'
	#
	
	for classifier_id in classifier_id_list:
		try:
			r = requests.get(
		        "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers/{0}".format(classifier_id),
		        auth=HTTPBasicAuth(username, password)
		    )
	    except requests.exceptions.RequestException as e:
        	raise TestingException("Requests error: {0}".format(e))

	    if r.status_code != 200:
	    	raise TestingException("Error getting status of classifier '{0}'".format(classifier_id))
	    else if r.json()['status'] != 'Available':
	    	raise TestingException("Classifier '{0}' is not Available".format(classifier_id))
	
	return

def classify_single_text(username,password,classifier_id,text):
	# Classifies a given text using a single classifier from an NLClassifier 
	# service
	#
	# Inputs: 
	# 	username - username for the NLClassifier to be used, as a string
	#
	# 	password - password for the NLClassifier to be used, as a string
	#
	#	classifier_id - a classifier id, as a string
	#		
	#	text - a string of text to be classified, not UTF-8 encoded
	#		ex. "Oh, look a tweet!"
	#
	# Returns:
	#	A "classification". Aka: 
	#	a dictionary containing the top_class and the confidences of all the possible classes 
	#	Format example:
	#		{'top_class': 'class_name',
	#		 'classes': [
	#					  {'class_name': 'myclass', 'confidence': 0.999} ,
	#					  {'class_name': 'myclass2', 'confidence': 0.001}
	#					]
	#		}
	#
	# Error Handling:
	#	This function should throw an exception if the classify call fails for any reason 
	#
	
	#TODO: Fill in this function
	
	return


def classify_all_texts(username,password,input_csv_name):
        # Classifies all texts in an input csv file using all classifiers for a given NLClassifier
        # service.
        #
        # Inputs:
        #       username - username for the NLClassifier to be used, as a string
        #
        #       password - password for the NLClassifier to be used, as a string
        #      
        #       input_csv_name - full path and name of an input csv file in the 
        #              6 column format of the input test/training files
        #
        # Returns:
        #       A dictionary of lists of "classifications".
        #       Each dictionary key is the name of a classifier.
        #       Each dictionary value is a list of "classifications" where a
        #       "classification" is in the same format as returned by
        #       classify_single_text.
        #       Each element in the main dictionary is:
        #       A list of dictionaries, one for each text, in order of lines in the
        #       input file. Each element is a dictionary containing the top_class
        #       and the confidences of all the possible classes (ie the same
        #       format as returned by classify_single_text)
        #       Format example:
        #              {'classifiername':
        #                      [
        #                              {'top_class': 'class_name',
        #                              'classes': [
        #                                        {'class_name': 'myclass', 'confidence': 0.999} ,
        #                                         {'class_name': 'myclass2', 'confidence': 0.001}
        #                                          ]
        #                              },
        #                              {'top_class': 'class_name',
        #                              ...
        #                              }
        #                      ]
        #              , 'classifiername2':
        #                      [
        #                      ...      
        #                      ]
        #              ...
        #              }
        #
        # Error Handling:
        #       This function should throw an exception if the classify call fails for any reason
        #       or if the input csv file is of an improper format.
        #

        #TODO: Fill in this function
        
        return


def compute_accuracy_of_single_classifier(classifier_dict, input_csv_file_name):
	# Given a list of "classifications" for a given classifier, compute the accuracy of this
	# classifier according to the input csv file
	#
	# Inputs:
	# 	classifier_dict - A list of "classifications". Aka:
	#		A list of dictionaries, one for each text, in order of lines in the 
	#		input file. Each element is a dictionary containing the top_class
	#		and the confidences of all the possible classes (ie the same
	#		format as returned by classify_single_text) 	
	# 		Format example:
	#			[
	#				{'top_class': 'class_name',
	#			 	 'classes': [
	#						  	{'class_name': 'myclass', 'confidence': 0.999} ,
	#						  	{'class_name': 'myclass2', 'confidence': 0.001}
	#							]
	#				},
	#				{'top_class': 'class_name',
	#				...
	#				}
	#			]
	#
	#	input_csv_name - full path and name of an input csv file in the  
	#		6 column format of the input test/training files
	#
	# Returns:
	#	The accuracy of the classifier, as a fraction between [0.0-1.0] (ie percentage/100). \
	#	See the handout for more info.
	#
	# Error Handling:
	# 	This function should throw an error if there is an issue with the 
	#	inputs.
	#
	
	#TODO: fill in this function
	
	return

def compute_average_confidence_of_single_classifier(classifier_dict, input_csv_file_name):
	# Given a list of "classifications" for a given classifier, compute the average 
	# confidence of this classifier wrt the selected class, according to the input
	# csv file. 
	#
	# Inputs:
	# 	classifier_dict - A list of "classifications". Aka:
	#		A list of dictionaries, one for each text, in order of lines in the 
	#		input file. Each element is a dictionary containing the top_class
	#		and the confidences of all the possible classes (ie the same
	#		format as returned by classify_single_text) 	
	# 		Format example:
	#			[
	#				{'top_class': 'class_name',
	#			 	 'classes': [
	#						  	{'class_name': 'myclass', 'confidence': 0.999} ,
	#						  	{'class_name': 'myclass2', 'confidence': 0.001}
	#							]
	#				},
	#				{'top_class': 'class_name',
	#				...
	#				}
	#			]
	#
	#	input_csv_name - full path and name of an input csv file in the  
	#		6 column format of the input test/training files
	#
	# Returns:
	#	The average confidence of the classifier, as a number between [0.0-1.0]
	#	See the handout for more info.
	#
	# Error Handling:
	# 	This function should throw an error if there is an issue with the 
	#	inputs.
	#
	
	#TODO: fill in this function
	
	return


if __name__ == "__main__":

	input_test_data = '<ADD FILE NAME HERE>'
	username = 'USERNAME'
	password = 'PASSWORD'

	try:
		#STEP 1: Ensure all 3 classifiers are ready for testing
		get_classifier_ids(username, password)

		#STEP 2: Test the test data on all classifiers
		
		#STEP 3: Compute the accuracy for each classifier
		
		#STEP 4: Compute the confidence of each class for each classifier

	except TestingException as e:
		sys.exit(e)
