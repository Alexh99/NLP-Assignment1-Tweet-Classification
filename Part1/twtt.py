import sys
import preprocess 

def main(argv):
    if (len(argv) < 2 or len(argv) > 3):
        print "Wrong number or arguements"              
        sys.exit(2)

    # Get command line arguements 
    input_file_name = argv[0]
    output_file_name = argv[len(argv) - 1]  #Last arguement 

    input_file = open(input_file_name, 'r')
    data = input_file.readlines()
    input_file.close()
    
    if (len(argv) == 3):                    #Optional arguement               
        group_number = argv[1]

        #TODO: Make 5500 and 800,000 constants?
        first_half = data[group_number * 5500 : (group_number + 1) * 5500]
        last_half = data[800000 + group_number * 5500 : 800000 + (group_number + 1) * 5500]
        data = first_half + last_half

    #Process the tweet as per the steps in the assignment
    processed_tweets = preprocess.preprocess(data)

    #write results to the file 
    output_file = open (output_file_name,'w')
    output_file.write(processed_tweets)
    output_file.close()

if __name__ == "__main__":
    #main(["data/testing.csv",5, "data/Testing_Results.txt"]) #hardcoded arguements
    main(sys.argv[1:]) # command line arguements 
