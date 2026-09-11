import streamlit as st
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder
import datetime
import webbrowser
import urllib.parse
import tempfile
import os


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="JARVIS Voice Assistant",
    page_icon="🤖",
    layout="centered"
)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>
        .stApp {
            background: radial-gradient(
                circle at top,
                #071b33 0%,
                #020812 45%,
                #000000 100%
            );
            color: white;
        }

        .title {
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            color: #00d9ff;
            text-shadow: 0 0 20px #00d9ff;
            margin-top: 20px;
        }

        .subtitle {
            text-align: center;
            color: #8edfff;
            font-size: 18px;
            margin-bottom: 30px;
        }

        .orb {
            width: 180px;
            height: 180px;
            margin: 20px auto;
            border-radius: 50%;
            background: radial-gradient(
                circle,
                #00ffff 0%,
                #0077ff 35%,
                #001f4d 70%,
                #000000 100%
            );
            box-shadow:
                0 0 25px #00d9ff,
                0 0 60px #0077ff,
                0 0 100px #003cff;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% {
                transform: scale(1);
                box-shadow:
                    0 0 25px #00d9ff,
                    0 0 60px #0077ff;
            }

            50% {
                transform: scale(1.08);
                box-shadow:
                    0 0 40px #00d9ff,
                    0 0 90px #0077ff;
            }

            100% {
                transform: scale(1);
                box-shadow:
                    0 0 25px #00d9ff,
                    0 0 60px #0077ff;
            }
        }

        .response-box {
            background: rgba(0, 20, 40, 0.8);
            border: 1px solid #00d9ff;
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0 0 20px rgba(0, 217, 255, 0.3);
        }

        .command-box {
            background: rgba(0, 20, 40, 0.6);
            border-radius: 10px;
            padding: 15px;
            margin-top: 15px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# JARVIS HEADER
# =========================================================

st.markdown(
    '<div class="title">J.A.R.V.I.S</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Just A Rather Very Intelligent System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="orb"></div>',
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "command" not in st.session_state:
    st.session_state.command = ""

if "response" not in st.session_state:
    st.session_state.response = "Hello! I am JARVIS. How can I help you?"

if "action_url" not in st.session_state:
    st.session_state.action_url = None


# =========================================================
# COMMAND PROCESSING
# =========================================================

def process_command(command):

    command = command.lower().strip()

    if not command:
        return "I didn't hear a command.", None

    # Greetings
    if any(word in command for word in [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]):
        return "Hello! How can I help you?", None

    # Time
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}.", None

    # Date
    if "date" in command or "today" in command:
        current_date = datetime.datetime.now().strftime("%A, %d %B %Y")
        return f"Today is {current_date}.", None

    # Open Google
    if "open google" in command:
        return "Opening Google.", "https://www.google.com"

    # Open YouTube
    if "open youtube" in command:
        return "Opening YouTube.", "https://www.youtube.com"

    # Open Gmail
    if "open gmail" in command:
        return "Opening Gmail.", "https://mail.google.com"

    # Search Google
    if command.startswith("search "):
        search_query = command.replace("search ", "", 1).strip()

        if search_query:
            encoded_query = urllib.parse.quote(search_query)
            url = f"https://www.google.com/search?q={encoded_query}"

            return f"Searching Google for {search_query}.", url

    # Search for something
    if "search for " in command:
        search_query = command.split("search for ", 1)[1].strip()

        if search_query:
            encoded_query = urllib.parse.quote(search_query)
            url = f"https://www.google.com/search?q={encoded_query}"

            return f"Searching for {search_query}.", url

    # Who are you?
    if "who are you" in command or "what are you" in command:
        return (
            "I am JARVIS, your virtual voice assistant. "
            "I can understand commands and help you perform simple tasks."
        ), None

    # Help
    if "help" in command:
        return (
            "You can ask me for the time, date, open Google, "
            "open YouTube, search Google, or ask who I am."
        ), None

    # Thanks
    if any(word in command for word in [
        "thank you",
        "thanks"
    ]):
        return "You're welcome!", None

    # Goodbye
    if any(word in command for word in [
        "goodbye",
        "bye",
        "exit",
        "quit"
    ]):
        return "Goodbye! Have a great day.", None

    # Unknown command
    return (
        f"I heard '{command}', but I don't know how to perform "
        "that command yet."
    ), None


# =========================================================
# SPEECH TO TEXT
# =========================================================

def convert_speech_to_text(audio_bytes):

    recognizer = sr.Recognizer()

    temporary_file = None

    try:

        # Create temporary WAV file
        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as temp_audio:

            temp_audio.write(audio_bytes)
            temporary_file = temp_audio.name

        # Read audio file
        with sr.AudioFile(temporary_file) as source:
            audio = recognizer.record(source)

        # Google Speech Recognition
        text = recognizer.recognize_google(audio)

        return text

    except sr.UnknownValueError:
        return None

    except sr.RequestError as error:
        st.error(
            f"Speech recognition service error: {error}"
        )
        return None

    except Exception as error:
        st.error(
            f"Audio processing error: {error}"
        )
        return None

    finally:

        if temporary_file and os.path.exists(temporary_file):
            try:
                os.remove(temporary_file)
            except Exception:
                pass


# =========================================================
# MICROPHONE
# =========================================================

st.subheader("🎤 Voice Command")

st.write(
    "Click the button below, speak your command, "
    "and then stop recording."
)

audio = mic_recorder(
    start_prompt="🎤 Start Speaking",
    stop_prompt="⏹️ Stop Recording",
    just_once=True,
    use_container_width=True,
    format="wav"
)


# =========================================================
# PROCESS MICROPHONE AUDIO
# =========================================================

if audio:

    audio_bytes = audio.get("bytes")

    if audio_bytes:

        with st.spinner("🎧 Listening and processing..."):

            recognized_text = convert_speech_to_text(
                audio_bytes
            )

        if recognized_text:

            st.session_state.command = recognized_text

            response, action_url = process_command(
                recognized_text
            )

            st.session_state.response = response
            st.session_state.action_url = action_url

            st.rerun()

        else:

            st.warning(
                "Sorry, I could not understand your voice. "
                "Please try speaking again."
            )


# =========================================================
# TEXT INPUT FALLBACK
# =========================================================

st.subheader("⌨️ Text Command")

text_command = st.text_input(
    "Type a command:",
    placeholder="Example: What is the time?"
)


if st.button("Send Command", use_container_width=True):

    if text_command.strip():

        st.session_state.command = text_command

        response, action_url = process_command(
            text_command
        )

        st.session_state.response = response
        st.session_state.action_url = action_url

        st.rerun()


# =========================================================
# DISPLAY COMMAND
# =========================================================

if st.session_state.command:

    st.markdown(
        f"""
        <div class="command-box">
            <b>🎤 You said:</b><br>
            {st.session_state.command}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# DISPLAY RESPONSE
# =========================================================

st.markdown(
    f"""
    <div class="response-box">
        <b>🤖 JARVIS:</b><br><br>
        {st.session_state.response}
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# ACTION LINK
# =========================================================

if st.session_state.action_url:

    st.link_button(
        "🔗 Open",
        st.session_state.action_url,
        use_container_width=True
    )


# =========================================================
# TEXT-TO-SPEECH
# =========================================================

if st.session_state.response:

    speech_text = st.session_state.response.replace(
        "'", "\\'"
    )

    st.components.v1.html(
        f"""
        <script>
            const text = '{speech_text}';

            if (window.speechSynthesis) {{
                window.speechSynthesis.cancel();

                const utterance =
                    new SpeechSynthesisUtterance(text);

                utterance.rate = 1.0;
                utterance.pitch = 1.0;
                utterance.volume = 1.0;

                window.speechSynthesis.speak(utterance);
            }}
        </script>
        """,
        height=0
    )


# =========================================================
# AVAILABLE COMMANDS
# =========================================================

with st.expander("📋 Available Commands"):

    st.markdown(
        """
        - **Hello**
        - **What is the time?**
        - **What is today's date?**
        - **Open Google**
        - **Open YouTube**
        - **Open Gmail**
        - **Search Python tutorials**
        - **Search for artificial intelligence**
        - **Who are you?**
        - **Help**
        - **Thank you**
        - **Goodbye**
        """
    )
