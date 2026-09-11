# Jarvis-Voice-recognition
A Python-based web voice assistant using Flask and browser speech recognition.
# 🤖 Jarvis Voice Assistant

A Python-based web voice assistant using Flask and browser speech recognition.

## Features

* 🎤 Voice input through the browser
* 🔊 Text-to-speech through the browser
* 🕐 Current time
* 📅 Current date
* 🌐 Open Google
* ▶ Open YouTube
* 🔎 Google search
* ❓ Built-in help commands
* 📱 Responsive web interface
* ☁️ Suitable for cloud deployment
* 🔑 No API key required

## Technologies

* Python
* Flask
* HTML
* CSS
* JavaScript
* Web Speech API

## Project Structure

```text
Jarvis-Voice-Assistant/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── templates/
│   └── index.html
│
└── static/
    └── style.css
```

## Installation

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Open your browser and visit:

```text
http://localhost:5000
```

## Available Commands

You can say:

* "Hello Jarvis"
* "What is the time?"
* "What is today's date?"
* "Open YouTube"
* "Open Google"
* "Search Python tutorial"
* "Who are you?"
* "What can you do?"
* "Help"
* "Goodbye"

## Deployment

For a production deployment using Gunicorn:

```bash
gunicorn app:app
```

Set the service start command to:

```text
gunicorn app:app
```

## Important

This version does not use:

* DeepSeek API
* OpenAI API
* PyAudio
* PyAutoGUI
* pyttsx3
* Desktop GUI
* `DISPLAY`

The microphone and speech output are handled by the user's browser.

## License

This project is intended for educational and personal projects.
