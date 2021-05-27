# Sentiment-Analysis
----
## About
----
This is a student project of the University of St. Gallen of the course *Skills - Programming with Advanced Computer Languages (8,789,1.00)*.  
The goal of this project was to build a python based script to analyze tweets about crypto currencies in real time and generate buy, sell or hold recommendations 
based on a certain amount of currently analyzed tweets. Addiotonal information and details about how the code works can be found in the commented code itself.

### Pre-requisites
----
We recommend using the Spyder IDE (Version 4.2.5, currently working with Python version 3.8.8) since the program plots the twitter sentiment *live*, which is
best displayed in the mentioned IDE in a seperate plotting pane.  

To run the code, the libraries `vaderSentiment` and `langdetect` need to be installed and loaded. To install them, write `pip install vaderSentiment` and `pip install langdetect` in your command prompt. Apart from these two libraries, the libraries `requests`, `json`, `numpy` and `matplotlib` need to be loaded as well.

The script gets live tweets through the Twitter developer API, which needs a personal token for authentification (bearer token) to accept the requests 
of the script. Please create your own bearer token, since the one written in the current script is not guaranteed to be accessible forever. To access the Twitter Developer platform, a Twitter account is needed. The personal bearer token to access the Twitter API can be created by clicking on 
this [link](https://developer.twitter.com/en) and following the instructions step-by-step.

### Instructions
----
1. Download this repository or copy the code into your IDE. 
2. Make sure that all pre-requisites are met. We highly recommend using the Spyder IDE and making the "Plots" window visible (which is usually in the upper
right corner). We also recommend using the IDE on default settings, since otherwise the plotting may not be displayed as intended.
3. (Recommended) Exchange the existing bearer token with your own bearer token in code line 52.
4. Run the code.
5. Fill in the wanted input (search tag/term, the amount of tweets to be analyzed, the amount of tweets included in the moving average window).
6. Wait for a couple seconds until enough tweets are collected and watch the live generated Twitter sentiment analysis graph.


![DOGECOIN_INPUT](https://user-images.githubusercontent.com/60882754/119737907-1a398280-be80-11eb-9f3b-ad795078d5b7.PNG)

### Files
----
- Code File: `2306_sentiment_analysis.py`
- Dictionary Update script: `dictionary_update.py`
- Financial lexicon: `LoughranMcDonald_SentimentWordLists_2018.xslx`
- Vader lexicon: `vader_lexicon.xslx`

### Description
----
The code analyses the sentiment of tweets in real time. The code therefore is structured as follows:

1. Access and communication to and with the Twitter API

>   The code interacts with the Twitter API through five functions, `create_headers`, `get_rules`, `delete_all_rules`, `set_rules` and `get_stream`.
>
>   - `create_headers`: This function provides the bearer token to the API.
>   - `get_rules`: This function requests the current rules in place.
>   - `delete_all_rules`: This function resets all rules.
>   - `set_rules`: This function defines the rules on what tweets to pull, which sends the requested tweets e.g. "bitcoin" to the API.
>   - `get_stream`: This function starts the Twitter stream and tweets are being collected.
>
>   Through these functions the rules on what tweets to pull can be influenced as well as the live stream being started.

2. Analysis of the collected tweets and allocation of a sentiment score between -1.00 (strong negative sentiment) and 1.00 (strong positive sentiment).

>   - With the help of the [Vader lexicon](https://github.com/cjhutto/vaderSentiment), which is additionally updated with manually classified financial terms from the Loughran-McDonald sentiment [word list](https://sraf.nd.edu/textual-analysis/resources/#Master%20Dictionary), the streamed tweets are being analyzed.
>
>   About the Loughran-McDonald sentiment word lists
>   - developed word lists to be used for financial content analysis
>   - term classifications regarding a large sample of 10Ks
>   - different categories of words lists like (negative, positive, uncertainty, constraining, etc.)
>
>   Source and further information about the development of the word list
>   - Loughran, Tim and McDonald, Bill, When is a Liability not a Liability?
>   - Textual Analysis, Dictionaries, and 10-Ks (March 4, 2010)
>   - Journal of Finance, Forthcoming
>   - Available at [SSRN](https://ssrn.com/abstract=1331573)
>
>   Use for updating the Vader lexicon
>   - Some lists are taken to update the Vader lexicon
>   - The goal is to improve the sentiment score in the context of financial terms
>   - The addition of follwoing word lists have been made:
>
>     | Wordlist      | number of terms|
>     | ------------- |:--------------:|
>     | Uncertainty   | 297 terms      |
>     | Constraining  | 184 terms      |
>     | Positive      | 354 terms      |
>
>   Double entries:
>   - The word lists also contain terms that are already occuring in the Vader lexicon
>   - In this case the score from Vader is kept and only new words are scored
>
>   NOTE: The word lists have been manually copy and pasted
>   - This allows it to run the program without downloading addtional files
>
>   Please find more detailed information about the dictionary expansion in our additonal script `dictionary_update.py`:
>   - How we collected and scored the terms
>   - How the strings of terms are created
>   - And how we treated double entries

3. Plotting of the analysed tweets based on the moving average of the N last tweets.

   ![DOGECOIN_RUNNING](https://user-images.githubusercontent.com/60882754/119736808-96cb6180-be7e-11eb-8c61-cc6085596b8e.PNG)

>   - To make the current sentiment and its change over the past short time period more readable and interpretable, the data is being visualized by plotting the moving average.
>   - At the end of the analysed time frame, a buy, sell or hold suggestion is displayed.

   ![DOGECOIN_RESULT](https://user-images.githubusercontent.com/60882754/119736840-a185f680-be7e-11eb-94f5-502844e16106.PNG)
