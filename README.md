# Sentiment-Analysis

## About

**Welcome** to the student project of **group No. 2306** of the course **Skills: Programming with Advanced Computer Languages (8,789,1.00)** taught by **Dr. Mario Silic** at the **University of St. Gallen**.  

The goal of this project was to build a **Python** based script to analyze the **Twitter sentiment** about **crypto-currencies**, display the sentiment graphically **in real time** and generate **buy, sell or hold** recommendations based on a window of the most recent tweets.  

Additional information and details about the inner workings of our code can also be found in the comments of our script.  

**Members of Group No. 2306**

  | Name               | Student ID | CodingXCamp ID | GitHub ID        |
  | ------------------ |:----------:|:-------------: |:----------------:|
  | Julian Flemming    | 16-608-143 | JulianF.       | ninnion          |
  | Simona Heim        | 15-613-623 | tapioca        | tapioca7         |
  | Alexandre Moine    | 15-052-319 | MrPineapple    | GoldenPineappleR |
  | Matthias Spichiger | 15-937-667 | Matt 32        | MatthiasSP       |

### Pre-requisites
----
We recommend using the **Spyder IDE** (Version 4.2.5, currently working with Python version 3.8.8) since the program plots the twitter sentiment *live*, which is
best displayed in the mentioned IDE in a **seperate plotting pane**.  

To run the code, the libraries `vaderSentiment` and `langdetect` need to be installed and loaded.  
To install them, simply write 
- `pip install vaderSentiment` and 
- `pip install langdetect` 
in your command prompt (e.g. in the Anaconda Prompt).  

Apart from these two libraries, the libraries  
- `requests`  
- `json`
- `numpy`
- `matplotlib`  

need to be loaded as well, as outlined at the very beginning of the script.  

The script accesses live tweets through the Twitter Developer API, which demands a personal token for authentification (called 'bearer token') to accept the HTTP GET-requests 
of this script.  

Please create your own bearer token, since the one written in the current script can not guarantee access to the Twitter API indefinitely.  
To create your own bearer token, create a Twitter account and access the Twitter Developer platform, by clicking on this [link](https://developer.twitter.com/en) and following the instructions step-by-step.


### Instructions
----
1. Download this repository or copy the code into your IDE.  

2. Make sure that all pre-requisites are met. We highly recommend using the Spyder IDE and making the "Plots" window visible (found in the upper
right corner). We also recommend using the default settings of your IDE, since otherwise the plotting may not be displayed as intended.

3. (Recommended) Exchange the existing bearer token with your own bearer token in code line 52.

4. Run the file `2306_sentiment_analysis.py ` in your IDE.

5. Fill in the input requested in the console window of your IDE (search tag/term, number of tweets to be analyzed, moving average window).

6. Wait a couple seconds until enough tweets are collected for the Twitter sentiment to be plotted live in your plotting pane.


### Files
----
This GitHub page contains the following files:
- Code File: `2306_sentiment_analysis.py`
- Dictionary Update script: `dictionary_update.py`
- Financial lexicon: `LoughranMcDonald_SentimentWordLists_2018.xslx`
- Vader lexicon: `vader_lexicon.xslx`


### Description
----
The code analyses the sentiment of tweets obtained via the Twitter API in real time, assings each tweet a sentiment score, displays it graphically and in the console window, and generates a Buy / Hold / Sell recommendation based on the most recent average sentiment.  
The code therefore is structured as follows:

#### 1. Access and communication to and with the Twitter API

The code interacts with the Twitter API through five functions; `create_headers`, `get_rules`, `delete_all_rules`, `set_rules` and `get_stream`.

- `create_headers`: This function provides the bearer token to the API.
- `get_rules`: This function requests the current rules in place.
- `delete_all_rules`: This function resets all rules.
- `set_rules`: This function defines the rules on which tweets to pull from the API, by sending the search term (e.g. "bitcoin") to the API.
- `get_stream`: This function starts the Twitter stream and the tweets are being collected, analyzed and displayed.

#### 2. Analysis of the collected tweets

With the help of the [Vader lexicon](https://github.com/cjhutto/vaderSentiment), which is additionally updated with manually classified financial terms from the Loughran-McDonald sentiment [word list](https://sraf.nd.edu/textual-analysis/resources/#Master%20Dictionary), the streamed tweets are being analyzed and assigned a sentiment score between -1.00 (strong negative sentiment) and 1.00 (strong positive sentiment).

Quick note about the Loughran-McDonald sentiment word lists:
- Developed word lists to be used for financial content analysis
- Term classifications regarding a large sample of 10Ks
- Different categories of words lists like (negative, positive, uncertainty, constraining, etc.)

Source and further information about the development of the word list:
- Loughran, Tim and McDonald, Bill, When is a Liability not a Liability?
- Textual Analysis, Dictionaries, and 10-Ks (March 4, 2010)
- Journal of Finance, Forthcoming
- Available at [SSRN](https://ssrn.com/abstract=1331573)

Use for updating the Vader lexicon:
- Three dictionaries are being used to update the Vader lexicon.
- The goal is to improve the sentiment score in the context of financial terms.
- These dictionaries are of the following size:

  | Wordlist      | number of terms|
  | ------------- |:--------------:|
  | Uncertainty   | 297 terms      |
  | Constraining  | 184 terms      |
  | Positive      | 354 terms      |

Double entries:
- The dictionaries may contain terms that are already in the Vader lexicon.
- In this case the score from Vader is kept and only new words are scored.

**NOTE**: The word lists have been manually copied and pasted.
- This allows the user to run the program without having to download any addtional files (you are very welcome).

Youu may find a more detailed information about the dictionary expansion in our additonal script `dictionary_update.py`:
- How we collected and scored the terms.
- How the strings of terms are created.
- And how we treated double entries.

#### 3. Plotting of the analysed tweets

To make the current sentiment and its change over the past short time period more readable and interpretable, the data is being visualized by plotting the moving average.  
The moving average depends on a window of `N` observations, which the user defined in the console window of his IDE at the start of the program.  
The moving average is defined as the function `moving_average` in the script, and it has two purposes:

1. Smoothing
It makes the line graph of the sentiment scores appear more smooth, thereby making it easier to detect trends in the live Twitter sentiment.

2. Recommendation
It increases the number of tweets that are considered for the final buy/hold/sell-recommendation, thereby making our suggestions more representative of the overall sentiment on Twitter.  

The tweets will also be displayed in the console window *live*, with each having an appropriate color scheme for the net sentimet score:
```diff
+ green for positive sentiment
! yellow for neutral sentiment
- red for negative sentiment
```
Below you can see how the plotting pane and the console output should look in your IDE while the skript is running:  

![dogecoin_running_half](https://user-images.githubusercontent.com/60882754/119815701-1d6a5800-beec-11eb-9af2-7d2f754d19d3.PNG)


#### 4. Buy | Hold | Sell - Recommendation

Once we have reached the desired number of tweets (which the user has previously defined in the console window of his IDE, i.e. the variable `my_range`), the script will automatically generate a buy/hold/sell-recommendation for the crypto-currency in question, based on the `N` most recently analyzed tweets.  

Below you can see how the bu/hold/sell-recommendation should look like in your IDE once the program has stopped running:

![dogecoin_recommendation_half](https://user-images.githubusercontent.com/60882754/119815638-0deb0f00-beec-11eb-808e-5db4b64214fa.PNG)

**Please note that this is a mere suggestion and no financial advice and that the students of this group cannot be held accountable for any transactions that the user of this script may initiate.** 

