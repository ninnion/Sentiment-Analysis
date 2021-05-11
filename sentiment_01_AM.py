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
# import numpy as np
# -> not used
# classifier = SentenceClassifier(model_path='./output')


# Bearer Token
# ---------------------------------------------------------------------------
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAGdBNgEAAAAAebL5tbsCMiq7TRRAskhG67nHrAg%3DyfHiDGamgrGsx9xfCBQ2Xacjoa1Xm8PbhqdNu763aAj3lRfi2m"


# Getting the tweets
# ---------------------------------------------------------------------------

sentimentList = []
neededSentiments = 500

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
        {"value": "#bitcoin", "tag": "bitcoin"},
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


# Tweet Stream and Sentiment Analysis with VADER
# ---------------------------------------------------------------------------

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
                    analyzer = SentimentIntensityAnalyzer()
                    # Function from VADER (sentiment analysis model that measures polarity and intensity of emotions)
                    vs = analyzer.polarity_scores(tweet)
                    # Polarity score witch compound index from -1 (negative) to +1 (positve)
                    print("\033[0;0m {:-<65} {}".format(tweet, str(vs)))
                    # \033 (Escape code for colour); 0 (no effect for style); resetting the colour coding
                    if vs["compound"] > 0.5:
                        print("\033[1;32;40m Net sentiment score:", vs["compound"], "\n")
                        # \033 (Escape code for colour; 1 (bold style); 32 (Bright Green); 40m (black background colour)
                    elif vs["compound"] < -0.5:
                        print("\033[1;31;40m Net sentiment score:", vs["compound"], "\n")
                        # \033 (Escape code for colour; 1 (bold style); 31 (Red); 40m (black background colour)
                    else:
                        print("\033[1;33;40m Net sentiment score:", vs["compound"], "\n")
                        # \033 (Escape code for colour; 1 (bold style); 33 (Yellow); 40m (black background colour)
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
