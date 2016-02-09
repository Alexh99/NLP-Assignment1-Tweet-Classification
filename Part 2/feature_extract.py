import re
import features

#Used to determine if a token is punctuation 
PUNCTUATION = [".","#","$",",",":",";","(",")",'"',"'"]

#Given a tweet, count the number of occurances the patterns
#in the list feature occur. case_flag is used to ignore
#capitalization from the parameters. 
def count_feature(tweet,feature,case_flag):
    num_features_found = 0
    for lines in tweet[1:]:
        for pattern in feature:
            if case_flag:
                found = re.findall(pattern,lines,flags= re.IGNORECASE)
            else:
                found = re.findall(pattern,lines)
            num_features_found += len(found)

    return str(num_features_found)

#Extracts the features from the data
def extract(data,maximum_number):
    final_string = ""

    #counters used if a third arguement is passed into the command line
    happy_tweet_counter = 0
    sad_tweet_counter = 0

    #For each tweet 
    for tweet in data:
        #Find what type of tweet it is 
        tweet_class = re.findall(r'\d', tweet[0])[0]
    
        #If the counters exceed the maximum_number of examples requested, skip
        #the feature extraction of the current tweet
        if (tweet_class =="0" and sad_tweet_counter < maximum_number):
            sad_tweet_counter += 1
        elif (tweet_class =="4" and happy_tweet_counter < maximum_number):
            happy_tweet_counter += 1
        elif maximum_number >= 0:
            continue
        
        feature_list = []
        #For each feature, count the number of occurances that appear in the tweet
        #and add it to the feature list
        for each_feature in features.FEATURES:
            feature_list.append(count_feature(tweet,each_feature[0],each_feature[1]))

        total_tokens = 0
        total_sentences = 0
        total_characters = 0
        
        #Count the number of sentences, tokens, and characters in the tweet
        for lines in tweet[1:]:
            total_tokens += len(lines.split())
            total_sentences+=1

            #Replace "/" with spaces so split will split up "you/NN" into ["you","NN"] 
            word_list = lines.replace("/"," ").split()
            #Increment by 2 to skip the tags in the list, only want the words
            for index in range(0,len(word_list),2):
                #Make sure the word is not punctuation
                if word_list[index] not in PUNCTUATION:
                    total_characters += len (word_list[index])

        #Check for division by 0
        if (total_sentences!=0):
            avg_sentence_length = float(total_tokens)/total_sentences 
        else:
            avg_sentence_length = 0
            
        #Check for division by 0    
        if (total_tokens!=0):
            avg_token_length = float(total_characters)/total_tokens
        else:
            avg_token_length = 0

        #Add number of sentences, tokens, characters, and tweet class to feature list
        feature_list.append(str(avg_sentence_length))
        feature_list.append(str(avg_token_length))
        feature_list.append(str(total_sentences))
        feature_list.append(tweet_class)

        #Convert the list into a string
        feature_string = ",".join(feature_list)
        final_string += feature_string +"\n"
        
    return final_string
