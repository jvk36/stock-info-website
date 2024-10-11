import os
import requests
from dotenv import load_dotenv


load_dotenv()

# *******************************************************************************
# Setup an account using the free tier at https://marketstack.com/ 
# to get an API Key restricted to 100 requests per month.
# *******************************************************************************
MARKETSTACK_API_KEY = os.environ["MARKETSTACK_API_KEY"]


def get_ticker_data(ticker):
    ticker_data_url = "https://api.marketstack.com/v1/tickers/" + ticker + "?access_key=" + MARKETSTACK_API_KEY
    response = requests.get(ticker_data_url)
    data = response.json()
    return {"name": data["name"], "stock_exchange": data["stock_exchange"]["name"]}

def get_splits_data(ticker):
    splits_data_url = "https://api.marketstack.com/v1/splits?symbols=" + ticker + "&access_key=" + MARKETSTACK_API_KEY
    response = requests.get(splits_data_url)
    data = response.json()
    return data["data"]

def get_dividends_data(ticker):
    dividends_data_url = "https://api.marketstack.com/v1/dividends?symbols=" + ticker + "&access_key=" + MARKETSTACK_API_KEY
    response = requests.get(dividends_data_url)
    data = response.json()
    return data["data"]

def get_eod_data(ticker):
    eod_data_url = "https://api.marketstack.com/v1/eod?symbols=" + ticker + "&access_key=" + MARKETSTACK_API_KEY
    response = requests.get(eod_data_url)
    data = response.json()
    return data["data"]

def get_stock_data(ticker):
    stock_data = get_ticker_data(ticker)
    stock_data["splits"] = get_splits_data(ticker)
    stock_data["dividends"] = get_dividends_data(ticker)
    stock_data["prices"] = get_eod_data(ticker)
    return stock_data
