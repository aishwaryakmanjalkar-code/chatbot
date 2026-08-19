# KLE BCA Belgaum - Admissions Chatbot 🎓

A simple, local, privacy-friendly admissions chatbot for **KLE Society's BCA College, Belgaum**, built with **Flask**, **Bootstrap** (styling only, no custom CSS/JS frameworks), and **Ollama** running the **llama3.2:latest** model.

The chatbot answers student queries about BCA admissions — eligibility, fees, documents, important dates, facilities, placements, and contact details — using a local knowledge base (`data.json`) that grounds the LLM's responses.

---

## ✨ Features

- 💬 Clean, responsive chat UI built entirely with **Bootstrap 5** (via CDN) — no custom CSS/JS libraries.
- 🧠 Powered by a **locally running LLM** (`llama3.2:latest`) via **Ollama** — no external API keys, no data leaves your machine.
- 📄 Answers are grounded in a structured **`data.json`** knowledge base specific to KLE BCA College admissions.
- ⚡ Lightweight Flask backend with a single `/chat` API endpoint.
- 🔁 Optional `/reload-data` endpoint to refresh the knowledge base without restarting the server.
- ✅ Quick-suggestion buttons for common admission questions.

---

## 📁 Project Structure

```
session3/
│
├── app.py                 # Flask application (backend + Ollama integration)
├── data.json               # Knowledge base: KLE BCA Belgaum admissions data
├── templates/
│   └── index.html          # Chat UI (Bootstrap-only styling)
└── README.md                # This file
```

---

## 🛠️ Prerequisites

1. **Python 3.8+**
2. **Ollama** installed locally → [https://ollama.com/download](https://ollama.com/download)
3. **llama3.2:latest** model pulled in Ollama
4. Python packages: `flask`, `requests`

---

## 🚀 Setup & Installation

### 1. Install Ollama and pull the model

```bash
# Install Ollama (see https://ollama.com/download for your OS)

# Pull the llama3.2 model
ollama pull llama3.2:latest

# Start the Ollama server (if not already running)
ollama serve
```

By default, Ollama listens on `http://localhost:11434`.

### 2. Install Python dependencies

```bash
pip install flask requests
```

### 3. Run the Flask app

```bash
cd session3
python app.py
```

### 4. Open the chatbot

Navigate to:

```
http://127.0.0.1:5000
```

---

## 💡 How It Works

1. **`data.json`** stores structured information about KLE BCA College, Belgaum — courses, eligibility, fees, admission process, documents, dates, facilities, placements, scholarships, and contact info.
2. On startup, **`app.py`** loads `data.json` and embeds it into a **system prompt** that instructs the LLM to answer only using this knowledge base.
3. When a user sends a message from the chat UI (`index.html`), it's POSTed to the Flask **`/chat`** endpoint.
4. Flask forwards the conversation (system prompt + user message) to the **Ollama REST API** (`/api/chat`) using the `llama3.2:latest` model.
5. The model's response is returned as JSON and rendered in the chat window.

```
Browser (Bootstrap UI)
      │  POST /chat { message }
      ▼
Flask app.py
      │  builds system prompt + user message
      ▼
Ollama REST API (localhost:11434/api/chat)
      │  llama3.2:latest generates a grounded reply
      ▼
Flask returns { reply }
      │
      ▼
Chat window updates
```

---

## 🔧 Configuration

You can adjust these settings at the top of `app.py`:

| Variable       | Description                                  | Default                              |
|----------------|-----------------------------------------------|---------------------------------------|
| `OLLAMA_URL`   | Ollama chat API endpoint                     | `http://localhost:11434/api/chat`    |
| `OLLAMA_MODEL` | Ollama model name to use                     | `llama3.2:latest`                    |
| `DATA_FILE`    | Path to the knowledge base JSON file          | `data.json` (same folder as `app.py`)|

---

## 📚 Updating the Knowledge Base

Edit `data.json` to update college information (fees, dates, contact details, FAQs, etc.). Then either:

- Restart the Flask app, **or**
- Call the `/reload-data` endpoint (POST request) to reload the data without restarting:

```bash
curl -X POST http://127.0.0.1:5000/reload-data
```

---

## ⚠️ Notes & Limitations

- This is a **local demo/educational project** — verify that Ollama is running before starting the Flask app, or the chatbot will show a connection warning.
- The chatbot only knows what's inside `data.json`. For anything outside this scope, it will politely direct users to contact the college admissions office.
- Sample contact details (phone/email/website) in `data.json` are placeholders — **replace them with the college's actual official information** before real-world use.
- No conversation history/persistence is implemented — each message is treated independently (can be extended to maintain multi-turn context if needed).

---

## 🧩 Possible Enhancements

- Add multi-turn conversation memory (pass chat history to Ollama).
- Add streaming responses (`"stream": true`) for a typing effect.
- Add a feedback/rating option for each bot response.
- Deploy behind a production WSGI server (e.g., Gunicorn) with authentication if hosted publicly.
- Add multilingual support (English/Kannada) for wider accessibility.

---

## 📜 License

This project is provided for educational/demo purposes. Update college-specific data before any production use.
