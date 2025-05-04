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

* "What's the price of Ethereum?"

* "Give me the latest Tesla stock news"

* "Summarize the PDF I just uploaded"

* "What's the weather in New York?"

* "Who are the top gainers today?"

## 📜 Credits

Inspired by:

Tech with Tim's Django AI Projects

## 🧠 Author

Kaleb — Solo dev building AI assistants

GitHub: @kalebcoleman