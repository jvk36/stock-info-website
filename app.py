from flask import Flask, render_template, request
from datetime import datetime
import src.json_data as json_data
import src.api_data as api_data

app = Flask(__name__)

# Define a custom filter for date formatting
@app.template_filter('dateformat')
def dateformat(value):
    # Convert the ISO string to a datetime object
    date_obj = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S+0000")
    # Return a formatted date string (change format as needed)
    return date_obj.strftime('%Y-%m-%d')

# Example function to return stock info (same as before)
def get_stock_info(ticker):
    stock_data = {
        'AAPL': {
            'name': 'Apple Inc', 
            'stock_exchange': 'NASDAQ Stock Exchange',
            'splits': [
                {'date': '2020-08-31', 'split_factor': '4:1'},
                {'date': '2014-06-09', 'split_factor': '7:1'}
            ],
            'dividends': [
                {'date': '2023-02-15', 'dividend': '0.22'},
                {'date': '2022-11-10', 'dividend': '0.22'}
            ],
            'prices': [
                {'date': '2024-10-09T00:00:00+0000', 'close': 172.99, 'volume': 50000000},
                {'date': '2024-10-08T00:00:00+0000', 'close': 170.50, 'volume': 45000000}
            ]
        }
    }
    return stock_data.get(ticker.upper(), {'name': 'Unknown', 'stock_exchange': 'Unknown', 'splits': [], 'dividends': [], 'prices': []})

@app.route('/', methods=['GET', 'POST'])
def index():
    stock_info = None
    if request.method == 'POST':
        ticker = request.form['ticker']
        # stock_info = get_stock_info(ticker) # get the hardcoded data for testing purposes
        # stock_info = json_data.get_stock_data() # get the data from the json files for testing purposes.
        stock_info = api_data.get_stock_data(ticker) # get data from the marketstack api
    return render_template('index.html', stock_info=stock_info)

if __name__ == '__main__':
    app.run(debug=True)
