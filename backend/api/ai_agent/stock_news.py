import requests
from dotenv import load_dotenv
import os
import re
from llama_index.core.tools import FunctionTool

load_dotenv()

ALPHA_VANTAGE_API_KEY2 = os.getenv('ALPHA_VANTAGE_API_KEY2')


def get_news_sentiment(tickers=None, topics=None, time_from=None, time_to=None, sort='LATEST', limit=20):
    base_url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT'
    params = {
        'apikey': ALPHA_VANTAGE_API_KEY2,
        'sort': sort,
        'limit': limit
    }
    if tickers:
        params['tickers'] = tickers
    if topics:
        params['topics'] = topics
    if time_from:
        params['time_from'] = time_from
    if time_to:
        params['time_to'] = time_to
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        articles = data.get('feed', [])
        summarized_articles = []

        for article in articles:
            summarized_articles.append({
                'title': article.get('title', 'No title available'),
                'summary': article.get('summary', 'No summary available'),
                'sentiment': article.get('overall_sentiment_label', 'No sentiment data')
            })

        if not summarized_articles:
            return "No articles found."

        return summarized_articles
    except requests.exceptions.RequestException as e:
        return f"RequestException: {e}. Unable to retrieve data from the API."
    except Exception as e:
        return f"An error occurred: {e}"

def news_sentiment_tool(prompt):
    tickers_match = re.search(r'tickers? (\w+(,\w+)*)', prompt)
    topics_match = re.search(r'topics? (\w+(,\w+)*)', prompt)
    time_from_match = re.search(r'time_from (\d{8}T\d{4})', prompt)
    time_to_match = re.search(r'time_to (\d{8}T\d{4})', prompt)
    
    tickers = tickers_match.group(1) if tickers_match else None
    topics = topics_match.group(1) if topics_match else None
    time_from = time_from_match.group(1) if time_from_match else None
    time_to = time_to_match.group(1) if time_to_match else None
    
    return get_news_sentiment(tickers=tickers, topics=topics, time_from=time_from, time_to=time_to)

news_sentiment_tool_instance = FunctionTool.from_defaults(
    fn=news_sentiment_tool,
    name="news_sentiment",
    description="This tool retrieves market news sentiment data. You can specify tickers, topics, time range, and sort order."
)
