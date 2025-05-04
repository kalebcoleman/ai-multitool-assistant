import requests
from dotenv import load_dotenv
import os
import re
from llama_index.core.tools import FunctionTool

load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

def get_stock_price(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()
    if 'Time Series (5min)' in data:
        latest_time = list(data['Time Series (5min)'].keys())[0]
        latest_close = data['Time Series (5min)'][latest_time]['4. close']
        return f"The latest closing price of {symbol} is ${latest_close}."
    else:
        return 'Stock symbol not found or API limit reached.'

def financial_tool(prompt):
    match = re.search(r'stock price of (\w+)', prompt, re.IGNORECASE)
    if match:
        symbol = match.group(1).upper()
        return get_stock_price(symbol)
    else:
        return 'Invalid prompt. Please ask for the stock price using the format: "stock price of [SYMBOL]"'

financial_engine = FunctionTool.from_defaults(
    fn=financial_tool,
    name="financial_data",
    description="This tool provides the latest stock price for a specified symbol. You need to use the format: 'stock price of [SYMBOL]' if you are not given the SYMBOL you still need to use it so make sure you find the right symbol for the task. if you are asked for random stocks you still must provide specific symbols.",
)
