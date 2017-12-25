import src.tweet as tweeter
import src.mcafee as mcafee

accounts = ['officialmcafee']

BTCTOBUY = 0.4
		
#mcafee.updateCoins()
while True:
	try:
		for acct in accounts:
			newTweets = tweeter.getNewTweets(acct)
			if newTweets is not None:
				for tweet in newTweets:
					print "%s : NEW TWEET at %s\n%s\n"%(acct, tweet[1], tweet[2])
					mcafee.parseTweetAndBuy(tweet[2], BTCTOBUY)
	except:
		print "meh!"
		continue
