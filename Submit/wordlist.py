#Dictionary to switch HTML cahracters to ASCII and to remove
#unwanted symbols
REPLACE_CHAR = {"&amp;" : "&",
                "&le;"  : "<",
                "&ge;"  : ">", #End of HTML tags -> ADD MORE? 
                "@"     : "",
                "#"     : ""
                }

abbreviation_file_1 = open("/u/cs401/Wordlists/abbrev.english",'r')
abbreviation_file_2 = open("/u/cs401/Wordlists/pn_abbrev.english",'r')

#Common abbreviations that contain periods
ABBREVIATIONS = abbreviation_file_1.readlines() + abbreviation_file_2.readlines()

for i in range (len(ABBREVIATIONS)):
    ABBREVIATIONS[i] = ABBREVIATIONS[i].lower().strip()

abbreviation_file_1.close()
abbreviation_file_2.close()

female_names = open("/u/cs401/Wordlists/femaleFirstNames.txt",'r')
male_names = open("/u/cs401/Wordlists/maleFirstNames.txt",'r')
last_names = open("/u/cs401/Wordlists/lastNames.txt",'r')

#Common names of people
KNOWN_NAMES = female_names.read() + male_names.read() + last_names.read()

female_names.close()
male_names.close()
last_names.close()
