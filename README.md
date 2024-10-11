# BEFORE RUNNING THE FILES EXECUTE THE FOLLOWING IN THE TERMINAL FROM THE WORKING FOLDER:
pip install -r requirements.txt

## Stock Info Website - Application Intro:

API Used - https://marketstack.com/ 

The Application uses the marketstack API to build a website that show information on any listed stock. The user inputs the ticker symbol of the stock he/she is interested in and it retrieves information from the API and shows it on the website.

## Application Design - Details:

The stock information website has six sections. Details follow:

1) Stock Ticker Input Section: It consists of an Edit Box to enter the Stock Ticker and a Submit button.

2) Company Information: The section is populated from the information retrieved from the API route https://api.marketstack.com/v1/tickers/{ticker}?access_key={YOUR API KEY GOES HERE}

3) Volume and Price Chart: The graph uses the JavaScript library Chart.js to show a Price and Volume Chart with Date as the X-axis. The data comes from the API route https://api.marketstack.com/v1/eod?symbols={ticker}?access_key={YOUR API KEY GOES HERE}

4) Volume and Price Grid: The section shows the same information in a Table/Spreadsheet/Grid.

5) Stock Splits Section: The section shows the stock split dates and split factor in a Table/Spreasheet/Grid.

6) Dividends Section: The section shows the dividend dates and Amount of Dividend in a Table/Spreadsheet/Grid.

## Application - Functional Description:

The stock information website is built using Python/Flask stack on the backend and HTML/CSS/Bootstrap/JavaScript for the front end. The Flask based web-server code is entirely contained in the app.py file. It uses the API using the src/api_data.py module. That module uses the requests library to retrieve the data from marketstack API. The front-end code is contained within templates/index.html. Details follow:

### app.py - Flask based webserver application code:

@app.route('/', methods=['GET', 'POST']): This single route handles the processing of the user interaction with the website. Flask's request module processes the 'POST' message when the user hits the Submit button on the website. The message is processed by accessing request.form['ticker'] that contains the ticker the user typed into the form. The stock information to be displayed on the website is then retrieved by calling api_data.get_stock_data(ticker). The dictionary that contains the information is then passed to the html template for display using Flask's template module render_template: render_template('index.html', stock_info=stock_info)

@app.template_filter('dateformat'): Defines a custom Jinja2 filter for date formatting. The html template uses this filter in the "Stock Price and Volume" section to format the date: {{ price.date | dateformat }}

get_stock_info(): The function hardcodes what is returned from a call to the API access function api_data.get_stock_data(ticker) for testing purposes. It is used by the testing module test-json-and-api.py as well. 

### templates/index.html - Front-end HTML code:

How it works overall:

1) The user enters the stock ticker in the form (e.g., AAPL for Apple).
2) When the form is submitted, a POST request is sent to the Flask server.
3) The backend function get_stock_info() retrieves the company name and stock exchange (mock data in this example).
4) The page is re-rendered with the stock information displayed below the form.

Table rendering:

1) Dividends, Splits, and price/volume information is presented using HTML tables. The table are only displayed if the corresponding data is available ({% if stock_info.<data> %}). 
2) The tables are wrapped in a div with the class .scrollable-table, which has a maximum height (max-height: 300px) and vertical scrolling (overflow-y: auto) to handle large data sets.The scrollable area only appears if the corresponding data exists.
3) The date is displayed in a more readable format by applying JavaScript to convert the ISO 8601 string (2024-10-09T00:00:00+0000) into a human-readable date format using toLocaleDateString().

Chart rendering Steps:

1) Install Chart.js: We will add Chart.js to the front-end by linking its CDN.
2) Prepare the Data: Extract the date, close, and volume from the price data and feed it to the chart.
3) Create a Canvas for the Chart: This will be where the chart is rendered.
4) Plot Price and Volume as Two Lines on the Same Graph.

Chart rendering Details:

1) Added Chart.js CDN: Chart.js is included using the CDN for rendering the graph.
2) Canvas Element: Added a <canvas> element with an ID of priceVolumeChart to display the chart.
3) JavaScript Code for Chart:
    Extracts the date, close, and volume from the stock data.
    Labels the x-axis with formatted dates.
    Plots two lines: one for the close price and one for the volume, each with a distinct color.
    The y axis is split into two, one for price and the other for volume (on the right side).
4) Styling:
    The chart is displayed beside the company information with the help of Flexbox (info-and-chart class).
    The width of both the chart and the company info is adjusted to ensure a proper layout.

NOTE: Flask uses Jinja2 as its templating engine, allowing you to embed dynamic content within your HTML files. Key concepts of the Jinja2 engine include the following:

    Templates: HTML files containing static content and placeholders for dynamic data.
    Jinja2 syntax: Special delimiters (the double curly braces {{) are used to distinguish Jinja2 code from HTML.
    Rendering: The process of replacing placeholders with actual data to generate the final HTML - Flask's render_template call.

### src/api_data.py - Data retrieval from the markstack API:

get_ticker_data(ticker), get_splits_data(ticker), get_dividends_data(ticker), and get_eod_data(ticker): These four functions return dictionaries (or list of dictionaries) that contain all the data that needs to be populated on the website.

get_stock_data(ticker): The function consolidates the data from the four function above into a single dictionary which is returned. 


## Testing Design - Details: 

The API free tier has a limit of 100 requests/month and that too for only a subset of the functionality. To avoid hitting the limits while building the website, we use two levels of hardcoded data to design, code, and test the functionality:

1) app.py - get_stock_data(ticker) function: The function returns hardcoded sample data for AAPL stock in a python dictionary  format. 

2) src/json_data.py - get_stock_data() function: The json sub-directory has 4 json files that contain real data retrieved from the API through postman for the 4 routes that we use for the program. The function reads these files and returns a consolidated python dictionary of the entire dataset:

    a) json/ticker-data.json: The file contains data returned by the marketstack API route https://api.marketstack.com/v1/tickers/{ticker}?access_key={YOUR API KEY GOES HERE} for Apple (ticker AAPL) stock. The Company Name ("name" key value) and Stock Exchange ("stock_exchange" key is a dictionary and the "name" key value under it) are the key-values that are used by our application. 

    b) json/splits-data.json: The file contains data returned by the marketstack API route https://api.marketstack.com/v1/splits?symbols={ticker}?access_key={YOUR API KEY GOES HERE} for Apple (ticker AAPL) stock. The "data" key value is a list of dictionaries. The "date" and "split_factor" are the key-values used by our application.

    c) json/dividends-data.json: The file contains data returned by the marketstack API route https://api.marketstack.com/v1/dividends?symbols={ticker}?access_key={YOUR API KEY GOES HERE} for Apple (ticker AAPL) stock. The "data" key value is a list of dictionaries. The "date" and "dividend" are the key-values used by our application.

    d) json/eod-data.json: The file contains data returned by the marketstack API route https://api.marketstack.com/v1/eod?symbols={ticker}?access_key={YOUR API KEY GOES HERE} for Apple (ticker AAPL) stock. The "data" key value is a list of dictionaries. The "date", "close", and "volume" are the key-values used by our application.

The consolidated dictionary has the following structure (taken directly from get_stock_data function in app.py):

    {
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

NOTE: The test-json-and-api.py is a wrapper around api_data.py and json_data.py. It can be used during testing to spit out the json into the terminal. 



