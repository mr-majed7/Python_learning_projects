import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv
import math

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

load_dotenv()

account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
client = Client(account_sid, auth_token)

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey":os.getenv("ALPHAVANTAG_API_KEY")
}


stock_api_response = requests.get("https://www.alphavantage.co/query",params=stock_params)
closing_y = stock_api_response.json()["Time Series (Daily)"]["2023-08-04"]["4. close"]
closing_y2 = stock_api_response.json()["Time Series (Daily)"]["2023-08-03"]["4. close"]

diff = ((float(closing_y2) - float(closing_y)) / float(closing_y)) * 100



news_params = {
    "q": "Tesla",
    "from": "2023-08-04",
    "sortBy": "popularity",
    "pageSize": "3",
    "apiKey":os.getenv("NEWS_API_KEY")
}

news_api_response = requests.get("https://newsapi.org/v2/everything?",params=news_params)
articles = news_api_response.json()["articles"]

outgoing_message = ""

for article in articles:
    title = article["title"]
    description = article["description"]
    outgoing_message += f"Headline: {title}\nBrief: {description}\n"

if diff<0:
    message = client.messages \
                .create(
                     body=f"TSLA:🔻{abs(math.floor(diff))}\n{outgoing_message} ",
                     from_='+13185451545',
                     to='+8801741816439'
                 )
else:
    message = client.messages \
                .create(
                     body=f"TSLA:🔺{abs(math.floor(diff))}\n{outgoing_message} ",
                     from_='+13185451545',
                     to='+8801741816439'
                 )

