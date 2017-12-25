# McAfee-Tweet-Crypto-Bot
A simple python bot which read McAfee's tweets for the coin of the day, buys it at +3% of current price and sells at 2x

This bot doesn't require your twitter developer keys as it uses the twitter's frontend API with some HTML parsing to get the tweets.

Only your Bittrex API keys are needed. You can get them here "https://bittrex.com/Manage#sectionApi". Just Generate a new key will all the 4 permissions as 'on'.

The only thing you need to change to use this bot is in `src/mcafee.py`. Enter your own bittrex API keys in the place of `<API KEY>` and `<API SECRET>`.

To change amount of bitcoin you will be using, just edit `main.py` and change the variable `BTCTOBUY` variable to any amount.
