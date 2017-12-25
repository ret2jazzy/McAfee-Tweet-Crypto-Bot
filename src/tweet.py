import requests
import json
from bs4 import BeautifulSoup
import os.path

def getTime(obj):
	return int(obj.find('span', {'class':'_timestamp'})['data-time'])

def getReadableTime(tweet):
	return tweet.find('a',{'class':'tweet-timestamp js-permalink js-nav js-tooltip'})['title']

def getLastTime(user):
	if os.path.exists("accounts/%s"%user):
		with open("accounts/%s"%user,"r") as f:
			lastKnownTime = int(f.read())
	else:
		lastKnownTime = 0	
	return lastKnownTime

def writeTime(user,time):
	with open("accounts/%s"%user, "w") as f:
		f.write(str(time))

def getTweetData(tweet):
	return tweet.find('div', {'class':'js-tweet-text-container'}).find('p').getText()

def isRetweet(tweet):
	if tweet.find('span', {'class' : 'js-retweet-text'}):
		return True
	return False

def getTweets(user):

	data = BeautifulSoup(requests.get("https://twitter.com/i/profiles/show/%s/timeline/tweets"%(user)).json()['items_html'],'lxml')

	allTweets = data.find_all('li', {'class' : 'js-stream-item stream-item stream-item '})
	pinnedTweet = data.find('li', {'class' : 'js-stream-item stream-item stream-item js-pinned '})

	tweets = []

	if pinnedTweet is not None:
		tweets.append([getTime(pinnedTweet),getReadableTime(pinnedTweet), getTweetData(pinnedTweet)])
	for tweet in allTweets:
		if not isRetweet(tweet):
			tweets.append([getTime(tweet), getReadableTime(tweet), getTweetData(tweet)])
	tweets.sort(key=lambda tweet1: tweet1[0],reverse=True)
	return tweets

def getNewTweets(user):
	latestTweets = getTweets(user)
	lastTweetTime = getLastTime(user)
	if len(latestTweets) == 0:
		return None
	if  lastTweetTime >= latestTweets[0][0]:
		return None
	newTweets = []
	writeTime(user,latestTweets[0][0])
	for tweet in latestTweets:
		if tweet[0] > lastTweetTime:
			newTweets.append(tweet)
		else:
			return newTweets
	return newTweets


