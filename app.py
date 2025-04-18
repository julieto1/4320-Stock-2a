import os
import requests
import csv
from flask import Flask, render_template, request
import pygal
from pygal.style import Style
import lxml

app = Flask(__name__)

# Load the available stock symbols from the CSV file
def load_stock_symbols():
    stock_symbols = []
    with open('stocks.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            stock_symbols.append(row[0])  # Assuming symbols are in the first column
    return stock_symbols

# Function to get stock data from Alpha Vantage API
def get_stock_data(symbol, time_series, start_date, end_date):
    series = None
    frame = None

    if time_series == 1:
        frame = "Time Series (5min)"
        series = "TIME_SERIES_INTRADAY"
    elif time_series == 2:
        frame = "Time Series (Daily)"
        series = "TIME_SERIES_DAILY"
    elif time_series == 3:
        frame = "Weekly Time Series"
        series = "TIME_SERIES_WEEKLY"
    elif time_series == 4:
        frame = "Monthly Time Series"
        series = "TIME_SERIES_MONTHLY"

    url = f'https://www.alphavantage.co/query?function={series}&symbol={symbol}&interval=5min&apikey=your_api_key'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return filter_data(data, frame, start_date, end_date)
    else:
        return response.status_code

# Function to filter the stock data based on the time series and dates
def filter_data(data, frame, start_date, end_date):
    if frame is None:
        print("Error Getting Frame")
        quit()

    time_series = data.get(f"{frame}", {})

    open_prices = []
    high_prices = []
    low_prices = []
    close_prices = []

    for timestamp, values in time_series.items():
        date = timestamp.split(' ')[0]
        if start_date <= date <= end_date:
            open_prices.append(float(values["1. open"]))
            high_prices.append(float(values["2. high"]))
            low_prices.append(float(values["3. low"]))
            close_prices.append(float(values["4. close"]))

    return open_prices, high_prices, low_prices, close_prices

# Function to render the stock chart
def render_chart(chart_type, opens, highs, lows, closes):
    custom_style = Style(
        background='white',
        plot_background='white',
        foreground='black',
        foreground_strong='black',
        foreground_subtle='grey',
        colors=('blue', 'green', 'red', 'orange')
    )

    if chart_type == 1:  # Line chart
        chart = pygal.Line(style=custom_style)
        chart.title = 'Stock Prices (Line Chart)'
        chart.add('Close', closes)
        filename = 'line_chart.svg'

    elif chart_type == 2:  # Bar chart
        chart = pygal.Bar(style=custom_style, width=1200, height=600)
        chart.title = 'Stock Prices (Bar Chart)'
        chart.add('Open', opens)
        chart.add('High', highs)
        chart.add('Low', lows)
        chart.add('Close', closes)
        filename = 'bar_chart.svg'

    chart.render_to_file(os.path.join("static", filename))

    return filename

@app.route('/', methods=['GET', 'POST'])
def index():
    # Load stock symbols
    stock_symbols = load_stock_symbols()

    # Default selected symbol and chart data
    selected_symbol = None
    chart_filename = None
    symbol_data = None
    start_date = None
    end_date = None

    if request.method == 'POST':
        selected_symbol = request.form.get('symbol')
        chart_type = int(request.form.get('chart_type'))
        time_series = int(request.form.get('time_series'))
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        # Fetch the stock data
        opens, highs, lows, closes = get_stock_data(selected_symbol, time_series, start_date, end_date)

        # Render the chart
        chart_filename = render_chart(chart_type, opens, highs, lows, closes)

    return render_template('index.html', 
                           stock_symbols=stock_symbols, 
                           selected_symbol=selected_symbol, 
                           chart_filename=chart_filename,
                           start_date=start_date,
                           end_date=end_date)

if __name__ == '__main__':
    app.run(debug=True)
