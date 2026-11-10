import os
import logging
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            return jsonify({"error": "API key not configured"}), 503

        data = request.get_json(silent=True) or {}
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"error": "Please enter a message"}), 400

        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model="gpt-5.5",
            instructions="You are JEFFERSON AI, a helpful AI assistant.",
            input=message
        )

        return jsonify({"reply": response.output_text})

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
