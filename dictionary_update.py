#%% PREAMBLE
# FILENAME:         dictionary_update.py 
# COURSE:           Skills - Programming with Advanced Computer Languages (8,789,1.00)


# NOTE: This is only an ADDITIONAL script to show how we updated the Vader lexicon
# PLEASE FIND THE WHOLE PROJECT CODE UNDER: https://github.com/ninnion/Sentiment-Analysis


# GROUP MEMBERS:
# LAST NAME,        FIRST NAME,     STUDENT-ID,     CODINGXCAMP-ID,     GITHUB-ID
# Flemming,         Julian,         16-608-143,     JulianF.,           ninnion 
# Heim,             Simona,         15-613-623,     tapioca,            tapioca7 
# Moine,            Alexandre,      15-052-319,     MrPineapple,        GoldenPineappleR
# Spichiger,        Matthias,       15-937-667,     Matt 32,            MatthiasSP

# NOTE: To run this code two files have to be downloaded that are also available on github:
# -> LoughranMcDonald_SentimentWordLists2018.xlsx
# -> vader_lexicon.xlsx

#%% INSTALL LIBRARIES
import pandas as pd


#%% Load Vader lexicon word list from excel file
vader = pd.read_excel(r"/Users/Documents/vader_lexicon.xlsx",
                            sheet_name= "vader_lexicon", header = None, names = ["word", "score", "variance", "guess"])


#%% Updates for Vader lexicon with Loughran-McDonald sentiment word lists for financial context

# About the Loughran-McDonald sentiment word lists
# -> developed word lists to be used for financial content analysis
# -> term classifications regarding a large sample of 10Ks
# -> different categories of words lists like (negative, positive, uncertainty, constraining, etc.)

# Source and further information about the development of the word list
# -> Loughran, Tim and McDonald, Bill, When is a Liability not a Liability?
# -> Textual Analysis, Dictionaries, and 10-Ks (March 4, 2010)
# -> Journal of Finance, Forthcoming
# -> Available at SSRN: https://ssrn.com/abstract=1331573

# Use for updating the Vader lexicon
# -> Some lists are taken to update the Vader lexicon
# -> The goal is to improve the sentiment score in the context of financial terms
# -> To see how the strings of terms are created please see the additional dictionary_update script on github
# -> The addition of follwoing word lists have been made:


#%% Uncertainty
# -> Adding a total of 297 terms regarding uncertainties in a financial context
# -> The terms that are arleady included in Vader do not get a new score
# -> All other terms that are not in the Vader lexicon were scored with -1.5


# load the unvertainty word list from the excel file by selecting the right sheet
# note that there is no header, therefore we create a new column header named "word"
# check correct path before loading the file
uncertainty = pd.read_excel(r"/Users/Documents/LoughranMcDonald_SentimentWordLists_2018.xlsx",
                            sheet_name= "Uncertainty", header = None, names = ["word"])

# make each word to lower case only
uncertainty["word"] = uncertainty["word"].str.lower()

# merge the two word lists Vader and uncertainties
# keep only the words that are in the uncertainty list but keep the Vader value if a word is in both lists
uncertainties = pd.merge(uncertainty, vader, on="word", how="left")

# for all the terms that do not occur in the Vader lexicon the score is still not indicated
# for all empty lines we fill in a negative score of -1.5
uncertainties["score"] = uncertainties["score"].fillna(-1.5)

# delete the additional columns from the vader list we don't need for the update
del uncertainties["variance"]
del uncertainties["guess"]

# put each words into "" followed by double points :
uncertainties["word"] = '"' + uncertainties["word"] + '"' + ':'

# put a comma after each score in a seperate string column
uncertainties["comma"] = ","

# check the dataframe
uncertainties

# save the dataframe to a csv file to then extract the string
uncertainties.to_csv(r'c:uncertainties.csv', index = False, sep = " ")



#%% Constraining
# -> Adding a total of 184 terms regarding constrainings in a financial context
# -> The terms that are arleady included in Vader do not get a new score
# -> All other terms that are not in the Vader lexicon were scored with -1


# load the constraining word list from the excel file by selecting the right sheet
# note that there is no header, therefore we create a new column header named "word"
# check correct path before loading the file
constraining = pd.read_excel(r"/Users/LoughranMcDonald_SentimentWordLists_2018.xlsx",
                            sheet_name= "Constraining", header = None, names = ["word"])

# make each word to lower case only
constraining["word"] = constraining["word"].str.lower()

# merge the two word lists Vader and uncertainties
# keep only the words that are in the uncertainty list but keep the Vader value if a word is in both lists
constraining = pd.merge(constraining, vader, on="word", how="left")

# for all the terms that do not occur in the Vader lexicon the score is still not indicated
# for all empty lines we fill in a negative score of -1
constraining["score"] = constraining["score"].fillna(-1)

# delete the additional columns from the vader list we don't need for the update
del constraining["variance"]
del constraining["guess"]

# put each words into "" followed by double points :
constraining["word"] = '"' + constraining["word"] + '"' + ':'

# put a comma after each score in a seperate string column
constraining["comma"] = ","

# check the dataframe
constraining

# save the dataframe to a csv file to then extract the string
constraining.to_csv(r'c:constraining.csv', index = False, sep = " ")


# %%Positive
# -> Adding a total of 354 positive terms regarding a financial context
# -> The terms that are arleady included in Vader do not get a new score
# -> All other terms that are not in the Vader lexicon were scored with +1.5


# load the positive word list from the excel file by selecting the right sheet
# note that there is no header, therefore we create a new column header named "word"
# check correct path before loading the file
positive = pd.read_excel(r"/Users/LoughranMcDonald_SentimentWordLists_2018.xlsx",
                            sheet_name= "Positive", header = None, names = ["word"])

# make each word to lower case only
positive["word"] = positive["word"].str.lower()

# merge the two word lists Vader and uncertainties
# keep only the words that are in the uncertainty list but keep the Vader value if a word is in both lists
positive = pd.merge(positive, vader, on="word", how="left")

# for all the terms that do not occur in the Vader lexicon the score is still not indicated
# for all empty lines we fill in a negative score of -1
positive["score"] = positive["score"].fillna(1.5)

# delete the additional columns from the vader list we don't need for the update
del positive["variance"]
del positive["guess"]

# put each words into "" followed by double points :
positive["word"] = '"' + positive["word"] + '"' + ':'

# put a comma after each score in a seperate string column
positive["comma"] = ","

# check the dataframe
positive

# save the dataframe to a csv file to then extract the string
positive.to_csv(r'c:positive.csv', index = False, sep = " ")

#%% END OF PROGRAM
