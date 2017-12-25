from bittrex.bittrex import *
import json
import time

myAcct = Bittrex("<API KEY>", "<API SECRET>",api_version=API_V1_1)

with open("src/Currencies", "r") as f:
	currencies = json.load(f)

with open("src/CurrenciesInverted", "r") as f:
	currenciesInverted = json.load(f)

def getLastPrice(coin):
	return myAcct.get_market_history(coin)['result'][0]['Price']

def buyCoin(coin, price, bitcoin):
	qty = (bitcoin/price)
	myAcct.buy_limit(coin,qty,price)
	return qty

def sellCoin(coin,price,qty):
	myAcct.sell_limit(coin,qty,price)

def hasOpenOrder(coin):
	return len(myAcct.get_open_orders(coin)['result']) > 0

def isValidCoin(coin):
	if coin.lower() in currencies:
		return "BTC-%s"%coin.upper()
	elif coin.lower() in currenciesInverted:
		return "BTC-%s"%currenciesInverted[coin.lower()].upper()
	else:
		return None

def getShitDone(coin,bitcoin):
	curPrice = getLastPrice(coin)
	up5 = curPrice + ((3./100) * curPrice)
	print "Buying at",up5
	boughtQty = buyCoin(coin,up5,bitcoin)
	print "Bought %f coins"%(boughtQty)
	time.sleep(1)
	up80 = curPrice + (0.8 * curPrice)
	up100 = curPrice + (1 * curPrice)
	up120 = curPrice + (1.2 * curPrice)
	while hasOpenOrder(coin):
		wait=1
	qtyBy3 = boughtQty * (1./3)
	sellCoin(coin,up80,qtyBy3)
	sellCoin(coin, up100, qtyBy3)
	sellCoin(coin, up120, qtyBy3)

def getChars(coinPart):
	return "".join([X for X in coinPart if X.isalpha()])

def parseTweetAndBuy(tweet,bitcoin):
	tweet = tweet.lower()
	if "coin of the day" in tweet:
		coinPart = tweet.split(":")[1].lstrip().split(" ")[:4]
		coinname = ""
		for part in coinPart:
			isValidFull = isValidCoin(getChars(part))
			if isValidFull is not None:
				coinname = isValidFull
				break
		if coinname == "":
			return
		print "Getting Shit Done -> %s"%coinname
		getShitDone(coinname, bitcoin)

def updateCoins():
	cns = myAcct.get_currencies()['result']
	allCr = {}
	allCr2 = {}
	for cn in cns:
		allCr[cn['Currency'].lower()] = cn['CurrencyLong'].lower()
		allCr2[cn['CurrencyLong'].lower()] = cn['Currency'].lower()

	with open("src/Currencies","w") as f:
		f.write(json.dumps(allCr))

	with open("src/CurrenciesInverted","w") as f:
		f.write(json.dumps(allCr2))
