# Sentiment-Analysis
---
*** About ***

This is a student project of the University of St. Gallen of the course Skills - Programming with Advanced Computer Languages (8,789,1.00).
The goal of this project was to build a python based script to analyze tweets about crypto currencies in real time and make buy, sell or hold suggestions 
based on a certain amount of currently analyzed tweets.
***
*** Pre-requisites ***

We recommend using the Spyder IDE (Version 4.1.5/4.2.5 currently working with Python version 3.8.1/3.8.8) since the program plots the live sentiment, which is
best displayed in the mentioned IDE.

To actually run the code, the vaderSentiment as well as the langdetect libraries need to be installed. Simply write "pip install vaderSentiment" 
respectively "pip install langdetect" to download them.
Apart from those rather unusual libraries the libraries requests, json, numpy and matplotlib need to be installed as well.

The script gets live tweets through the Twitter developer API, which needs a personal token for authentification (bearer token) to accept the requests 
of the script. Please create your own bearer token, since the one written in the current script is not guaranteed to be accessible forever.
To access the Twitter Developer platform, a Twitter account is needed. The personal bearer token to access the Twitter API can be created by following
the following link and following each step in the Developer portal: https://developer.twitter.com/en
***
*** Instructions ***

<img width="571" alt="Bildschirmfoto 2021-05-26 um 09 45 16" src="https://user-images.githubusercontent.com/82701839/119700465-894cb200-be53-11eb-9ab1-96d320eb8f0e.png">


1. download this repository or copy the code into you IDE. 
2. Make sure that all pre-requisites are met. We highly recommend using the Spyder IDE and making the "Plots" window visible (which is usually in the upper
right corner).
3. (Recommended) Exchange the existing bearer token with your own bearer token in code line 52.
4. Run the code.
5. Fill in the wanted input (search tag/term, the amount of analyzed tweets, the amount of tweets counting for the moving average).
6. Wait for a couple seconds until enough tweets are collected and watch the live generated Twitter sentiment analysis graph.
***
*** Files ***
- Code File:
- Dictionary Update script: dictionary_update.py
- Financial lexicon: LoughranMcDonald_SentimentWordLists_2018.xslx
- Vader lexicon: vader_lexicon.xslx
***
*** Description ***

The code analyses the sentiment of tweets in real time. The code therefore is structured as follows:

1. Access and communication to and with the Twitter API

- The code interacts with the Twitter API through five functions, "create_headers", "get_rules", "delete_all_rules", "set_rules" and "get_stream".

- "create_headers": This function provides the bearer token to the API.
- "get_rules": This function requests the current rules in place.
- "delete_all_rules": This function resets all rules.
- "set_rules": This function defines the rules on what tweets to pull, which sends the requested tweets e.g. "bitcoin" to the API.
- "get_stream": This function starts the Twitter stream and tweets are being collected.

         Through these functions the rules on what tweets to pull can be influenced as well as the live stream being started.

2. Analysis of the collected tweets and allocation of a sentiment score between -1.00 (strong negative sentiment) and 1.00 (strong positive sentiment).

- With the help of the Vader lexicon, which is additionally updated with manually classified financial terms from the Loughran-McDonald sentiment word list, the streamed tweets are being analyzed.

         About the Loughran-McDonald sentiment word lists
         - developed word lists to be used for financial content analysis
         - term classifications regarding a large sample of 10Ks
         - different categories of words lists like (negative, positive, uncertainty, constraining, etc.)

Source and further information about the development of the word list
- Loughran, Tim and McDonald, Bill, When is a Liability not a Liability?
- Textual Analysis, Dictionaries, and 10-Ks (March 4, 2010)
- Journal of Finance, Forthcoming
- Available at SSRN: https://ssrn.com/abstract=1331573

Use for updating the Vader lexicon
- Some lists are taken to update the Vader lexicon
- The goal is to improve the sentiment score in the context of financial terms
- To see how the strings of terms are created please see the additional dictionary_update script on github
- The addition of follwoing word lists have been made:
         Uncertanty (297 terms)
         Constraining (184 terms)
         Positve (354 terms)

Double entries:
- The word lists also contain terms that are already occuring in the Vader lexicon
- In this case the score from Vader is kept and only new words are scored
- For more information please see addtional script on GitHub called "dictionary_update"

NOTE: The word lists have been manually copy and pasted
- This allows it to run the program without downloading addtional files
- To see how we collcected and scored the terms please see addtional script on GitHub called "dictionary_update"

3. Plotting of the analysed tweets based on the moving average of the N last tweets.

- To make the current sentiment and its change over the past short time period more readable and interpretable, the data is being visualized by plotting the moving average.
At the end of the analysed time frame, a buy, sell or hold suggestion is displayed.