"""
KLE BCA Belgaum - Admissions Chatbot
Flask + Ollama (llama3.2:latest)

Prerequisites:
    1. Install Ollama:        https://ollama.com/download
    2. Pull the model:        ollama pull llama3.2:latest
    3. Make sure Ollama is running (it runs as a local service on
       http://localhost:11434 by default; `ollama serve` if needed)
    4. pip install flask requests
    5. python app.py
    6. Open http://127.0.0.1:5000 in your browser
"""

import json
import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2:latest"
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

# ---------------------------------------------------------------------------
# Load college admission data (used as grounding context for the model)
# ---------------------------------------------------------------------------
def load_college_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


COLLEGE_DATA = load_college_data()

SYSTEM_PROMPT = f"""You are the official admissions assistant chatbot for
KLE BCA College, Belagavi (Belgaum), Karnataka. Answer ONLY questions
related to BCA admissions, eligibility, fees, documents, dates, placements
and college facilities, using the reference data below. Be concise, polite,
and helpful. If the answer is not present in the reference data, say you
are not sure and suggest the user contact the college admission office
directly. Do not make up facts that contradict the reference data.

Reference data (JSON):
{json.dumps(COLLEGE_DATA, indent=2)}
"""

# Keep a simple in-memory chat history (per server run) for conversational
# context. For a production app you'd key this by session/user id.
chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html", college_name=COLLEGE_DATA.get("college_name", "KLE BCA College"))


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a question about BCA admissions."}), 400

    chat_history.append({"role": "user", "content": user_message})

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": chat_history,
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()
        result = response.json()
        reply = result.get("message", {}).get("content", "").strip()

        if not reply:
            reply = "Sorry, I couldn't generate a response. Please try again."

        chat_history.append({"role": "assistant", "content": reply})

    except requests.exceptions.ConnectionError:
        reply = ("⚠️ Could not connect to Ollama. Make sure Ollama is running "
                  "locally (ollama serve) and that the 'llama3.2:latest' "
                  "model is pulled (ollama pull llama3.2:latest).")
    except requests.exceptions.RequestException as e:
        reply = f"⚠️ Error communicating with the model: {str(e)}"

    return jsonify({"reply": reply})


@app.route("/reset", methods=["POST"])
def reset():
    """Clear conversation history but keep the system prompt."""
    global chat_history
    chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]
    return jsonify({"status": "reset"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)