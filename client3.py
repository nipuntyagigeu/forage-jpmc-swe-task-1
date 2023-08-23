import json
import random
import urllib.request

# Server API URLs
QUERY = "http://localhost:8080/query?id={}"

# 500 server request
N = 500

def getDataPoint(quote):
    """ Produce all the needed values to generate a datapoint """
    stock = quote['stock']
    bid_price = float(quote['top_bid']['price'])
    ask_price = float(quote['top_ask']['price'])
    price = (bid_price + ask_price) / 2  # Calculate average of bid and ask prices
    return stock, bid_price, ask_price, price

def getRatio(price_a, price_b):
    """ Get ratio of price_a and price_b """
    if price_b == 0:
        return None  # Avoid division by zero
    return price_a / price_b  # Calculate the ratio

# Main
if __name__ == "__main__":
    # Query the price once every N seconds.
    prices = {}  # Dictionary to store stock prices
    
    for _ in iter(range(N)):
        quotes = json.loads(urllib.request.urlopen(QUERY.format(random.random())).read())
        
        for quote in quotes:
            stock, bid_price, ask_price, price = getDataPoint(quote)
            print("Quoted %s at (bid:%s, ask:%s, price:%s)" % (stock, bid_price, ask_price, price))
            prices[stock] = price  # Store the price in the dictionary
        
        if "stockA" in prices and "stockB" in prices:
            ratio = getRatio(prices["stockA"], prices["stockB"])
            if ratio is not None:
                print("Ratio %s" % ratio)
            else:
                print("Cannot calculate ratio due to division by zero.")
        else:
            print("Cannot calculate ratio as price data is missing for one or both stocks.")
