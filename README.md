# 🧠 AI Agent Assistant - Django + React + LlamaIndex + OpenAi

An intelligent full-stack AI-powered web assistant that allows users to:

- Chat with a ReAct agent using OpenAI + LlamaIndex
- Retrieve real-time stock, crypto, weather, and news data
- Ask questions about PDFs
- Save and manage notes

Built with Django (Backend), React (Frontend).

## 🚀 Quick Start

**1. Backend (Django):**
```bash
cd backend
python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**2. Frontend (React):**
```bash
cd frontend
npm install
npm run dev
```

## 🛠️ Tech Stack

*   **Frontend:** React, Vite, Axios
*   **Backend:** Django, Django Rest Framework, LlamaIndex, OpenAI
*   **Authentication:** JWT (djangorestframework-simplejwt)

## ⚙️ Configuration

Create `.env` files in the `backend` and `frontend` directories and add the following environment variables:

### Backend (`/backend/.env`)

| Variable | Description | Example |
|---|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key. | `sk-...` |
| `ALPHA_VANTAGE_API_KEY` | Your Alpha Vantage API key for stock data. | `...` |
| `OPENWEATHERMAP_API_KEY` | Your OpenWeatherMap API key for weather data. | `...` |
| `NEWS_API_KEY` | Your News API key for news headlines. | `...` |
| `SECRET_KEY` | Your Django secret key. | `django-insecure-...` |

### Frontend (`/frontend/.env`)

| Variable | Description |
|---|---|
| `VITE_API_URL` | The URL of your backend API. | `http://127.0.0.1:8000` |


## 🤖 AI Agent Tools

Below are real prompts you can try with the AI agent:

#### 📄 PDF Uploads

![PDF Upload](./images/pdf%20upload%202.PNG)

After uploading a PDF, you can ask:

*   _"What algorithms are discussed in the L18_worksheet PDF?"_
*   _"Can you summarize the contents of my 'L18_worksheet' PDF?"_

#### 📈 Crypto & Stock Price

![Crytpo/Stock tool](./images/crptyo%20and%20stock%20tool.PNG)

*   _"What is the latest price of Tesla stock?"_
*   _"How is Ethereum performing today?"_

#### 📊 Top Gainers & Losers

![Top Gainers Tool](./images/top%20gainers%20tool.PNG)

*   _"Who are the top gainers and losers in the stock market today?"_
*   _"Can you tell me the top 5 gainers only?"_

#### 📰 News & Sentiment

![News Tool](./images/news%20tool.PNG)

*   _"Give me recent news headlines about Nvidia."_
*   _"What's the market sentiment on Nvidia stock?"_

#### 🌦️ Weather

![Weather Tool](./images/weather%20tool.PNG)

*   _"What's the weather like in Sacramento right now?"_
*   _"Can you put that into Fahrenheit?"_


## 📝 Notes Feature

You can create, view, and delete notes that are tied to your user account. This makes it easy to track and save key information from your chats or personal input.

#### Example Screenshots

✅ **Creating a Note**
![Creating a Note](./images/note%20creating%20proof.PNG)

📋 **Notes Saved with Timestamp**
![Saved Note With Timestamp](./images/notes%20example.PNG)

🧾 **Example Note**
![Example Note](./images/notes%20created.PNG)

## API Reference

The following are the main API endpoints provided by the backend:

| Method | Endpoint | Description | Auth Required |
|---|---|---|:---:|
| `POST` | `/api/register/` | Create a new user. | |
| `POST` | `/api/token/` | Obtain a new JWT access and refresh token. | |
| `POST` | `/api/token/refresh/` | Refresh a JWT access token. | |
| `GET` | `/api/notes/` | Get a list of the current user's notes. | ✅ |
| `POST` | `/api/notes/` | Create a new note. | ✅ |
| `DELETE` | `/api/notes/delete/<int:pk>/` | Delete a note by its ID. | ✅ |
| `POST` | `/api/query/` | Send a prompt to the AI agent. | ✅ |
| `GET` | `/api/chat-history/` | Get the user's chat history. | ✅ |
| `DELETE` | `/api/clear-chat-history/` | Clear the user's chat history. | ✅ |
| `POST` | `/api/upload-pdf/` | Upload a PDF file for the AI agent to index. | ✅ |

## 🤝 Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/YourFeature`).
6.  Open a pull request.

## 📜 Credits

Inspired by Tech with Tim's Django AI Projects.

## 🧠 Author

Kaleb — Solo dev building AI assistants

*   **GitHub:** [@kalebcoleman](https://github.com/kalebcoleman)

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.