import requests
from dotenv import load_dotenv
import os
from llama_index.core.tools import FunctionTool

load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

def get_top_gainers_losers():
    url = f'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={ALPHA_VANTAGE_API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"RequestException: {e}. Unable to retrieve data from the API."
    except Exception as e:
        return f"An error occurred: {e}"

top_gainers_losers_tool = FunctionTool.from_defaults(
    fn=get_top_gainers_losers,
    name="top_gainers_losers",
    description="This tool retrieves the top gainers, losers, and most actively traded tickers in the US market. so when you are asked about the top gainers and losers use this tool. DO NOT INPUT ANYTHING INSIDE Action Input."
)
