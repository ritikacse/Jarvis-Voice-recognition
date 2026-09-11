from flask import Flask, render_template, request, jsonify
import datetime

app = Flask(__name__)


def jarvis_response(command):
    command = command.lower().strip()

    # -----------------------------
    # GREETING
    # -----------------------------
    if "hello" in command or "hi" in command:
        return {
            "response": "Hello! I am Jarvis. How can I help you?",
            "action": None
        }

    # -----------------------------
    # TIME
    # -----------------------------
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")

        return {
            "response": f"The current time is {current_time}.",
            "action": None
        }

    # -----------------------------
    # DATE
    # -----------------------------
    elif "date" in command or "today" in command:
        current_date = datetime.datetime.now().strftime(
            "%A, %d %B %Y"
        )

        return {
            "response": f"Today is {current_date}.",
            "action": None
        }

    # -----------------------------
    # YOUTUBE
    # -----------------------------
    elif "open youtube" in command:
        return {
            "response": "Opening YouTube.",
            "action": "youtube"
        }

    # -----------------------------
    # GOOGLE
    # -----------------------------
    elif "open google" in command:
        return {
            "response": "Opening Google.",
            "action": "google"
        }

    # -----------------------------
    # SEARCH
    # -----------------------------
    elif command.startswith("search"):
        search_query = command.replace(
            "search", "", 1
        ).strip()

        if search_query:
            return {
                "response": (
                    f"Searching Google for {search_query}."
                ),
                "action": "search",
                "value": search_query
            }

        return {
            "response": "What would you like me to search for?",
            "action": None
        }

    # -----------------------------
    # HELP
    # -----------------------------
    elif "help" in command or "what can you do" in command:
        return {
            "response": (
                "I can tell the time and date, "
                "open Google and YouTube, "
                "search the web, and respond to basic commands."
            ),
            "action": None
        }

    # -----------------------------
    # ABOUT JARVIS
    # -----------------------------
    elif "who are you" in command:
        return {
            "response": (
                "I am Jarvis, a Python based web voice assistant."
            ),
            "action": None
        }

    # -----------------------------
    # THANK YOU
    # -----------------------------
    elif "thank you" in command or "thanks" in command:
        return {
            "response": "You're welcome!",
            "action": None
        }

    # -----------------------------
    # EXIT
    # -----------------------------
    elif (
        "stop" in command
        or "exit" in command
        or "quit" in command
        or "goodbye" in command
    ):
        return {
            "response": "Goodbye! Have a nice day.",
            "action": "stop"
        }

    # -----------------------------
    # UNKNOWN COMMAND
    # -----------------------------
    else:
        return {
            "response": (
                "Sorry, I don't understand that command. "
                "Say help to see what I can do."
            ),
            "action": None
        }


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# COMMAND API
# ==========================================

@app.route("/command", methods=["POST"])
def command():

    data = request.get_json(silent=True) or {}

    user_command = data.get("command", "")

    result = jarvis_response(user_command)

    return jsonify(result)


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    import os

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
