#%% PREAMBLE
# FILENAME:         2306_sentiment_analysis.py 
# COURSE:           Skills - Programming with Advanced Computer Languages (8,789,1.00)
# PROJECT LANGUAGE: Python
# PROJECT NAME:     Sentiment Analysis
# GITHUB-URL:       https://github.com/ninnion/Sentiment-Analysis
# DESCRIPTION:      Generate BUY/HOLD/SELL rating for financial assets based on live Twitter sentiment analysis.
# GROUP ID:         2306
#
# GROUP MEMBERS:
# LAST NAME,        FIRST NAME,     STUDENT-ID,     CODINGXCAMP-ID,     GITHUB-ID
# Flemming,         Julian,         16-608-143,     JulianF.,           ninnion 
# Heim,             Simona,         15-613-623,     tapioca,            tapioca7 
# Moine,            Alexandre,      15-052-319,     MrPineapple,        GoldenPineappleR
# Spichiger,        Matthias,       15-937-667,     Matt 32,            MatthiasSP
#
# TECHNICAL DETAILS:
# PYTHON VERSION:   3.9.5
# SPYDER VERSION:   4.2.5 (Currently working with Python version 3.8.8)

#%% INSTALL LIBRARIES
# In Anaconda Prompt write: >'pip install vaderSentiment' and press 'ENTER'.
# In the same prompt, write >'pip install langdetect' and press 'ENTER'.

#%% IMPORT LIBRARIES 
# VADER | Valence Aware Dictionary and sEntiment Reasoner (https://github.com/cjhutto/vaderSentiment)
# To assign sentiment values to tweets
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# REQUESTS (https://docs.python-requests.org/en/master/)
# To send HTTP/1.1 requests.
import requests

# JSON (https://www.w3schools.com/python/python_json.asp)
# To access JSON data from the Twitter API
import json

# DETECT FROM LANGDETECT (https://pypi.org/project/langdetect/)
# To recognize English language tweets
from langdetect import detect

# NUMPY
# For easy handling of numerical data
import numpy as np

# MATPLOTLIB.PYPLOT
# For live plotting of the sentiment scores
import matplotlib.pyplot as plt

#%% BEARER_TOKEN
# The bearer token is a personal token for authentification. It is needed so that the Twitter API accepts our requests.
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAGdBNgEAAAAAebL5tbsCMiq7TRRAskhG67nHrAg%3DyfHiDGamgrGsx9xfCBQ2Xacjoa1Xm8PbhqdNu763aAj3lRfi2m"
    
#%% ANALYZER
analyzer = SentimentIntensityAnalyzer()

#%% INPUTS
# Ask for a single word for which we want to perform our sentiment analysis (e.g: 'bitcoin')
a = (input("\033[0;0m Hi there! Please enter a single word (like 'bitcoin') to perform a live Twitter sentiment analysis: "))
# colour code reset to delete any colour that might be from past runs

# Check if the entered input can be transformed into a string
while type(a) != str:
  try:
    a = str(a) # Try to convert input to string
  except:
    print("Only strings can be counted!")
    a = (input("Please try again with a string? ")) # Ask to input a string if conversion failed
    continue

# Check if the input was only one word, if not, ask user to enter one word only
while len(a.split()) != 1:
    print("You entered more than one word or nothing")
    a = input("Please try again and enter only ONE term? ")

# Add a hashtag to the input so that we may search for both hasthags (e.g.: '#bitcoin') and words (e.g.: 'bitcoin')
b = "#" + a

# asking for the input regarding amount of tweets (my_range)
c = input("Please enter also the maximum number of tweets you want to get. We recommend any number below 500: ")
# try if entered string can be transformed into an integer
# otherwise the user will be asked again to enter a number, again and again
while type(c)!=int:
  try:
    c = int(c)
  except:
    print("Sorry, only integers are allowed!")
    c = (input("Please try again and enter an integer for the total number of tweets to analyse? "))
    continue
# Recommend max 500 Tweets
# Twitter API may become exhausted, user has to wait for a while

# asking for the input regarding the moving average (N)
d = input("Now please select the window for the moving average (average of n-last entries; recommended range: 5-20): ")
# try if entered string can be transformed into an integer
# otherwise the user will be asked again to enter a number, again and again
while type(d)!=int:
  try:
    d = int(d)
  except:
    print("Sorry, only integers are allowed!")
    d = (input("Please try again and enter an integer for the moving average? "))
    continue


#%% CUSTOMIZE DICTIONARY
# About the compound score
# -> most used by researches
# -> between -1 (most extreme negative) and 1 (most extreme positive)
# -> positve >= 0.5
# -> negative <= -0.5
# -> between - 0.5 and 0.5

# About the pos, neg, neu ratios
# -> proportions, add up to 1
# -> raw categorization, no VADER rule-based enhancements applied
# -> no word-order sensitivity, modifiers, amplifiers, negation polarity switches, or contrastive conjunction sensitivity

# About the lexicon
# -> stored as: vader_lexicon.txt
# -> labels: TOKEN, MEAN-SENTIMENT-RATING, STANDARD DEVIATION, and RAW-HUMAN-SENTIMENT-RATINGS
# -> NOTE: The current algorithm makes immediate use of the first two elements (token and mean valence)
# -> The final two elements (SD and raw ratings) are provided for rigor
# -> you should find 10 independent humans to evaluate/rate each new token you want to add to the lexicon
# -> make sure the standard deviation does not exceed 2.5, and take the average rating for the valence
# -> each word is assigned a sentiment score (between -4 and +4)

# Examples:
#print(analyzer.lexicon['best'])
# 3.2	0.6	[2, 4, 4, 3, 4, 3, 3, 3, 3, 3]
#print(analyzer.lexicon['good'])
# 1.9	0.9434	[2, 1, 1, 3, 2, 4, 2, 2, 1, 1]
#print(analyzer.lexicon['bad'])
# -2.5	0.67082	[-3, -2, -4, -3, -2, -2, -3, -2, -2, -2]   
#print(analyzer.lexicon['worst'])
# -3.1	1.04403	[-4, -4, -3, -1, -3, -4, -2, -2, -4, -4]    
#print(analyzer.lexicon['worth'])
# 0.9	0.9434	[0, 0, 1, 1, 2, 1, 1, 3, 0, 0]   
#print(analyzer.lexicon['worthless'])
# -1.9	1.13578	[-3, -1, -3, -4, -1, -3, -1, -1, -1, -1]  
#print(analyzer.lexicon['shit'])
# -2.6	1.0198	[-2, -1, -4, -3, -4, -4, -2, -2, -2, -2]

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
#          Uncertanty (297 terms)
#          Constraining (184 terms)
#          Positve (354 terms)

# Double entries:
# -> The word lists also contain terms that are already occuring in the Vader lexicon
# -> In this case the score from Vader is kept and only new words are scored
# -> For more information please see addtional script on GitHub called "dictionary_update"

# NOTE: The word lists have been manually copy and pasted
# -> This allows it to run the program without downloading addtional files
# -> To see how we collcected and scored the terms please see addtional script on GitHub called "dictionary_update"

uncertainties_words = {"abeyance": -1.5 , "abeyances": -1.5 , "almost": -1.5 , "alteration": -1.5 , "alterations": -1.5, "ambiguities": -1.5 , "ambiguity": -1.5 , "ambiguous": -1.5 , "anomalies": -1.5 , "anomalous": -1.5 , 
"anomalously": -1.5 , "anomaly": -1.5 , "anticipate": -1.5 , "anticipated": -1.5 , "anticipates": -1.5 , "anticipating": -1.5 , "anticipation": 0.4 , "anticipations": -1.5 , "apparent": -1.5 , "apparently": -1.5 , 
"appear": -1.5 , "appeared": -1.5 , "appearing": -1.5 , "appears": -1.5 , "approximate": -1.5 , "approximated": -1.5 , "approximately": -1.5 , "approximates": -1.5 , "approximating": -1.5 , "approximation": -1.5 , 
"approximations": -1.5 , "arbitrarily": -1.5 , "arbitrariness": -1.5 , "arbitrary": -1.5 , "assume": -1.5 , "assumed": -1.5 , "assumes": -1.5 , "assuming": -1.5 , "assumption": -1.5 , "assumptions": -1.5 , 
"believe": -1.5 , "believed": -1.5 , "believes": -1.5 , "believing": -1.5 , "cautious": -0.4 , "cautiously": -1.5 , "cautiousness": -1.5 , "clarification": -1.5 , "clarifications": -1.5 , "conceivable": -1.5 , 
"conceivably": -1.5 , "conditional": -1.5 , "conditionally": -1.5 , "confuses": -1.3 , "confusing": -0.9 , "confusingly": -1.4 , "confusion": -1.2 , "contingencies": -1.5 , "contingency": -1.5 , "contingent": -1.5 , 
"contingently": -1.5 , "contingents": -1.5 , "could": -1.5 , "crossroad": -1.5 , "crossroads": -1.5 , "depend": -1.5 , "depended": -1.5 , "dependence": -1.5 , "dependencies": -1.5 , "dependency": -1.5 ,
"dependent": -1.5 , "depending": -1.5 , "depends": -1.5 , "destabilizing": -1.5 , "deviate": -1.5 , "deviated": -1.5 , "deviates": -1.5 , "deviating": -1.5 , "deviation": -1.5 , "deviations": -1.5 , "differ": -1.5 , 
"differed": -1.5 , "differing": -1.5 , "differs": -1.5 , "doubt": -1.5 , "doubted": -1.1 , "doubtful": -1.4 , "doubts": -1.2 , "exposure": -1.5 , "exposures": -1.5 , "fluctuate": -1.5 , "fluctuated": -1.5 , "fluctuates": -1.5 , 
"fluctuating": -1.5 , "fluctuation": -1.5 , "fluctuations": -1.5 , "hidden": -1.5 , "hinges": -1.5 , "imprecise": -1.5 , "imprecision": -1.5 , "imprecisions": -1.5 , "improbability": -1.5 , "improbable": -1.5 , "incompleteness": -1.5 , 
"indefinite": -1.5 , "indefinitely": -1.5 , "indefiniteness": -1.5 , "indeterminable": -1.5 , "indeterminate": -1.5 , "inexact": -1.5 , "inexactness": -1.5 , "instabilities": -1.5 , "instability": -1.5 , "intangible": -1.5 , "intangibles": -1.5 , 
"likelihood": -1.5 , "may": -1.5 , "maybe": -1.5 , "might": -1.5 , "nearly": -1.5 , "nonassessable": -1.5 , "occasionally": -1.5 , "ordinarily": -1.5 , "pending": -1.5 , "perhaps": -1.5 , "possibilities": -1.5 , "possibility": -1.5 , "possible": -1.5 , 
"possibly": -1.5 , "precaution": -1.5 , "precautionary": -1.5 , "precautions": -1.5 , "predict": -1.5 , "predictability": -1.5 , "predicted": -1.5 , "predicting": -1.5 , "prediction": -1.5 , "predictions": -1.5 , "predictive": -1.5 , "predictor": -1.5 , 
"predictors": -1.5 , "predicts": -1.5 , "preliminarily": -1.5 , "preliminary": -1.5 , "presumably": -1.5 , "presume": -1.5 , "presumed": -1.5 , "presumes": -1.5 , "presuming": -1.5 , "presumption": -1.5 , "presumptions": -1.5 , 
"probabilistic": -1.5 , "probabilities": -1.5 , "probability": -1.5 , "probable": -1.5 , "probably": -1.5 , "random": -1.5 , "randomize": -1.5 , "randomized": -1.5 , "randomizes": -1.5 , "randomizing": -1.5 , "randomly": -1.5 , 
"randomness": -1.5 , "reassess": -1.5 , "reassessed": -1.5 , "reassesses": -1.5 , "reassessing": -1.5 , "reassessment": -1.5 , "reassessments": -1.5 , "recalculate": -1.5 , "recalculated": -1.5 , "recalculates": -1.5 , "recalculating": -1.5 , 
"recalculation": -1.5 , "recalculations": -1.5 , "reconsider": -1.5 , "reconsidered": -1.5 , "reconsidering": -1.5 , "reconsiders": -1.5 , "reexamination": -1.5 , "reexamine": -1.5 , "reexamining": -1.5 , "reinterpret": -1.5 , "reinterpretation": -1.5 , 
"reinterpretations": -1.5 , "reinterpreted": -1.5 , "reinterpreting": -1.5 , "reinterprets": -1.5 , "revise": -1.5 , "revised": -1.5 , "risk": -1.1 , "risked": -0.9 , "riskier": -1.4 , "riskiest": -1.5 , "riskiness": -1.3 , "risking": -1.3 , 
"risks": -1.1 , "risky": -0.8 , "roughly": -1.5 , "rumors": -1.5 , "seems": -1.5 , "seldom": -1.5 , "seldomly": -1.5 , "sometime": -1.5 , "sometimes": -1.5 , "somewhat": -1.5 , "somewhere": -1.5 , "speculate": -1.5 , "speculated": -1.5 ,
"speculates": -1.5 , "speculating": -1.5 , "speculation": -1.5 , "speculations": -1.5 , "speculative": 0.4 , "speculatively": -1.5 , "sporadic": -1.5 , "sporadically": -1.5 , "sudden": -1.5 , "suddenly": -1.5 , "suggest": -1.5 , "suggested": -1.5 , 
"suggesting": -1.5 , "suggests": -1.5 , "susceptibility": -1.5 , "tending": -1.5 , "tentative": -1.5 , "tentatively": -1.5 , "turbulence": -1.5 , "uncertain": -1.2 , "uncertainly": -1.4 , "uncertainties": -1.4 , "uncertainty": -1.4 , "unclear": -1.0 , 
"unconfirmed": -0.5 , "undecided": -0.9 , "undefined": -1.5 , "undesignated": -1.5 , "undetectable": -1.5 , "undeterminable": -1.5 , "undetermined": -1.5 , "undocumented": -1.5 , "unexpected": -1.5 , "unexpectedly": -1.5 , "unfamiliar": -1.5 , 
"unfamiliarity": -1.5 , "unforecasted": -1.5 , "unforseen": -1.5 , "unguaranteed": -1.5 , "unhedged": -1.5 , "unidentifiable": -1.5 , "unidentified": -1.5 , "unknown": -1.5 , "unknowns": -1.5 , "unobservable": -1.5 , "unplanned": -1.5 ,
"unpredictability": -1.5 , "unpredictable": -1.5 , "unpredictably": -1.5 , "unpredicted": -1.5 , "unproved": -1.5 , "unproven": -1.5 , "unquantifiable": -1.5 , "unquantified": -1.5 , "unreconciled": -1.5 ,
"unseasonable": -1.5 , "unseasonably": -1.5 , "unsettled": -1.3 , "unspecific": -1.5 , "unspecified": -1.5 , "untested": -1.5 , "unusual": -1.5 , "unusually": -1.5 , "unwritten": -1.5 , "vagaries": -1.5 , "vague": -0.4 ,
"vaguely": -1.5 , "vagueness": -1.5 , "vaguenesses": -1.5 , "vaguer": -1.5 , "vaguest": -1.5 , "variability": -1.5 , "variable": -1.5 , "variables": -1.5 , "variably": -1.5 , "variance": -1.5 ,
"variances": -1.5 , "variant": -1.5 , "variants": -1.5 , "variation": -1.5 , "variations": -1.5 , "varied": -1.5 , "varies": -1.5 , "vary": -1.5 , "varying": -1.5 , "volatile": -1.5 , "volatilities": -1.5 , "volatility": -1.5}

constraining_words = {"abide": -1.0 ,
"abiding": -1.0 , "bound": -1.0 , "bounded": -1.0 , "commit": 1.2 , "commitment": 1.6 , "commitments": 0.5 , "commits": 0.1 , "committed": 1.1 , "committing": 0.3 , "compel": -1.0 , "compelled": 0.2 , "compelling": 0.9 ,
"compels": -1.0 , "comply": -1.0 , "compulsion": -1.0 , "compulsory": -1.0 , "confine": -1.0 , "confined": -1.0 , "confinement": -1.0 , "confines": -1.0 , "confining": -1.0 , "constrain": -1.0 ,
"constrained": -0.4 , "constraining": -1.0 , "constrains": -1.0 , "constraint": -1.0 , "constraints": -1.0 , "covenant": -1.0 , "covenanted": -1.0 , "covenanting": -1.0 , "covenants": -1.0 , "depend": -1.0 , 
"dependance": -1.0 , "dependances": -1.0 , "dependant": -1.0 , "dependencies": -1.0 , "dependent": -1.0 , "depending": -1.0 , "depends": -1.0 , "dictate": -1.0 , "dictated": -1.0 , "dictates": -1.0 ,
"dictating": -1.0 , "directive": -1.0 , "directives": -1.0 , "earmark": -1.0 , "earmarked": -1.0 , "earmarking": -1.0 , "earmarks": -1.0 , "encumber": -1.0 , "encumbered": -1.0 , "encumbering": -1.0 ,
"encumbers": -1.0 , "encumbrance": -1.0 , "encumbrances": -1.0 , "entail": -1.0 , "entailed": -1.0 , "entailing": -1.0 , "entails": -1.0 , "entrench": -1.0 , "entrenched": -1.0 , "escrow": -1.0 , "escrowed": -1.0 ,
"escrows": -1.0 , "forbade": -1.0 , "forbid": -1.3 , "forbidden": -1.8 , "forbidding": -1.9 , "forbids": -1.3 , "impair": -1.0 , "impaired": -1.0 , "impairing": -1.0 , "impairment": -1.0 ,
"impairments": -1.0 , "impairs": -1.0 , "impose": -1.2 , "imposed": -0.3 , "imposes": -0.4 , "imposing": -0.4 , "imposition": -1.0 , "impositions": -1.0 , "indebted": -1.0 , "inhibit": -1.6 ,
"inhibited": -0.4 , "inhibiting": -0.4 , "inhibits": -0.9 , "insist": -1.0 , "insisted": -1.0 , "insistence": -1.0 , "insisting": -1.0 , "insists": -1.0 , "irrevocable": -1.0 , "irrevocably": -1.0 ,
"limit": -1.0 , "limiting": -1.0 , "limits": -1.0 , "mandate": -1.0 , "mandated": -1.0 , "mandates": -1.0 , "mandating": -1.0 , "mandatory": 0.3 , "manditorily": -1.0 , "necessitate": -1.0 , "necessitated": -1.0 ,
"necessitates": -1.0 , "necessitating": -1.0 , "noncancelable": -1.0 , "noncancellable": -1.0 , "obligate": -1.0 , "obligated": -1.0 , "obligates": -1.0 , "obligating": -1.0 , "obligation": -1.0 ,
"obligations": -1.0 , "obligatory": -1.0 , "oblige": -1.0 , "obliged": -1.0 , "obliges": -1.0 , "permissible": -1.0 , "permission": -1.0 , "permissions": -1.0 , "permitted": -1.0 , "permitting": -1.0 , "pledge": -1.0 ,
"pledged": -1.0 , "pledges": -1.0 , "pledging": -1.0 , "preclude": -1.0 , "precluded": -1.0 , "precludes": -1.0 , "precluding": -1.0 , "precondition": -1.0 , "preconditions": -1.0 , "preset": -1.0 ,
"prevent": 0.1 , "prevented": 0.1 , "preventing": -0.1 , "prevents": 0.3 , "prohibit": -1.0 , "prohibited": -1.0 , "prohibiting": -1.0 , "prohibition": -1.0 , "prohibitions": -1.0 , "prohibitive": -1.0 ,
"prohibitively": -1.0 , "prohibitory": -1.0 , "prohibits": -1.0 , "refrain": -1.0 , "refraining": -1.0 , "refrains": -1.0 , "require": -1.0 , "required": -1.0 , "requirement": -1.0 , "requirements": -1.0 ,
"requires": -1.0 , "requiring": -1.0 , "restrain": -1.0 , "restrained": -1.0 , "restraining": -1.0 , "restrains": -1.0 , "restraint": -1.0 , "restraints": -1.0 , "restrict": -1.6 , "restricted": -1.6 ,
"restricting": -1.6 , "restriction": -1.1 , "restrictions": -1.0 , "restrictive": -1.0 , "restrictively": -1.0 , "restrictiveness": -1.0 , "restricts": -1.3 , "stipulate": -1.0 , "stipulated": -1.0 ,
"stipulates": -1.0 , "stipulating": -1.0 , "stipulation": -1.0 , "stipulations": -1.0 , "strict": -1.0 , "stricter": -1.0 , "strictest": -1.0 , "strictly": -1.0 , "unavailability": -1.0 , "unavailable": -1.0}

positive_words = {"able": 1.5 , "abundance": 1.5 , "abundant": 1.5 , "acclaimed": 1.5 , "accomplish": 1.8 , "accomplished": 1.9 , "accomplishes": 1.7 , "accomplishing": 1.5 , "accomplishment": 1.5 ,
"accomplishments": 1.5 , "achieve": 1.5 , "achieved": 1.5 , "achievement": 1.5 , "achievements": 1.5 , "achieves": 1.5 , "achieving": 1.5 , "adequately": 1.5 , "advancement": 1.5 , "advancements": 1.5 ,
"advances": 1.5 , "advancing": 1.5 , "advantage": 1.0 , "advantaged": 1.4 , "advantageous": 1.5 , "advantageously": 1.9 , "advantages": 1.5 , "alliance": 1.5 , "alliances": 1.5 , "assure": 1.4 ,
"assured": 1.5 , "assures": 1.3 , "assuring": 1.6 , "attain": 1.5 , "attained": 1.5 , "attaining": 1.5 , "attainment": 1.5 , "attainments": 1.5 , "attains": 1.5 , "attractive": 1.9 , "attractiveness": 1.8 ,
"beautiful": 2.9 , "beautifully": 2.7 , "beneficial": 1.9 , "beneficially": 2.4 , "benefit": 2.0 , "benefited": 1.5 , "benefiting": 1.5 , "benefitted": 1.7 , "benefitting": 1.9 , "best": 3.2 ,
"better": 1.9 , "bolstered": 1.5 , "bolstering": 1.5 , "bolsters": 1.5 , "boom": 1.5 , "booming": 1.5 , "boost": 1.7 , "boosted": 1.5 , "breakthrough": 1.5 , "breakthroughs": 1.5 , "brilliant": 2.8 ,
"charitable": 1.7 , "collaborate": 1.5 , "collaborated": 1.5 , "collaborates": 1.5 , "collaborating": 1.5 , "collaboration": 1.5 , "collaborations": 1.5 , "collaborative": 1.5 , "collaborator": 1.5 ,
"collaborators": 1.5 , "compliment": 2.1 , "complimentary": 1.9 , "complimented": 1.8 , "complimenting": 2.3 , "compliments": 1.7 , "conclusive": 1.5 , "conclusively": 1.5 , "conducive": 1.5 ,
"confident": 2.2 , "constructive": 1.5 , "constructively": 1.5 , "courteous": 2.3 , "creative": 1.9 , "creatively": 1.5 , "creativeness": 1.8 , "creativity": 1.6 , "delight": 2.9 , "delighted": 2.3 ,
"delightful": 2.8 , "delightfully": 2.7 , "delighting": 1.6 , "delights": 2.0 , "dependability": 1.5 , "dependable": 1.5 , "desirable": 1.3 , "desired": 1.1 , "despite": 1.5 , "destined": 1.5 ,
"diligent": 1.5 , "diligently": 1.5 , "distinction": 1.5 , "distinctions": 1.5 , "distinctive": 1.5 , "distinctively": 1.5 , "distinctiveness": 1.5 , "dream": 1.0 , "easier": 1.8 , "easily": 1.4 ,
"easy": 1.9 , "effective": 2.1 , "efficiencies": 1.6 , "efficiency": 1.5 , "efficient": 1.8 , "efficiently": 1.7 , "empower": 1.5 , "empowered": 1.5 , "empowering": 1.5 , "empowers": 1.5 ,
"enable": 1.5 , "enabled": 1.5 , "enables": 1.5 , "enabling": 1.5 , "encouraged": 1.5 , "encouragement": 1.8 , "encourages": 1.9 , "encouraging": 2.4 , "enhance": 1.5 , "enhanced": 1.5 ,
"enhancement": 1.5 , "enhancements": 1.5 , "enhances": 1.5 , "enhancing": 1.5 , "enjoy": 2.2 , "enjoyable": 1.9 , "enjoyably": 1.8 , "enjoyed": 2.3 , "enjoying": 2.4 , "enjoyment": 2.6 ,
"enjoys": 2.3 , "enthusiasm": 1.9 , "enthusiastic": 2.2 , "enthusiastically": 2.6 , "excellence": 3.1 , "excellent": 2.7 , "excelling": 2.5 , "excels": 2.5 , "exceptional": 1.5 , "exceptionally": 1.5 ,
"excited": 1.4 , "excitement": 2.2 , "exciting": 2.2 , "exclusive": 0.5 , "exclusively": 1.5 , "exclusiveness": 1.5 , "exclusives": 1.5 , "exclusivity": 1.5 , "exemplary": 1.5 , "fantastic": 2.6 ,
"favorable": 2.1 , "favorably": 1.6 , "favored": 1.8 , "favoring": 1.8 , "favorite": 2.0 , "favorites": 1.8 , "friendly": 2.2 , "gain": 2.4 , "gained": 1.6 , "gaining": 1.8 , "gains": 1.4 ,
"good": 1.9 , "great": 3.1 , "greater": 1.5 , "greatest": 3.2 , "greatly": 1.5 , "greatness": 1.5 , "happiest": 3.2 , "happily": 2.6 , "happiness": 2.6 , "happy": 2.7 , "highest": 1.5 ,
"honor": 2.2 , "honorable": 2.5 , "honored": 2.8 , "honoring": 2.3 , "honors": 2.3 , "ideal": 2.4 , "impress": 1.9 , "impressed": 2.1 , "impresses": 2.1 , "impressing": 2.5 , "impressive": 2.3 ,
"impressively": 2.0 , "improve": 1.9 , "improved": 2.1 , "improvement": 2.0 , "improvements": 1.3 , "improves": 1.8 , "improving": 1.8 , "incredible": 1.5 , "incredibly": 1.5 , "influential": 1.9 ,
"informative": 1.5 , "ingenuity": 1.5 , "innovate": 2.2 , "innovated": 1.5 , "innovates": 2.0 , "innovating": 1.5 , "innovation": 1.6 , "innovations": 1.5 , "innovative": 1.9 , "innovativeness": 1.5 ,
"innovator": 1.5 , "innovators": 1.5 , "insightful": 1.5 , "inspiration": 2.4 , "inspirational": 2.3 , "integrity": 1.6 , "invent": 1.5 , "invented": 1.5 , "inventing": 1.5 , "invention": 1.5 ,
"inventions": 1.5 , "inventive": 1.5 , "inventiveness": 1.5 , "inventor": 1.5 , "inventors": 1.5 , "leadership": 1.5 , "leading": 1.5 , "loyal": 2.1 , "lucrative": 1.5 , "meritorious": 2.1 ,
"opportunities": 1.6 , "opportunity": 1.8 , "optimistic": 1.3 , "outperform": 1.5 , "outperformed": 1.5 , "outperforming": 1.5 , "outperforms": 1.5 , "perfect": 2.7 , "perfected": 2.7 ,
"perfectly": 3.2 , "perfects": 1.6 , "pleasant": 2.3 , "pleasantly": 2.1 , "pleased": 1.9 , "pleasure": 2.7 , "plentiful": 1.5 , "popular": 1.8 , "popularity": 2.1 , "positive": 2.6 , "positively": 2.4 ,
"preeminence": 1.5 , "preeminent": 1.5 , "premier": 1.5 , "premiere": 1.5 , "prestige": 1.5 , "prestigious": 1.5 , "proactive": 1.8 , "proactively": 1.5 , "proficiency": 1.5 , "proficient": 1.5 ,
"proficiently": 1.5 , "profitability": 1.1 , "profitable": 1.9 , "profitably": 1.6 , "progress": 1.8 , "progressed": 1.5 , "progresses": 1.5 , "progressing": 1.5 , "prospered": 1.5 , "prospering": 1.5 ,
"prosperity": 1.5 , "prosperous": 2.1 , "prospers": 1.5 , "rebound": 1.5 , "rebounded": 1.5 , "rebounding": 1.5 , "receptive": 1.5 , "regain": 1.5 , "regained": 1.5 , "regaining": 1.5 ,
"resolve": 1.6 , "revolutionize": 1.5 , "revolutionized": 1.5 , "revolutionizes": 1.5 , "revolutionizing": 1.5 , "reward": 2.7 , "rewarded": 2.2 , "rewarding": 2.4 , "rewards": 2.1 ,
"satisfaction": 1.9 , "satisfactorily": 1.6 , "satisfactory": 1.5 , "satisfied": 1.8 , "satisfies": 1.8 , "satisfy": 2.0 , "satisfying": 2.0 , "smooth": 1.5 , "smoothing": 1.5 , "smoothly": 1.5 ,
"smooths": 1.5 , "solves": 1.1 , "solving": 1.4 , "spectacular": 1.5 , "spectacularly": 1.5 , "stability": 1.5 , "stabilization": 1.5 , "stabilizations": 1.5 , "stabilize": 1.5 , "stabilized": 1.5 ,
"stabilizes": 1.5 , "stabilizing": 1.5 , "stable": 1.2 , "strength": 2.2 , "strengthen": 1.3 , "strengthened": 1.8 , "strengthening": 2.2 , "strengthens": 2.0 , "strengths": 1.7 ,"strong": 2.3 ,
"stronger": 1.6 , "strongest": 1.9 , "succeed": 2.2 , "succeeded": 1.8 , "succeeding": 2.2 , "succeeds": 2.2 , "success": 2.7 , "successes": 2.6 , "successful": 2.8 , "successfully": 2.2 ,
"superior": 2.5 , "surpass": 1.5 , "surpassed": 1.5 , "surpasses": 1.5 , "surpassing": 1.5 , "transparency": 1.5 , "tremendous": 1.5 , "tremendously": 1.5 , "unmatched": -0.3 , "unparalleled": 1.5 ,
"unsurpassed": 1.5 , "upturn": 1.5 , "upturns": 1.5 , "valuable": 2.1 , "versatile": 1.5 , "versatility": 1.5 , "vibrancy": 1.5 , "vibrant": 2.4 , "win": 2.8 , "winner": 2.8 , "winners": 2.1 , "winning": 2.4 , "worthy": 1.9}

analyzer.lexicon.update(uncertainties_words)
analyzer.lexicon.update(constraining_words)
analyzer.lexicon.update(positive_words)

#%% ADDING WORDS TO LEXICON that still are missing (e.g. slang terms for cryptocurrencies)

new_words = {"sell": -3, "buy": 3, "moon": 2.5, "mooning": 2.5, "diamond": 1.5, "paper": -1.5, "fomo": 1.5, "shill": -2, "hodl": 1.5, "rekt": -2, "pump": 1.6, "down": -2.0, "downwards": -2.0, "up": 2.0, "upwards": 2.0}

analyzer.lexicon.update(new_words)

# Check if added word is in the lexicon:
# print(analyzer.lexicon["moon"])

#%% CREATE_HEADERS
def create_headers(bearer_token):
    # PURPOSE: This function provides the bearer token to the API.
    # INPUT:   bearer_token
    # OUTPUT:  headers
    # USAGE:   create_headers(bearer_token)
    
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    
    return headers

#%% GET_RULES
def get_rules(headers, bearer_token):
    # PURPOSE: This function requests the current rules in place.
    # INPUT:   headers, bearer_token
    # OUTPUT:  response.json()
    # USAGE:   get_rules(headers, bearer_token)
    
    response = requests.get("https://api.twitter.com/2/tweets/search/stream/rules", headers=headers)
    
    if response.status_code != 200:
        raise Exception("Cannot get rules (HTTP {}): {}".format(response.status_code, response.text))
        
    print(json.dumps(response.json()))
    
    return response.json()

#%% DELETE_ALL_RULES 
def delete_all_rules(headers, bearer_token, rules):
    # PURPOSE: This function resets all rules.
    # INPUT:   headers, bearer_token, rules
    # OUTPUT:  print(json.dumps(response.json()))
    # USAGE:   delete_all_rules(headers, bearer_token, rules)
    
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post("https://api.twitter.com/2/tweets/search/stream/rules", headers = headers, json = payload)
    
    if response.status_code != 200:
        raise Exception("Cannot delete rules (HTTP {}): {}".format( response.status_code, response.text))
        
    print(json.dumps(response.json()))

#%% SET_RULES
def set_rules(headers, delete, bearer_token):
    # PURPOSE: This function defines the rules on what tweets to pull.
    # INPUT:   headers, delete, bearer_token
    # OUTPUT:  print(json.dumps(response.json()))
    # USAGE:   set_rules(headers, delete, bearer_token)
    
    # We may adjust the rules if needed:
    sample_rules = [{"value": b, "tag": a}] # {"value": "cat has:images -grumpy", "tag": "cat pictures"}
    payload = {"add": sample_rules}
    response = requests.post("https://api.twitter.com/2/tweets/search/stream/rules", headers = headers, json = payload)
    
    if response.status_code != 201:
        raise Exception("Cannot add rules (HTTP {}): {}".format(response.status_code, response.text))
        
    print(json.dumps(response.json()))

#%% MOVING_AVERAGE
def moving_average(x, N):
    # PURPOSE: This function calculates the moving average
    # INPUT:   x (list of numbers), N (integer)
    # OUTPUT:  a vector as that is the running mean of the input vector
    # USAGE:   running_mean(x, N)
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)

#%% GET_STREAM

def get_stream(headers, set, bearer_token):
    # PURPOSE: This function starts the Twitter stream
    # INPUT:   headers, delete, bearer_token
    # OUTPUT:  BUY/HOLD/SELL Rating, Sentiment scores
    # USAGE:   get_stream(headers, set, bearer_token):
        
    # Initialize lists to save sentiment score and for plotting:
    sentimentList = []
    x_vec = [1]
    my_range = c
    N = d
    
    response = requests.get("https://api.twitter.com/2/tweets/search/stream", headers=headers, stream=True)
    print(response.status_code)
    
    if response.status_code != 200:
        raise Exception("Cannot get stream (HTTP {}): {}".format(response.status_code, response.text))
        
    for response_line in response.iter_lines():
        
        if response_line:
            json_response = json.loads(response_line)
            tweet = json_response['data']['text']
            tweet = tweet.replace(':', '')
            try:
                if detect(tweet) == 'en' and len(sentimentList) < my_range:
                    # Function from VADER (sentiment analysis model that measures polarity and intensity of emotions)
                    vs = analyzer.polarity_scores(tweet)
                    # Polarity score witch compound index from -1 (negative) to +1 (positve)
                    # \033 (Escape code for colour); 0 (no effect for style); resetting the colour coding
                    print("\033[0;0m {:-<65} {}".format(tweet, str(vs))) 
                    # Storing the compound sentiment score in the empty list sentimentList
                    sentimentList.append(vs["compound"])
                    # PLOT RUNNING MEAN OF SENTIMENT SCORES LIVE
                    y_vec = sentimentList
                    # Create N-Moving Average from sentiment scores
                    y_vec = moving_average(y_vec, N)
                    # Plot the N-moving average
                    plt.plot(x_vec, y_vec, color ='b', linestyle = '-', label = str(N) +"-Mov. Avg.")
                    # Create dashed lines that indicate cutoffs between Buy/Hold/Sell ratings
                    plt.axhline(y =  0.66, color = 'k', linestyle = 'dashed')
                    plt.axhline(y =  0.33, color = 'k', linestyle = 'dashed')
                    plt.axhline(y =  0.00, color = 'k', linestyle = 'dashed')
                    plt.axhline(y = -0.33, color = 'k', linestyle = 'dashed')
                    plt.axhline(y = -0.66, color = 'k', linestyle = 'dashed')
                    # Add shading in the colors green, yellow, red to the areas indicating Buy/Hold/Sell ratings
                    plt.axhspan( 1.00,  0.33, facecolor = 'g', alpha = 0.25, label = "Buy")
                    plt.axhspan( 0.33, -0.33, facecolor = 'y', alpha = 0.25, label = "Hold")
                    plt.axhspan(-0.33, -1.00, facecolor = 'r', alpha = 0.25, label = "Sell")
                    # Fix x-axis limits in advance to 'my_range'
                    plt.xlim([1, my_range-N+2])
                    # Pre-define x-axis ticks frequency
                    plt.xticks(np.arange(1, my_range-N+2, step = (my_range-N+1) // 10))
                    # Fix y-axis limits between -1 and +1 (range of sentiment scores)
                    plt.ylim([-1, 1])
                    # Fix y-axis ticks
                    plt.yticks([-1.00, -0.66, -0.33, 0.00, 0.33, 0.66, 1.00])
                    # Add plot title, x-axis label and y-axis label.
                    plt.title(str(N) +"-Mov. Avg. of Twitter Sent. Scores for Term " +"'" +a.upper() +"'")
                    plt.xlabel("Tweet Number")
                    # Add a legend
                    plt.legend(loc = "upper left")
                    # Pause the plot shortly after every iteration
                    plt.pause(0.05)
                    # Add 1 to x_vector after every iteration
                    x_vec.append(x_vec[-1] + 1) 
                    
                    # PRINT SENTIMENT SCORES FOR INDIVIDUAL TWEETS
                    if vs["compound"] > 0.33:
                        # \033 (Escape code for colour; 1 (bold style); 32 (Bright Green); 40m (black background colour)
                        print("\033[1;32;40m Net sentiment score:", vs["compound"], "\n")
                        
                    elif vs["compound"] < -0.33:
                        # \033 (Escape code for colour; 1 (bold style); 31 (Red); 40m (black background colour)
                        print("\033[1;31;40m Net sentiment score:", vs["compound"], "\n")
                        
                    else:
                        # \033 (Escape code for colour; 1 (bold style); 33 (Yellow); 40m (black background colour)
                        print("\033[1;33;40m Net sentiment score:", vs["compound"], "\n")
                        
                # PRINT BUY/HOLD/SELL RATING  BASED ON AVERAGE SENTIMENT OF LAST N SCORES
                if len(sentimentList) != 0 and len(sentimentList)%my_range == 0:
                    endList = sentimentList[-N:]
                    print("\033[0;0m ********* Sentiment mean score of last " +str(N) +" tweets: " + str(round(np.mean(endList), 2)))
                    
                    # summary about the inputs
                    print("----------------------------------------------------------------------------------")
                    print("----------------------------------------------------------------------------------")
                    print("Ok. We are done. Based on ", c, " tweets about '", a, "' we evaluated their sentiment score.", 
                          " Based on a moving average of ", d, "you will find our suggestion below.", sep = "")
                    print(" No investment advice! Any liability excluded!!", sep = "")
                    print("----------------------------------------------------------------------------------")
                    print("----------------------------------------------------------------------------------")  
                                                
                    # Printing out the BUY/HOLD/SELL rating based on the sentiment of the last my_range tweets
                    if np.mean(endList) >= 0.33:
                        print("\033[1;32;40m========================================================================")
                        print("|>                                                                    <|")
                        print("|>                                                                    <|")
                        print("|>                                                                    <|")
                        print("|>                              !!!!!                                 <|")
                        print("|>                              !BUY!                                 <|")
                        print("|>                              !!!!!                                 <|")
                        print("|>                               " + str("%.2f" % round(np.mean(endList), 2)) + "                                 <|")
                        print("|>                                                                    <|")
                        print("|>                                                                    <|")
                        print("|>                                                                    <|")
                        print("========================================================================")
                        
                    elif np.mean(endList) <= -0.33:
                        print("\033[1;31;40m========================================================================")
                        print("|>                                                                    <|")
                        print("|>                                                                    <|")
                        print("|>                                                                    <|")
                        print("|>                                                                    <|")
                        print("|>                               !!!!                                 <|")
                        print("|>                               SELL                                 <|")
                        print("|>                               !!!!                                 <|")
                        print("|>                               " + str("%.2f" % round(np.mean(endList), 2)) + "                                 <|")
                        print("|>                                                                    <|")
                        print("|>                                                                    <|")
                        print("|>                                                                    <|")
                        print("|>                                                                    <|")
                        print("========================================================================")
                        
                    else:
                        print("\033[1;33;40m========================================================================")
                        print("|>                                                                    <|")
                        print("|>                                                                    <|")
                        print("|>                                                                    <|")
                        print("|>                                                                    <|")
                        print("|>                                HOLD                                <|")
                        print("|>                                " + str("%.2f" % round(np.mean(endList), 2)) + "                                <|")
                        print("|>                                                                    <|")
                        print("|>                                                                    <|")
                        print("|>                                                                    <|")
                        print("|>                                                                    <|")
                        print("========================================================================")
                    break # Break the loop once you reached the desired amount of sentiment scores ('my_range')
            except:
                pass
            
#%% RUN THE PROGRAM
def main():
    # PURPOSE: This function runs the whole program.
    bearer_token = BEARER_TOKEN
    headers = create_headers(bearer_token)
    rules = get_rules(headers, bearer_token)
    delete = delete_all_rules(headers, bearer_token, rules)
    set = set_rules(headers, delete, bearer_token)
    get_stream(headers, set, bearer_token)

if __name__ == "__main__":
    main()
    
#%% END OF PROGRAM
