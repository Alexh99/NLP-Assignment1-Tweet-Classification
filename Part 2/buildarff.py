import sys
import re
import feature_extract

def main(argv):
    if (len(argv) < 2 or len(argv) > 3):
        print "Wrong number or arguements"              
        sys.exit(2)

    # Get command line arguements 
    input_file_name = argv[0]
    output_file_name = argv[1]

    #open the data 
    input_file = open(input_file_name, 'r')
    tweet_information = input_file.readlines()
    input_file.close()

    maximum_number = -1

    #Optional arguement used to request maximum number of examples
    if (len(argv) == 3):                                
        maximum_number = argv[2]

    data = []
    tweet = []
    #Reformat the data to be a multidimensional array.
    #Each element in the list is a tweet, and the tweet is made
    #up of a list of strings (sentences)
    # data = [["this is a tweet. \n", "this is the same tweet"], ["This is a new tweet \n"]]
    for line in tweet_information:
        if re.search(r'<A=[0,2,4]', line):
            data.append(tweet)
            tweet = []
            
        tweet.append(line)

    #Extract the desired features
    results = feature_extract.extract(data[1:],maximum_number)

    header = open("header.txt",'r').read()
    
    #write results to the file 
    output_file = open (output_file_name,'w')
    output_file.write(header)
    output_file.write(results)
    output_file.close()

if __name__ == "__main__":
    main(["data/Testing_Results.txt","data/feature_results.arff"]) #hardcoded arguements
    #main(sys.argv[1:]) # command line arguements 
