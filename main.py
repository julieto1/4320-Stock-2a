import requests
import pygal
import key
import lxml

def main():
    print("Stock Data Visualizer\n----------------------------\n")

    symbol = input("Enter the stock symbol you are looking for: ")
    print("----------------------------")

    chart = input("Enter chart type: \n1. Line \n2. Bar\n")
    print("----------------------------")
    chart_type = validate_chart(chart)

    time_series = input("Enter time series: \n1. Intraday \n2. Daily \n3. Weekly \n4. Monthly\n")
    print("----------------------------")
    time = validate_time(time_series)

    opens, highs, lows, closes, dates = get_symbol(symbol, time)

    if not opens or not highs or not lows or not closes or not dates:
        print("No data found. Please check the symbol and time series.")
    else:
        render_chart(chart_type, opens, highs, lows, closes, dates)

def validate_chart(chart):
    while chart not in ['1', '2']:
        print("Invalid selection. Please enter a valid chart type.")
        chart = input("Enter chart type: \n1. Line \n2. Bar\n")
    return int(chart)

def validate_time(time):
    while time not in ['1', '2', '3', '4']:
        print("Invalid selection. Please enter a valid time series.")
        time = input("Enter time series: \n1. Intraday \n2. Daily \n3. Weekly \n4. Monthly\n")
    return int(time)

def get_symbol(symbol, time):
    series = None
    frame = None

    if time == 1:
        frame = "Time Series (5min)"
        series = "TIME_SERIES_INTRADAY"
    elif time == 2:
        frame = "Time Series (Daily)"
        series = "TIME_SERIES_DAILY"
    elif time == 3:
        frame = "Weekly Time Series"
        series = "TIME_SERIES_WEEKLY"
    elif time == 4:
        frame = "Monthly Time Series"
        series = "TIME_SERIES_MONTHLY"

    url = f'https://www.alphavantage.co/query?function={series}&symbol={symbol}&interval=5min&apikey={key.key}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print("API Response Data:")
        print(data)  # Log the response for debugging
        return filter_data(data, frame)
    else:
        print(f"Error: {response.status_code}")
        return [], [], [], [], []

def filter_data(data, frame):
    if frame == None:
        print("Error Getting Frame")
        quit()

    time_series = data.get(f"{frame}", {})

    if not time_series:
        print("No time series data available for the given frame.")
        return [], [], [], [], []

    open_prices = []
    high_prices = []
    low_prices = []
    close_prices = []
    dates = []

    for timestamp, values in time_series.items():
        open_prices.append(float(values["1. open"]))
        high_prices.append(float(values["2. high"]))
        low_prices.append(float(values["3. low"]))
        close_prices.append(float(values["4. close"]))
        dates.append(timestamp)  # Ensure dates are also appended

    print(f"Dates: {dates}")  # Log dates for debugging
    return open_prices, high_prices, low_prices, close_prices, dates

def render_chart(chart_type, opens, highs, lows, closes, dates):
    if chart_type == 1:
        line_chart(opens, highs, lows, closes, dates)
    elif chart_type == 2:
        bar_chart(opens, highs, lows, closes, dates)

def line_chart(opens, highs, lows, closes, dates):
    line_chart = pygal.Line()
    line_chart.title = 'Stock Prices Over Time'

    # Ensure dates are passed as string format (this should work)
    line_chart.x_labels = [str(date) for date in dates[::5]]  # Show every 5th date label to avoid overcrowding

    # Adding data series to the line chart
    line_chart.add('Close', closes, fill_opacity=0.3)
    line_chart.add('Open', opens)
    line_chart.add('High', highs)
    line_chart.add('Low', lows)
    
    # Save and render the chart
    line_chart.render_to_file('line_chart.svg')
    print("Line chart saved as 'line_chart.svg'")

def bar_chart(opens, highs, lows, closes, dates):
    bar_chart = pygal.Bar()
    bar_chart.title = 'Stock Prices (Open, High, Low, Close)'

    # Ensure dates are passed as string format (this should work)
    bar_chart.x_labels = [str(date) for date in dates[::5]]  # Show every 5th date label to avoid overcrowding

    # Adding data series to the bar chart
    bar_chart.add('Open', opens)
    bar_chart.add('High', highs)
    bar_chart.add('Low', lows)
    bar_chart.add('Close', closes)

    # Save and render the chart
    bar_chart.render_to_file('bar_chart.svg')
    print("Bar chart saved as 'bar_chart.svg'")

if __name__ == "__main__":
    main()
