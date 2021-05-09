#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 14:32:28 2021

@author: alexandremoine
"""

# Load packages
# ---------------------------------------------------------------------------
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# Load tweets from excel
# ---------------------------------------------------------------------------
tweets = pd.read_excel (r"/Users/alexandremoine/Documents/UNI/Master/FS_21/Programming/group_project/bitcoindata.xlsx")


# Create a new column 
# ---------------------------------------------------------------------------
tweets["Score"] = "NA"

tweets.head()

# Sentiment Intensity Analysis
# ---------------------------------------------------------------------------
analyzer = SentimentIntensityAnalyzer()
for sentence in tweets["Sentiment Text"]:
    vs = analyzer.polarity_scores(sentence)
    print("{:-<65} {}".format(sentence, str(vs)))
    tweets["Score"] = vs["compound"]
    #tweets["Score"].append(vs["compound"])
    #if tweets["Sentiment Text"] == sentence:
        #tweets["Score"] = vs["compound"]
    # MISTAKE: only takes the last vs compound when defining the value
    # no mistake when only printing vs compound
    print("Net sentiment score:", vs["compound"])


print(tweets)


# Sentiment score Average
# ---------------------------------------------------------------------------
tweets["Score"].mean()