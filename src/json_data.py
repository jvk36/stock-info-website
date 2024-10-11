import json

def get_ticker_data():
    with open("./json/ticker-data.json", "r") as file:
        data = json.load(file)
        # print(type(data))
        return {"name": data["name"], "stock_exchange": data["stock_exchange"]["name"]}

def get_splits_data():
    with open("./json/splits-data.json", "r") as file:
        data = json.load(file)
        # print(type(data))
        return data["data"]

def get_dividends_data():
    with open("./json/dividends-data.json", "r") as file:
        data = json.load(file)
        # print(type(data))
        return data["data"]

def get_eod_data():
    with open("./json/eod-data.json", "r") as file:
        data = json.load(file)
        # print(type(data))
        return data["data"]

def get_stock_data():
    stock_data = get_ticker_data()
    stock_data["splits"] = get_splits_data()
    stock_data["dividends"] = get_dividends_data()
    stock_data["prices"] = get_eod_data()
    return stock_data
