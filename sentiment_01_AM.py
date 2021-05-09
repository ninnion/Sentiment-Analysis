#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 09:54:49 2021

@author: alexandremoine
"""


import requests
# import os
import json

# import config
# for hierarchical configuration scheme with support for mappings and sequences

# import preprocessor as p
# not used (apperently)

# suited for simple preprocessing of Python files

from langdetect import detect
# for language detection

# from csv import writer
# not used

#from ernie import SentenceClassifier

# import numpy as np
# not used

# classifier = SentenceClassifier(model_path='./output')

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAGdBNgEAAAAAebL5tbsCMiq7TRRAskhG67nHrAg%3DyfHiDGamgrGsx9xfCBQ2Xacjoa1Xm8PbhqdNu763aAj3lRfi2m"

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
                    print(tweet)

                    ##try:
                    #     classes = ['Bearish', 'Neutral', 'Bullish']
                    ##    probabilites = classifier.predict_one(tweet)
                    ##    print(classes[np.argmax(probabilites)])
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