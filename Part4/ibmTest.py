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

import requests, sys, csv, urllib
from requests.auth import HTTPBasicAuth
from collections import OrderedDict

# Supress InsecurePlatformWarning/SNIMissingWarning, etc. on CDF
requests.packages.urllib3.disable_warnings()

class TestingException(Exception):
	"""Exception raised when there is an issue testing a classifier"""

def get_classifier(username,password,classifier_id):
	# Helper function to get a classifier
	# 
	# Inputs:
	# 	username - username for the NLClassifier to be used, as a string
	#
	# 	password - password for the NLClassifier to be used, as a string
	# 
	# 	classifier_id - id of the classifier to retrieve
	# 
	# Returns:
	# 	a classifier dict
	# 
	# Error Handling:
	#	This function should throw an exception if the classifier call fails for any reason
	# 

	try:
		r = requests.get(
			"https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers/{0}".format(classifier_id),
			auth=HTTPBasicAuth(username, password)
		)
	except requests.exceptions.RequestException as e:
		raise TestingException("Requests error: {0}".format(e))

	if r.status_code != 200:
		raise TestingException("Error getting classifier '{0}'".format(classifier_id))

	return r.json()

def get_valid_classifiers(username,password):
	# Helper function to get all valid classifiers
	# 
	# Inputs:
	# 	username - username for the NLClassifier to be used, as a string
	#
	# 	password - password for the NLClassifier to be used, as a string
	# 
	# Returns:
	# 	a list of classifier dicts
	# 
	# Error Handling:
	#	This function should throw an exception if the classifier call fails for any reason
	# 

	# Get a list of all VALID classifiers (assuming only one instance of 'Classifier 500',
	# 'Classifier 2500', and 'Classifier 5000' are allowed).
	try:
		r = requests.get(
			'https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers',
			auth=HTTPBasicAuth(username, password)
		)
	except requests.exceptions.RequestException as e:
		raise TestingException("Requests error: {0}".format(e))

	if r.status_code != 200:
		raise TestingException("Error getting classifiers '{0}'".format(classifier_id))

	valid_classifier_names = ["Classifier {0}".format(i) for i in (500, 2500, 5000)]
	classifiers = [c for c in r.json()['classifiers'] if c['name'] in valid_classifier_names]

	# Ensure there's 1 instance of each required classifier type
	classifier_names = [c['name'] for c in classifiers]
	if set(classifier_names) != set(valid_classifier_names) or len(classifier_names) != len(valid_classifier_names):
		raise TestingException('Single instances of each of the required classifiers were not found')

	return classifiers

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
	
	return [classifier['classifier_id'] for classifier in get_valid_classifiers(username, password)]

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
		classifier = get_classifier(username, password, classifier_id)

		if classifier['status'] != 'Available':
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
	
	query_string = {'text': text}
	try:
		r = requests.get(
			"https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers/{0}/classify?{1}".format(classifier_id, urllib.urlencode(query_string)),
			auth=HTTPBasicAuth(username, password)
		)
	except requests.exceptions.RequestException as e:
		raise TestingException("Requests error: {0}".format(e))
	
	# Get the data and return it (only with the keys 'top_class' and 'classes')
	data = r.json()
	return {key: data[key] for key in ('top_class', 'classes')}


def classify_all_texts(username,password,input_csv_name):
		# Classifies all texts in an input csv file using all classifiers for a given NLClassifier
		# service.
		#
		# Inputs:
		#	   username - username for the NLClassifier to be used, as a string
		#
		#	   password - password for the NLClassifier to be used, as a string
		#	  
		#	   input_csv_name - full path and name of an input csv file in the 
		#			  6 column format of the input test/training files
		#
		# Returns:
		#	   A dictionary of lists of "classifications".
		#	   Each dictionary key is the name of a classifier.
		#	   Each dictionary value is a list of "classifications" where a
		#	   "classification" is in the same format as returned by
		#	   classify_single_text.
		#	   Each element in the main dictionary is:
		#	   A list of dictionaries, one for each text, in order of lines in the
		#	   input file. Each element is a dictionary containing the top_class
		#	   and the confidences of all the possible classes (ie the same
		#	   format as returned by classify_single_text)
		#	   Format example:
		#			  {'classifiername':
		#					  [
		#							  {'top_class': 'class_name',
		#							  'classes': [
		#										{'class_name': 'myclass', 'confidence': 0.999} ,
		#										 {'class_name': 'myclass2', 'confidence': 0.001}
		#										  ]
		#							  },
		#							  {'top_class': 'class_name',
		#							  ...
		#							  }
		#					  ]
		#			  , 'classifiername2':
		#					  [
		#					  ...	  
		#					  ]
		#			  ...
		#			  }
		#
		# Error Handling:
		#	   This function should throw an exception if the classify call fails for any reason
		#	   or if the input csv file is of an improper format.
		#

		classifiers = get_valid_classifiers(username, password)
		classifications = {classifier['name']: [] for classifier in classifiers}

		try:
			with open(input_csv_name, 'r') as f:
				reader = csv.reader(f, delimiter=',')
				for row in reader:
					tweet = row[5].replace('"', '').replace('\t', '\\t')
					# Classify each tweet using each classifier, add to the corresponding list
					for classifier in classifiers:
						classification = classify_single_text(username, password, classifier['classifier_id'], tweet)
						classifications[classifier['name']].append(classification)

		except IOError:
			raise TestingException("Error opening file '{0}'".format(input_csv_name))

		return classifications


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
	#	input_csv_file_name - full path and name of an input csv file in the  
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

	correct = []
	try:
		with open(input_csv_file_name, 'r') as f:
			reader = csv.reader(f, delimiter=',')
			for i, row in enumerate(reader):
				# Record whether it guessed top_class as the correct class for each line
				expected_class = row[0]
				predicted_class = classifier_dict[i]['top_class']
				correct.append(expected_class==predicted_class)

	except IOError:
		raise TestingException("Error opening file '{0}'".format(input_csv_file_name))
	except IndexError:
		raise TestingException('There was an error accessing an index in the input data')
	
	return sum(correct)/float(len(correct))

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
	#	input_csv_file_name - full path and name of an input csv file in the  
	#		6 column format of the input test/training files
	#
	# Returns:
	#	The average confidences of the classifier, as a pair of numbers between [0.0-1.0]
	#	(correct, incorrect)
	# 	See the handout for more info.
	#
	# Error Handling:
	# 	This function should throw an error if there is an issue with the 
	#	inputs.
	#
	
	correct_confidences = []
	incorrect_confidences = []
	try:
		with open(input_csv_file_name, 'r') as f:
			reader = csv.reader(f, delimiter=',')
			for i, row in enumerate(reader):
				# Record whether it guessed top_class as the correct class for each line
				expected_class = row[0]
				predicted_class = classifier_dict[i]['top_class']
				# Get the confidence of the predicted class
				confidence = None
				for class_confidence in classifier_dict[i]['classes']:
					if class_confidence['class_name'] == predicted_class:
						confidence = class_confidence['confidence']

				correct_confidences.append(confidence) if expected_class == predicted_class else incorrect_confidences.append(confidence)

	except IOError:
		raise TestingException("Error opening file '{0}'".format(input_csv_file_name))
	except IndexError:
		raise TestingException('There was an error accessing an index in the input data')
	
	avg_correct_confidence = sum(correct_confidences)/float(len(correct_confidences))
	avg_incorrect_confidence = sum(incorrect_confidences)/float(len(incorrect_confidences))
	
	return avg_correct_confidence, avg_incorrect_confidence

def get_classifier_name_key(classifier_name_tuple):
	# Helper function for writing out to the text file (sorted by classifier number)
	# ie. allows for the ordering of 'Classifier 500', 'Classifier 2500', 'Classifier 5000'
	#
	# Inputs:
	#	classifier_name_tuple - A tuple with classifier name and some value (accuracy or confidence)
	# 		ex. (u'Classifier 500', 0.99)
	# 
	# Returns:
	# 	The value to use when sorting (the classifier's training data set size), ex. 500
	# 

	return int(classifier_name_tuple[0].split(' ')[1])

if __name__ == "__main__":

	input_test_data = '/u/cs401/A1/tweets/testdata.manualSUBSET.2009.06.14.csv'
	output_file = '4output.txt'

	username = '5d1f18ba-c9b9-4609-bdd9-6a4f659674f0'
	password = 'bVnKJwROHgNW'

	try:
		#STEP 1: Ensure all 3 classifiers are ready for testing
		ids = get_classifier_ids(username, password)
		assert_all_classifiers_are_available(username, password, ids)

		#STEP 2: Test the test data on all classifiers
		classifications = classify_all_texts(username, password, input_test_data)

		#STEP 3: Compute the accuracy for each classifier
		accuracies = {}
		for classifier_name, classification in classifications.iteritems():
			accuracy = compute_accuracy_of_single_classifier(classification, input_test_data)
			accuracies[classifier_name] = accuracy

		#STEP 4: Compute the average confidence for correct/incorrect classifications (for each classifier)
		confidences = {}
		for classifier_name, classification in classifications.iteritems():
			correct_confidence, incorrect_confidence = compute_average_confidence_of_single_classifier(classification, input_test_data)
			confidences[classifier_name] = (correct_confidence, incorrect_confidence)

		#WRITE TO FILE
		with open(output_file, 'w') as f:
			f.write('4 IBM Watson on BlueMix\n')
			f.write('=======================\n')
			f.write('-----------------------\n')
			f.write('4.3 Accuracy\n')
			f.write('-----------------------\n')
			# Sort so that they're printed in the right order
			ordered_accuracies = OrderedDict(sorted(accuracies.items(), key=get_classifier_name_key))
			for classifier_name, accuracy in ordered_accuracies.iteritems():
				f.write("{0}:\n\t{1}\n".format(classifier_name, accuracy))
			
			f.write('\n-----------------------\n')
			f.write('4.4 Average Confidence\n')
			f.write('-----------------------\n')
			ordered_confidences = OrderedDict(sorted(confidences.items(), key=get_classifier_name_key))
			for classifier_name, (correct_confidence, incorrect_confidence) in ordered_confidences.iteritems():
				f.write("{0}:\n\t{1} when correct,\n\t{2} when incorrect\n".format(classifier_name, correct_confidence, incorrect_confidence))
			f.write('\n-----------------------\n')
			f.write('Discussion\n')
			f.write('-----------------------\n')
			f.write('<INSERT COMMENTS HERE>')

	except TestingException as e:
		sys.exit("Caught an exception: {0}".format(e))
	except IOError:
		raise TestingException("Error writing to '{0}'".format(output_file))
