## 🧠 AI Agent Assistant - Django + React + LlamaIndex + OpenAi

An intelligent full-stack AI-powered web assistant that allows users to:

Chat with a ReAct agent using OpenAI + LlamaIndex

Retrieve real-time stock, crypto, weather, and news data

Ask questions about PDFs 

Save and manage notes

Built with Django (Backend), React (Frontend).

## 🚀 Features

Feature              Description

🧠 ReAct Agent       Uses tools to answer user prompts intelligently

📈 Stock, Crypto, Finance       Real-time data via Alpha Vantage API

🌦️ Weather & News       Fetches daily data using news & weather engines

📄 PDF Upload + Indexing        Upload PDFs and query via LlamaIndex

📝 Notes        Create, delete, and list user notes

🔐 Auth     JWT-based secure authentication

## 🛠️ Tech Stack

Frontend:

* React + Vite

* Axios for HTTP

* JWT stored in localStorage

Backend:

* Django + Django Rest Framework

* JWT Auth (djangorestframework-simplejwt)

* LlamaIndex

* OpenAI

## 🧪 Running Locally

1. Clone repo & install backend

```
cd backend
python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

2. Set .env

```
# backend/.env
OPENAI_API_KEY=sk-...
ALPHA_VANTAGE_API_KEY=...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

```

3. Frontend (React)

```
cd frontend
npm install
npm run dev
```

## 🤖 Tools You Can Ask the Agent About
Below are real prompts you can try with the AI agent:

📄 PDF Uploads
![PDF Upload](./pdf%20upload%202.PNG)

After uploading a PDF, you can ask:

* "What algorithms are discussed in the L18_worksheet PDF?"

* "Can you summarize the contents of my 'L18_worksheet' PDF?"

📈 Crypto & Stock Price
![Crytpo/Stock tool](./crptyo%20and%20stock%20tool.PNG)

* "What is the latest price of Tesla stock?"

* "How is Ethereum performing today?"

📊 Top Gainers & Losers
![Top Gainers Tool](./top%20gainers%20tool.PNG)

* "Who are the top gainers and losers in the stock market today?"

* "Can you tell me the top 5 gainers only?"

📰 News & Sentiment
![News Tool](./news%20tool.PNG)

* "Give me recent news headlines about Nvidia."

* "What's the market sentiment on Nvidia stock?"

🌦️ Weather
![Weather Tool](./weather%20tool.PNG)

* "What's the weather like in Sacramento right now?"

* "Can you put that into Fahrenheit?"

## 📜 Credits

Inspired by:

Tech with Tim's Django AI Projects

## 🧠 Author

Kaleb — Solo dev building AI assistants

GitHub: @kalebcoleman