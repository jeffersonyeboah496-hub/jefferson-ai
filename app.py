
import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            return jsonify({"error": "AI API key is not configured yet."}), 503

        data = request.get_json()
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"error": "Please enter a message."}), 400

        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model="gpt-5.5",
            instructions="You are JEFFERSON AI, a helpful and friendly AI assistant.",
            input=message
        )

        return jsonify({"reply": response.output_text})

    except Exception:
        return jsonify({
            "error": "Something went wrong. Please try again."
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
