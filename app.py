import streamlit as st
import streamlit.components.v1 as components
import datetime
import urllib.parse


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="JARVIS Voice Assistant",
    page_icon="🤖",
    layout="centered"
)


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at top,
            #092b4c 0%,
            #03111f 45%,
            #000000 100%
        );
    color: white;
}

.title {
    text-align: center;
    font-size: 55px;
    font-weight: bold;
    color: #00d9ff;
    text-shadow:
        0 0 10px #00d9ff,
        0 0 30px #008cff,
        0 0 50px #0066ff;
}

.subtitle {
    text-align: center;
    color: #9beaff;
    font-size: 18px;
    margin-bottom: 30px;
}

.orb {
    width: 180px;
    height: 180px;
    margin: 30px auto;
    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            #ffffff 0%,
            #00eaff 15%,
            #0077ff 40%,
            #00244d 70%,
            #000000 100%
        );

    box-shadow:
        0 0 20px #00eaff,
        0 0 50px #008cff,
        0 0 90px #0055ff;

    animation: pulse 2s infinite;
}

@keyframes pulse {

    0% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.08);
    }

    100% {
        transform: scale(1);
    }
}

.box {
    background: rgba(0, 20, 40, 0.8);
    border: 1px solid #00d9ff;
    border-radius: 15px;
    padding: 20px;
    margin-top: 20px;
    box-shadow: 0 0 20px rgba(0, 217, 255, 0.25);
}

.command {
    color: #8eeaff;
    font-size: 18px;
}

.response {
    color: white;
    font-size: 20px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

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


# ============================================================
# SESSION STATE
# ============================================================

if "command" not in st.session_state:
    st.session_state.command = ""

if "response" not in st.session_state:
    st.session_state.response = (
        "Hello! I am JARVIS. How can I help you?"
    )

if "url" not in st.session_state:
    st.session_state.url = ""


# ============================================================
# COMMAND PROCESSOR
# ============================================================

def process_command(command):

    command = command.lower().strip()

    if not command:
        return "I didn't hear anything.", ""

    # ----------------------------------------
    # GREETING
    # ----------------------------------------

    if any(word in command for word in [
        "hello",
        "hi jarvis",
        "hey jarvis",
        "hey"
    ]):
        return "Hello! How can I help you?", ""

    # ----------------------------------------
    # TIME
    # ----------------------------------------

    if "time" in command:

        current_time = datetime.datetime.now().strftime(
            "%I:%M %p"
        )

        return (
            f"The current time is {current_time}.",
            ""
        )

    # ----------------------------------------
    # DATE
    # ----------------------------------------

    if "date" in command or "today" in command:

        current_date = datetime.datetime.now().strftime(
            "%A, %d %B %Y"
        )

        return (
            f"Today is {current_date}.",
            ""
        )

    # ----------------------------------------
    # GOOGLE
    # ----------------------------------------

    if "open google" in command:

        return (
            "Opening Google.",
            "https://www.google.com"
        )

    # ----------------------------------------
    # YOUTUBE
    # ----------------------------------------

    if "open youtube" in command:

        return (
            "Opening YouTube.",
            "https://www.youtube.com"
        )

    # ----------------------------------------
    # GMAIL
    # ----------------------------------------

    if "open gmail" in command:

        return (
            "Opening Gmail.",
            "https://mail.google.com"
        )

    # ----------------------------------------
    # SEARCH
    # ----------------------------------------

    if command.startswith("search "):

        query = command[7:].strip()

        if query:

            encoded = urllib.parse.quote(query)

            url = (
                "https://www.google.com/search?q="
                + encoded
            )

            return (
                f"Searching Google for {query}.",
                url
            )

    # ----------------------------------------
    # SEARCH FOR
    # ----------------------------------------

    if "search for " in command:

        query = command.split(
            "search for ",
            1
        )[1].strip()

        if query:

            encoded = urllib.parse.quote(query)

            url = (
                "https://www.google.com/search?q="
                + encoded
            )

            return (
                f"Searching for {query}.",
                url
            )

    # ----------------------------------------
    # WHO ARE YOU
    # ----------------------------------------

    if (
        "who are you" in command
        or "what are you" in command
    ):

        return (
            "I am JARVIS, your virtual voice assistant.",
            ""
        )

    # ----------------------------------------
    # HELP
    # ----------------------------------------

    if "help" in command:

        return (
            "You can ask me for the time, date, "
            "open Google, open YouTube, open Gmail, "
            "or search Google.",
            ""
        )

    # ----------------------------------------
    # THANK YOU
    # ----------------------------------------

    if (
        "thank you" in command
        or "thanks" in command
    ):

        return (
            "You're welcome!",
            ""
        )

    # ----------------------------------------
    # GOODBYE
    # ----------------------------------------

    if (
        "goodbye" in command
        or command == "bye"
        or "exit" in command
    ):

        return (
            "Goodbye! Have a great day.",
            ""
        )

    # ----------------------------------------
    # UNKNOWN
    # ----------------------------------------

    return (
        f"I heard '{command}', "
        "but I don't know that command yet.",
        ""
    )


# ============================================================
# PROCESS COMMAND FROM BROWSER
# ============================================================

def handle_command(command):

    response, url = process_command(command)

    st.session_state.command = command
    st.session_state.response = response
    st.session_state.url = url


# ============================================================
# TEXT INPUT
# ============================================================

st.subheader("⌨️ Type a command")

text_command = st.text_input(
    "Command",
    placeholder="Example: What is the time?",
    label_visibility="collapsed"
)

if st.button(
    "Send Command",
    use_container_width=True
):

    if text_command.strip():

        handle_command(text_command)

        st.rerun()


# ============================================================
# BROWSER VOICE RECOGNITION
# ============================================================

st.subheader("🎤 Voice Command")

components.html(
    """
    <style>

    body {
        background: transparent;
        font-family: Arial, sans-serif;
        text-align: center;
    }

    #micButton {
        background: #0077ff;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 15px 30px;
        font-size: 18px;
        cursor: pointer;
        box-shadow: 0 0 20px #0077ff;
    }

    #micButton:hover {
        background: #00aaff;
    }

    #status {
        color: #8eeaff;
        margin-top: 15px;
        font-size: 16px;
    }

    </style>

    <button id="micButton">
        🎤 Start Speaking
    </button>

    <div id="status">
        Click the button and speak
    </div>

    <script>

    const button = document.getElementById("micButton");
    const status = document.getElementById("status");

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if (!SpeechRecognition) {

        status.innerHTML =
            "❌ Speech recognition is not supported. " +
            "Please use Google Chrome.";

        button.disabled = true;

    } else {

        const recognition = new SpeechRecognition();

        recognition.lang = "en-US";
        recognition.continuous = false;
        recognition.interimResults = false;

        button.onclick = function() {

            status.innerHTML =
                "🎧 Listening... Speak now";

            button.innerHTML =
                "⏹️ Listening...";

            recognition.start();
        };

        recognition.onresult = function(event) {

            const text =
                event.results[0][0].transcript;

            status.innerHTML =
                "You said: " + text;

            button.innerHTML =
                "🎤 Start Speaking";

            /*
             * Send the recognized command back
             * to the Streamlit parent page.
             */

            window.parent.postMessage(
                {
                    type: "JARVIS_VOICE_COMMAND",
                    command: text
                },
                "*"
            );
        };

        recognition.onerror = function(event) {

            status.innerHTML =
                "❌ Error: " + event.error;

            button.innerHTML =
                "🎤 Start Speaking";
        };

        recognition.onend = function() {

            button.innerHTML =
                "🎤 Start Speaking";
        };
    }

    </script>
    """,
    height=180
)


# ============================================================
# VOICE MESSAGE RECEIVER
# ============================================================

components.html(
    """
    <script>

    window.addEventListener(
        "message",
        function(event) {

            if (
                event.data &&
                event.data.type ===
                "JARVIS_VOICE_COMMAND"
            ) {

                const command =
                    event.data.command;

                /*
                 * Store command temporarily
                 * in browser localStorage.
                 */

                localStorage.setItem(
                    "jarvis_command",
                    command
                );

                /*
                 * Reload Streamlit so Python
                 * can process the command.
                 */

                window.parent.location.reload();
            }

        }
    );

    </script>
    """,
    height=0
)


# ============================================================
# RESPONSE
# ============================================================

st.markdown(
    f"""
    <div class="box">

        <div class="command">
            <b>🎤 You said:</b><br>
            {st.session_state.command or "Waiting for command..."}
        </div>

        <br>

        <div class="response">
            <b>🤖 JARVIS:</b><br><br>
            {st.session_state.response}
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# OPEN LINK
# ============================================================

if st.session_state.url:

    st.link_button(
        "🔗 Open",
        st.session_state.url,
        use_container_width=True
    )


# ============================================================
# TEXT TO SPEECH
# ============================================================

response_text = st.session_state.response

safe_text = (
    response_text
    .replace("\\", "\\\\")
    .replace("'", "\\'")
    .replace("\n", " ")
)

components.html(
    f"""
    <script>

    const responseText = '{safe_text}';

    if (
        responseText &&
        responseText !== "Hello! I am JARVIS. How can I help you?"
    ) {{

        if (window.speechSynthesis) {{

            window.speechSynthesis.cancel();

            const speech =
                new SpeechSynthesisUtterance(
                    responseText
                );

            speech.lang = "en-US";
            speech.rate = 1.0;
            speech.pitch = 1.0;
            speech.volume = 1.0;

            window.speechSynthesis.speak(speech);
        }}
    }}

    </script>
    """,
    height=0
)


# ============================================================
# AVAILABLE COMMANDS
# ============================================================

with st.expander("📋 Available Commands"):

    st.markdown("""
    **Voice commands you can try:**

    - 🎤 Hello Jarvis
    - 🕐 What is the time?
    - 📅 What is today's date?
    - 🌐 Open Google
    - ▶️ Open YouTube
    - 📧 Open Gmail
    - 🔎 Search Python tutorials
    - 🔎 Search for artificial intelligence
    - 🤖 Who are you?
    - ❓ Help
    - 🙏 Thank you
    - 👋 Goodbye
    """)
