from flask import Flask, render_template, request
import pandas as pd
import plotly.graph_objs as go
import os

app = Flask(__name__)

# Generate or load dummy stock data
def load_or_generate_dummy_data():
    if not os.path.exists('dummy_stock_data.csv'):
        generate_dummy_data()
    return pd.read_csv('dummy_stock_data.csv')

def generate_dummy_data():
    data = {
        'Date': pd.date_range(start='2022-01-01', end='2022-12-31'),
        'AAPL': [100 + i for i in range(365)],
        'GOOGL': [200 + i for i in range(365)],
        'MSFT': [150 + i for i in range(365)]
    }
    df = pd.DataFrame(data)
    df.to_csv('dummy_stock_data.csv', index=False)

df = load_or_generate_dummy_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot', methods=['POST'])
def plot():
    selected_stocks = request.form.getlist('stocks')

    traces = []
    for stock in selected_stocks:
        trace = go.Scatter(x=df['Date'], y=df[stock], mode='lines', name=stock)
        traces.append(trace)

    layout = go.Layout(title='Stock Prices', xaxis=dict(title='Date'), yaxis=dict(title='Price'))
    fig = go.Figure(data=traces, layout=layout)
    plot_div = fig.to_html(full_html=False)

    return render_template('plot.html', plot_div=plot_div)

if __name__ == '__main__':
    app.run(debug=True)
