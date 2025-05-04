import requests
from dotenv import load_dotenv
import os
import re
from llama_index.core.tools import FunctionTool

load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

def get_crypto_price(symbol):
    url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={symbol}&market=USD&apikey={ALPHA_VANTAGE_API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        data = response.json()
        if "Error Message" in data:
            return f"API Error: {data['Error Message']}. Please check the API key and symbol."
        try:
            time_series = data['Time Series (Digital Currency Daily)']
            latest_date = list(time_series.keys())[0]
            close_price = time_series[latest_date].get('4a. close (USD)', time_series[latest_date].get('4. close'))
            if not close_price:
                return "The expected data format is not present in the API response."
            return f"The latest closing price for {symbol} is {close_price} USD."
        except KeyError as e:
            return f"KeyError: {e}. It seems the expected key is not present in the API response."
    except requests.exceptions.RequestException as e:
        return f"RequestException: {e}. Unable to retrieve data from the API."
    except Exception as e:
        return f"An error occurred: {e}"

def crypto_tool(prompt):
    match = re.search(r'price of (\w+)', prompt, re.IGNORECASE)
    if match:
        symbol = match.group(1).upper()
        return get_crypto_price(symbol)
    else:
        return 'Invalid prompt. Please ask for the price using the format: "price of [CRYPTO_SYMBOL]"'



crypto_price_tool = FunctionTool.from_defaults(
    fn=crypto_tool,
    name="crypto_tool",
    description="Get current price of a cryptocurrency like bitcoin or ethereum. Do not ask like 'what is the price of ETH' you must ask 'price of [CRYPTO_SYMBOL]' for example 'price of ETH' this is to ensure we get the proper api call needed. and make sure you do not return the prompt return the answer."
)

