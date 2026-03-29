from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
import json
import os

load_dotenv()

app = Flask(__name__, static_folder=".")
CORS(app)

API_KEY = os.environ.get("GROQ_API_KEY", "")

if not API_KEY:
    print("ERROR: GROQ_API_KEY not found!")

client = Groq(api_key=API_KEY)


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    news_text = data.get("text", "").strip()

    if not news_text:
        return jsonify({"error": "No text provided"}), 400

    prompt = f"""You are an expert fact-checker and media literacy analyst. Carefully analyze the following news text and determine whether it is real or fake news.

News text: "{news_text}"

Analyze it based on:
- Sensational or emotional language designed to trigger outrage
- Verifiable facts vs unverifiable claims
- Presence of credible sources or citations
- Scientific or logical consistency
- Common misinformation patterns (conspiracy theories, health myths, election fraud claims, etc.)

Respond ONLY with a valid JSON object (no markdown, no backticks, no extra text):
{{
  "verdict": "Real News" or "Fake News" or "Uncertain / Needs Verification",
  "confidence": <integer 0-100>,
  "summary": "<2 sentence explanation of your verdict>",
  "red_flags": ["<flag1>", "<flag2>"],
  "positive_signals": ["<signal1>", "<signal2>"],
  "advice": "<one sentence tip for the reader on how to verify this themselves>"
}}"""

    try:
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.3
        )
        raw = chat_completion.choices[0].message.content.strip()
        clean = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean)
        return jsonify(result)

    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse AI response. Try again."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


port = int(os.environ.get("PORT", 5000))

if __name__ == "__main__":
    print("Starting Fake News Detector server...")
    print(f"Open http://127.0.0.1:{port} in your browser")
    app.run(host="0.0.0.0", port=port)