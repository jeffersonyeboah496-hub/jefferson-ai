import os
import logging
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            return jsonify({"error": "API key not configured"}), 503

        data = request.get_json(silent=True) or {}
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"error": "Please enter a message"}), 400

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=message,
            config=types.GenerateContentConfig(
                system_instruction="You are JEFFERSON AI, a helpful AI assistant."
            )
        )

        return jsonify({"reply": response.text or "I couldn't generate a response."})

    except Exception:
        logging.exception("AI request failed")
        return jsonify({
            "error": "AI service error. Check server logs."
        }), 500

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
        )
