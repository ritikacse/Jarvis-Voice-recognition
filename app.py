import streamlit as st
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder
import datetime
import webbrowser


# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="Jarvis Voice Assistant",
    page_icon="🤖",
    layout="centered"
)


# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------

st.markdown("""
<style>

body {
    background-color: #050b18;
}

.main {
    background-color: #050b18;
}

.title {
    text-align: center;
    color: #00e5ff;
    font-size: 45px;
    font-weight: bold;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #aaaaaa;
    font-size: 18px;
    margin-bottom: 30px;
}

.jarvis-orb {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    margin: 20px auto;
    background: radial-gradient(circle, #00e5ff 0%, #0066ff 40%, #00152e 75%);
    box-shadow:
        0 0 20px #00e5ff,
        0 0 50px #0066ff,
        0 0 100px #003cff;
}

.response-box {
    padding: 20px;
    border-radius: 15px;
    background-color: #0c1628;
    border: 1px solid #00e5ff;
    color: white;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)


# -------------------------------------------------
# TITLE
# -------------------------------------------------

st.markdown(
    '<div class="title">🤖 JARVIS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Voice Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="jarvis-orb"></div>',
    unsafe_allow_html=True
)


# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------

if "command" not in st.session_state:
    st.session_state.command = ""

if "response" not in st.session_state:
    st.session_state.response = ""

if "action" not in st.session_state:
    st.session_state.action = ""


# -------------------------------------------------
# COMMAND PROCESSING
# -------------------------------------------------

def process_command(command):

    command = command.lower().strip()

    # Greeting
    if any(word in command for word in [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]):
        return "Hello! I am Jarvis. How can I help you?", ""

    # Time
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}.", ""

    # Date
    elif "date" in command or "today" in command:
        current_date = datetime.datetime.now().strftime("%d %B %Y")
        return f"Today's date is {current_date}.", ""

    # Open Google
    elif "open google" in command:
        return "Opening Google.", "https://www.google.com"

    # Open YouTube
    elif "open youtube" in command:
        return "Opening YouTube.", "https://www.youtube.com"

    # Search Google
    elif command.startswith("search"):
        search_query = command.replace("search", "", 1).strip()

        if search_query:
            url = (
                "https://www.google.com/search?q="
                + search_query.replace(" ", "+")
            )

            return f"Searching Google for {search_query}.", url

        return "Please tell me what you want me to search for.", ""

    # Who are you
    elif "who are you" in command or "what are you" in command:
        return (
            "I am Jarvis, your voice assistant. "
            "I can perform simple commands and answer you with voice."
        ), ""

    # Help
    elif "help" in command:
        return (
            "You can ask me for the time, date, open Google, "
            "open YouTube, or search Google."
        ), ""

    # Thank you
    elif "thank" in command or "thanks" in command:
        return "You're welcome!", ""

    # Goodbye
    elif "goodbye" in command or "bye" in command:
        return "Goodbye! Have a nice day.", ""

    # Unknown command
    else:
        return (
            f"I heard '{command}', but I don't know how to perform that command yet."
        ), ""


# -------------------------------------------------
# SPEECH RECOGNITION
# -------------------------------------------------

def convert_speech_to_text(audio_bytes):

    recognizer = sr.Recognizer()

    try:

        # Save audio temporarily
        with open("voice_command.wav", "wb") as audio_file:
            audio_file.write(audio_bytes)

        # Read WAV file
        with sr.AudioFile("voice_command.wav") as source:

            audio = recognizer.record(source)

        # Convert speech to text
        text = recognizer.recognize_google(audio)

        return text

    except sr.UnknownValueError:

        return ""

    except sr.RequestError:

        return "ERROR_INTERNET"

    except Exception as e:

        st.error(f"Audio error: {e}")

        return ""


# -------------------------------------------------
# MICROPHONE
# -------------------------------------------------

st.markdown("### 🎤 Speak to Jarvis")

audio = mic_recorder(
    start_prompt="🎤 Start Speaking",
    stop_prompt="⏹️ Stop Recording",
    just_once=True,
    use_container_width=True,
    format="wav"
)


# -------------------------------------------------
# PROCESS MICROPHONE INPUT
# -------------------------------------------------

if audio:

    audio_bytes = audio["bytes"]

    with st.spinner("Listening..."):

        recognized_text = convert_speech_to_text(audio_bytes)

    if recognized_text == "ERROR_INTERNET":

        st.error(
            "Speech recognition requires an internet connection."
        )

    elif recognized_text:

        st.session_state.command = recognized_text

        response, action = process_command(
            recognized_text
        )

        st.session_state.response = response
        st.session_state.action = action

        st.rerun()

    else:

        st.warning(
            "I could not understand your voice. Please try again."
        )


# -------------------------------------------------
# SHOW USER COMMAND
# -------------------------------------------------

if st.session_state.command:

    st.markdown("### 🗣️ You said:")

    st.info(
        st.session_state.command
    )


# -------------------------------------------------
# SHOW JARVIS RESPONSE
# -------------------------------------------------

if st.session_state.response:

    st.markdown("### 🤖 Jarvis:")

    st.markdown(
        f"""
        <div class="response-box">
        {st.session_state.response}
        </div>
        """,
        unsafe_allow_html=True
    )


# -------------------------------------------------
# ACTION LINK
# -------------------------------------------------

if st.session_state.action:

    st.markdown(
        f"[🔗 Click here to open]( {st.session_state.action} )"
    )


# -------------------------------------------------
# BROWSER TEXT-TO-SPEECH
# -------------------------------------------------

if st.session_state.response:

    speech_text = st.session_state.response.replace(
        "'", "\\'"
    )

    st.components.v1.html(
        f"""
        <script>

        const text = '{speech_text}';

        if ('speechSynthesis' in window) {{

            window.speechSynthesis.cancel();

            const speech = new SpeechSynthesisUtterance(text);

            speech.lang = 'en-US';
            speech.rate = 1.0;
            speech.pitch = 1.0;
            speech.volume = 1.0;

            window.speechSynthesis.speak(speech);
        }}

        </script>
        """,
        height=0
    )


# -------------------------------------------------
# AVAILABLE COMMANDS
# -------------------------------------------------

with st.expander("📋 Available Voice Commands"):

    st.write("""
    Try saying:

    - **Hello Jarvis**
    - **What is the time?**
    - **What is today's date?**
    - **Open Google**
    - **Open YouTube**
    - **Search Python tutorials**
    - **Who are you?**
    - **Help**
    - **Thank you**
    - **Goodbye**
    """)
