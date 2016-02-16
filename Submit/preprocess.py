import re
import wordlist
import NLPlib


def preprocess(data):
    
    final_result = ""
    tagger = NLPlib.NLPlib()
    
    for i in range(len(data)):
        data[i] =  data[i].split(",")

        #If there is a comma in the tweet, this will fix it
        tweet = ""
        for j in range (5,len(data[i])-1):
            tweet = tweet + data[i][j] +","

        tweet = tweet + data[i][-1]
        
        #Get rid of the quotation marks surrounding the tweet
        tweet = tweet.strip().strip('"')

        #remove html tags
        tweet = re.sub(r'"<[^>]*>' ,"", tweet)  
      
        #replace html character codes and other characters such as "@" and "#"
        for key in wordlist.REPLACE_CHAR:                
            tweet = tweet.replace(key, wordlist.REPLACE_CHAR[key])

        #Removes URLS, fails in case like : awww. 
        tweet = re.sub(r'(www.|http)\S*\s*',"", tweet, flags= re.IGNORECASE)

        #Splits the sentences so they appear on different lines.
        #Followed the rules on page 135 of the textbook
        tweet_list = tweet.split()

        j = 0
        #Go through each word and check for end-of-sentence punctuation
        while j < len(tweet_list):
            inserted_line = False
            
            #If there is a period in the word, and it is not a common abbreviation
            #then it is the end of a sentence, and add a new line 
            if (j+1) < len(tweet_list) and "." in tweet_list[j] and tweet_list[j].lower() not in wordlist.ABBREVIATIONS:
                tweet_list.insert(j+1,"\n")
                inserted_line = True
                
            #If there is an exclimation mark, and it is not followed by a name or a
            #lowercase word then it is the end of a sentence, and add a new line 
            if ("!" in tweet_list[j] or "?" in tweet_list[j]):
                if ((j+1) < len(tweet_list) and not tweet_list[j+1].islower() and  tweet_list[j+1].lower() not in wordlist.KNOWN_NAMES):
                    tweet_list.insert(j+1,"\n") 
                    inserted_line = True

            #Splits the word up if it has any punctuatuion: e.g can't -> ["can", "'" , "t"]
            split_punctuation = re.split('(\W+)', tweet_list[j])

            #Small little hack to fix split: e.g dog. -> ["dog", ".", ""],
            #just remove the final part of the list
            if (split_punctuation[-1] == ""):
                split_punctuation.pop(-1)

            if (split_punctuation[0] == ""):
                split_punctuation.pop(0)
            #Add the split up punctuation words back into the list
            tweet_list = tweet_list[:j] + split_punctuation + tweet_list[j+1:]
            
            #Don't need to loop through the newline characters or the punctuation words we added 
            j += inserted_line + len(split_punctuation)
            

        #Call the tagger to get the parts of speech
        tags = tagger.tag(tweet_list)

        #Combine the words with the parts of speech, skip over newline characters
        for j in range (len(tweet_list)):
            if (tweet_list[j]!="\n"):
                tweet_list[j]  = tweet_list[j] + "/" + tags[j]            

        #Joins the list back into a string. After joining, each line has a space infront,
        #.replace fixes this 
        tweet =  " ".join(tweet_list).replace("\n ", "\n")

        #Add answer to the beginning of the tweet and add tweet to the output string
        tweet = "<A=" + data[i][0].strip('"') +">\n" +tweet
        
        final_result += tweet + "\n"
        
    return final_result
