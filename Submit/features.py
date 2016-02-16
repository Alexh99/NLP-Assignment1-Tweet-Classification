#Each feature that we want to count is made up of a list of patterns to search for
#some of the features are read in from files located in /u/cs401/Wordlists/,
#other features are defined in this file.

#The lists contain the regex pattern that will be searched for. To add a new feature
#create a new list with the patterns you want and add it to the FEATURES list located
#at the bottom of the file. If you want your patterns to ignore capitalization,
#use True for the second parameter, and False otherwise.

COUNT_FIRST_PERSON = open("/u/cs401/Wordlists/First-person",'r').readlines()
for i in range (len(COUNT_FIRST_PERSON)):
    if (COUNT_FIRST_PERSON[i] !=""):
        COUNT_FIRST_PERSON[i] = " " + COUNT_FIRST_PERSON[i].strip() +"/"
    else:
        COUNT_FIRST_PERSON.pop(i)
    
    
COUNT_SECOND_PERSON = open("/u/cs401/Wordlists/Second-person",'r').readlines()
for i in range (len(COUNT_SECOND_PERSON)):
    if (COUNT_SECOND_PERSON[i] !=""):
        COUNT_SECOND_PERSON[i] =  " " +  COUNT_SECOND_PERSON[i].strip() +"/"
    else:
        COUNT_SECOND_PERSON.pop(i)
    

COUNT_THIRD_PERSON = open("/u/cs401/Wordlists/Third-person",'r').readlines()
for i in range (len(COUNT_THIRD_PERSON)):
    if (COUNT_THIRD_PERSON[i] !=""):
        COUNT_THIRD_PERSON[i] =  " " +  COUNT_THIRD_PERSON[i].strip() +"/"
    else:
        COUNT_THIRD_PERSON.pop(i)


COUNT_CONJUCTIONS = open("/u/cs401/Wordlists/Conjunct",'r').readlines()
for i in range (len(COUNT_CONJUCTIONS)):
    if (COUNT_CONJUCTIONS[i] !=""):
        COUNT_CONJUCTIONS[i] = " " + COUNT_CONJUCTIONS[i].strip() +"/"
    else:
        COUNT_CONJUCTIONS.pop(i)

    
COUNT_PAST_TENSE_VERBS = ["/VBD ","/VBN "]
COUNT_FUTURE_TENSE_VERBS = ["'/POS ll","will","gonna","going/VBG to/TO .*/VB"]
COUNT_COMMAS = [" ,"]
COUNT_COLONS_SEMICOLONS = [" :"," ;"]
COUNT_DASHES = ["-"]
COUNT_PARENTHESES = [" \("," \)"," \["," \]"," {"," }"]
COUNT_ELLIPSES = ["\.\.\."]
COUNT_COMMON_NOUNS = ["/NN ","/NNS "]
COUNT_PROPER_NOUNS = ["/NNP ","/NNPS "]
COUNT_ADVERBS = ["/RB ","/RBR ","/RBS "]
COUNT_WH_WORDS = ["/WDT ","/WP ","/WP$ ","/WRB "]

COUNT_SLANG = open("/u/cs401/Wordlists/Slang",'r').readlines()
for i in range (len(COUNT_SLANG)):
    if (COUNT_SLANG[i] !=""):
        COUNT_SLANG[i] = " " +  COUNT_SLANG[i].strip() +"/"
    else:
        COUNT_SLANG.pop(i)
        
COUNT_UPPERCASE_WORDS = ['[A-Z][A-Z]+/']

              #Feature List    #Ignore Capitalization? 
FEATURES = [ [COUNT_FIRST_PERSON,True],
             [COUNT_SECOND_PERSON,True],
             [COUNT_THIRD_PERSON,True],
             [COUNT_CONJUCTIONS,True],
             [COUNT_PAST_TENSE_VERBS,False],
             [COUNT_FUTURE_TENSE_VERBS,True],
             [COUNT_COMMAS,False],
             [COUNT_COLONS_SEMICOLONS,False],
             [COUNT_DASHES,False],
             [COUNT_PARENTHESES,False],
             [COUNT_ELLIPSES, False],
             [COUNT_COMMON_NOUNS,False],
             [COUNT_PROPER_NOUNS,False],
             [COUNT_ADVERBS, False],
             [COUNT_WH_WORDS,False],
             [COUNT_SLANG, True],
             [COUNT_UPPERCASE_WORDS, False]]
