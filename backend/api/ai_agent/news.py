import requests
from dotenv import load_dotenv
import os
from llama_index.core.tools import FunctionTool, ToolMetadata
import re

NEWS_API_KEY = os.getenv('NEWS_API_KEY')

def get_news(topic):
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get('articles', [])
    if articles:
        top_article = articles[0]
        return f"Top news on {topic}: {top_article['title']} - {top_article['description']}"
    else:
        return f"No news found on {topic}."

def news_tool(prompt):
    match = re.search(r'news on (\w+)', prompt, re.IGNORECASE)
    if match:
        topic = match.group(1)
        return get_news(topic)
    else:
        return 'Invalid prompt. Please ask for news using the format: "news on [TOPIC]"'

news_engine = FunctionTool.from_defaults(
    fn=news_tool,
    name="news_retrieval",
    description="This tool retrieves the latest news on a specific topic. Use the format: 'news on [TOPIC]'. Make sure you use the exact topic, not the abbreviation. For example, if you want the news on politics, you must use 'news on politics'. please do not use full sentences.",
)
