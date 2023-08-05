import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv

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



