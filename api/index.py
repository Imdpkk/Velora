import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from api.chatbot import chatbot
from config.constants import WELCOME_MESSAGE

# ==========================================
# Load Environment Variables
# ==========================================

load_dotenv()

# ==========================================
# Flask App
# ==========================================

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

# ==========================================
# Home
# ==========================================

@app.route("/")
def home():
    return render_template(
        "index.html",
        welcome_message=WELCOME_MESSAGE
    )

# ==========================================
# Chat API
# ==========================================

@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "response": "Invalid request."
            }), 400

        message = data.get("message", "").strip()

        if not message:

            return jsonify({
                "success": False,
                "response": "Please enter a message."
            })

        reply = chatbot.generate_response(message)

        return jsonify({
            "success": True,
            "response": reply
        })

    except Exception as e:

        print("SERVER ERROR:", e)

        return jsonify({
            "success": False,
            "response": "Something went wrong. Please try again."
        }), 500

# ==========================================
# Health Check
# ==========================================

@app.route("/health")
def health():

    return jsonify({
        "status": "running",
        "service": "Velora AI",
        "version": "2.0"
    })

# ==========================================
# Start Server
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )