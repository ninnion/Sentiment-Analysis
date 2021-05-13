# Load modules
# ---------------------------------------------------------------------------

# import pandas as pd
# -> not used
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
# import os
import json
# import config
# -> for hierarchical configuration scheme with support for mappings and sequences
# import preprocessor as p
# -> not used (apperently)
# -> suited for simple preprocessing of Python files
from langdetect import detect
# -> for language detection
# from csv import writer
# -> not used
# from ernie import SentenceClassifier
import numpy as np
# classifier = SentenceClassifier(model_path='./output')


# Asking for input
# ---------------------------------------------------------------------------

# aks for an input that should be searched
a = (input("Hi! Enter a term or word that you want to get the live Twitter sentiment: "))

# try if entered input can be transformed into a string
# otherwise the user will be asked again to enter a input
while type(a)!=str:
  try:
    a = str(a)
  except:
    print("Only strings can be counted!")
    a = (input("Please try again with a string? "))
    continue

# check if entered word is only one word
while len(a.split()) != 1:
    print("You entered more than one word or nothing")
    a = input("Please try again and enter only ONE term? ")

b = "#" + a
# add the hashtag to the term for the search later

# to think about: case sensitivity!!
#   should we put the input all to lower case: a.lower() -> would be better for hashtags, but not good for Ticker search (e.g. BTC, AAPL)


# Bearer Token
# ---------------------------------------------------------------------------

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAGdBNgEAAAAAebL5tbsCMiq7TRRAskhG67nHrAg%3DyfHiDGamgrGsx9xfCBQ2Xacjoa1Xm8PbhqdNu763aAj3lRfi2m"


# Getting the tweets
# ---------------------------------------------------------------------------

def Average(lst):
    if len(lst == 0):
        return len(lst)
    else:
        return sum(lst[-neededSentiments: ]) / neededSentiments

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def get_rules(headers, bearer_token):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(headers, bearer_token, rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(headers, delete, bearer_token):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": b, "tag": a},
        #{"value": "cat has:images -grumpy", "tag": "cat pictures"},
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))

    
# Customize dictionary
# ---------------------------------------------------------------------------
# about the compound score
# -> most used by researches
# -> between -1 (most extreme negative) and 1 (most extreme positive)
# -> positve >= 0.5
# -> negative <= -0.5
# -> between - 0.5 and 0.5

# about the pos, neg, neu ratios
# -> proportions, add up to 1
# -> raw categorization, no VADER rule-based enhancements applied
# -> no word-order sensitivity, modifiers, amplifiers, negation polarity switches, or contrastive conjunction sensitivity

# about the lexicon
# -> stored as: vader_lexicon.txt
# -> labels: TOKEN, MEAN-SENTIMENT-RATING, STANDARD DEVIATION, and RAW-HUMAN-SENTIMENT-RATINGS
# -> NOTE: The current algorithm makes immediate use of the first two elements (token and mean valence)
# -> The final two elements (SD and raw ratings) are provided for rigor
# -> you should find 10 independent humans to evaluate/rate each new token you want to add to the lexicon
# -> make sure the standard deviation doesn't exceed 2.5, and take the average rating for the valence
# -> each word is assigned a sentiment score (between -4 and +4)

# Examples:
    # best	3.2	0.6	[2, 4, 4, 3, 4, 3, 3, 3, 3, 3]
      # print(analyzer.lexicon["best"])
    # good	1.9	0.9434	[2, 1, 1, 3, 2, 4, 2, 2, 1, 1]
      # print(analyzer.lexicon["good"])
    # bad	-2.5	0.67082	[-3, -2, -4, -3, -2, -2, -3, -2, -2, -2]
      # print(analyzer.lexicon["bad"])
    # worst	-3.1	1.04403	[-4, -4, -3, -1, -3, -4, -2, -2, -4, -4]
      # print(analyzer.lexicon["worst"])
    # worth	0.9	0.9434	[0, 0, 1, 1, 2, 1, 1, 3, 0, 0]
      # print(analyzer.lexicon["worth"])
    # worthless	-1.9	1.13578	[-3, -1, -3, -4, -1, -3, -1, -1, -1, -1]
      # print(analyzer.lexicon["worthless"])
    # shit	-2.6	1.0198	[-2, -1, -4, -3, -4, -4, -2, -2, -2, -2]
      # print(analyzer.lexicon["shit"])

analyzer = SentimentIntensityAnalyzer()

# ADDING new words to the lexicon (NOT WORKING)
#new_words = {
    #"sell": -2.5, "buy": 2.5, "moon": 1.5, "down": -2.0, "downwards": -2.0,
    #"up": 2.0, "upwards": 2.0
    #}
#analyzer.lexicon.update(new_words)

# ADDING new words to the lexicon (WORKING)
analyzer.lexicon.update({"sell": -2.5, "buy": 2.5, "moon": 1.5, "down": -2.0, "downwards": -2.0,
                         "up": 2.0, "upwards": 2.0
                        })

# Check if added word is in the lexicon
# print(analyzer.lexicon["sell"])

# REMOVING words from the lexicon (NOT WORKING)
analyzer.lexicon.pop("miss")

# Check if added word is still in the lexicon
# print(analyzer.lexicon["miss"])
# -> should get you an error message


# Tweet Stream and Sentiment Analysis with VADER
# ---------------------------------------------------------------------------

sentimentList = []
# empty list to store the compound sentiment score afterwards
neededSentiments = 500
# QUESTION: neededSentiment set to 500 (do not remeber why??)

def get_stream(headers, set, bearer_token):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", headers=headers, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            #print(json.dumps(json_response, indent=4, sort_keys=True))
            tweet = json_response['data']['text']
            #tweet = p.clean(tweet)
            tweet = tweet.replace(':', '')
            #print(tweet)
            try:
                if detect(tweet) == 'en':
                    # Function from VADER (sentiment analysis model that measures polarity and intensity of emotions)
                    vs = analyzer.polarity_scores(tweet)
                    # Polarity score witch compound index from -1 (negative) to +1 (positve)
                    print("\033[0;0m {:-<65} {}".format(tweet, str(vs)))
                    # \033 (Escape code for colour); 0 (no effect for style); resetting the colour coding
                    sentimentList.append(vs["compound"])
                    # storing the compound sentiment score in the empty list sentimentList
                    if vs["compound"] > 0.5:
                        print("\033[1;32;40m Net sentiment score:", vs["compound"], "\n")
                        # \033 (Escape code for colour; 1 (bold style); 32 (Bright Green); 40m (black background colour)
                    elif vs["compound"] < -0.5:
                        print("\033[1;31;40m Net sentiment score:", vs["compound"], "\n")
                        # \033 (Escape code for colour; 1 (bold style); 31 (Red); 40m (black background colour)
                    else:
                        print("\033[1;33;40m Net sentiment score:", vs["compound"], "\n")
                        # \033 (Escape code for colour; 1 (bold style); 33 (Yellow); 40m (black background colour)
                 if len(sentimentList)%50 == 0:
                    endList = sentimentList[-50:]
                    print("\033[0;0m ********* Sentiment mean score of last 50 tweets: " + str(np.mean(endList)))
                    # print("\033[0;0m ********* Net sentiment score of last 50 tweets: " + str(sum(endList)))
                    # average of the compound sentiment score of last 50 tweets
                    # QUESTION: What is the better measure here? mean or sum?
                            
                    # printing out the general suggestion based on the sentiment of the last 50 tweets
                    if np.mean(endList) > 0.5:
                        print("\033[1;32;40m========================================================================")
                        print("|>                                                                    <|")
                        print("|>                              !!!!!                                 <|")
                        print("|>                              !BUY!                                 <|")
                        print("|>                              !!!!!                                 <|")
                        print("|>                                                                    <|")
                        print("========================================================================")
                    if np.mean(endList) < -0.5:
                       print("\033[1;31;40m========================================================================")
                       print("|>                                                                    <|")
                       print("|>                               !!!!                                 <|")
                       print("|>                               SELL                                 <|")
                       print("|>                               !!!!                                 <|")
                       print("|>                                                                    <|")
                       print("========================================================================")
                    else:
                       print("\033[1;33;40m========================================================================")
                       print("|>                                                                    <|")
                       print("|>                                                                    <|")
                       print("|>                    Uncertain or neutral sentiment                  <|")
                       print("|>                                                                    <|")
                       print("|>                                                                    <|")
                       print("========================================================================")
                      
                      
                      
                      
                    ##try:
                    #     -1 Bearish, 0 Neutral, 1 Bullish
                    #     classes = ['BEARISH', 'NEUTRAL', 'BULLISH']
                    ##    probabilites = classifier.predict_one(tweet)
                    ##    polarity = (classes[np.argmax(probabilites)]
                    ##    sentimentList.append(polarity)

                    ##    if len(sentimentList) > 50:
                    ##         endList = sentimentList[-50:]
                    ##         print('********* Total Bullish: ' + str(endList.count('BULLISH')))
                    ##         print('********* Total Bearish: ' + str(endList.count('BEARISH')))

                    ##         if endList.count('BULLISH') > 40:
                    ##         # BUY Signal
                    ##         elif endList.count('BEARISH') > 40:
                    ##         # SELL Signal
                    ## except:
                    ##    pass
                    #tweetlst = [tweet]

                    #with open('bitcoindata.csv', 'a+', newline='') as write_obj:
                    #  csv_writer = writer(write_obj)
                    #  csv_writer.writerow(tweetlst)
            except:
                pass

def main():
    bearer_token = BEARER_TOKEN
    headers = create_headers(bearer_token)
    rules = get_rules(headers, bearer_token)
    delete = delete_all_rules(headers, bearer_token, rules)
    set = set_rules(headers, delete, bearer_token)
    get_stream(headers, set, bearer_token)


if __name__ == "__main__":
    main()
