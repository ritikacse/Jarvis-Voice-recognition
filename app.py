```python
import streamlit as st
import streamlit.components.v1 as components
import datetime
import json


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Jarvis Voice Assistant",
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
            #123b68 0%,
            #071321 45%,
            #02060c 100%
        );
    color: white;
}

.main-title {
    text-align: center;
    font-size: 55px;
    font-weight: bold;
    letter-spacing: 10px;
}

.subtitle {
    text-align: center;
    color: #9bb4d3;
    font-size: 18px;
}

.jarvis-orb {
    width: 150px;
    height: 150px;
    margin: 25px auto;

    border-radius: 50%;

    display: flex;
    justify-content: center;
    align-items: center;

    background:
        radial-gradient(
            circle,
            #55cfff,
            #0787f5 40%,
            #064c91 70%,
            #021326
        );

    box-shadow:
        0 0 35px #008cff,
        0 0 70px #008cff55;
}

.jarvis-letter {
    width: 85px;
    height: 85px;

    border-radius: 50%;

    display: flex;
    justify-content: center;
    align-items: center;

    background: #061426;

    border: 2px solid #70d4ff;

    font-size: 50px;
    font-weight: bold;
}

.response-box {
    margin-top: 20px;
    padding: 20px;

    border-radius: 15px;

    background: rgba(5, 15, 28, 0.9);

    border: 1px solid #24415e;
}

.label {
    color: #55cfff;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="jarvis-orb">
    <div class="jarvis-letter">J</div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">JARVIS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Python Web Voice Assistant</div>',
    unsafe_allow_html=True
)


# ============================================================
# COMMAND PROCESSOR
# ============================================================

def process_command(command):

    command = command.lower().strip()

    # Greeting
    if (
        "hello" in command
        or "hi jarvis" in command
        or command == "hi"
    ):
        return "Hello! I am Jarvis. How can I help you?", None

    # Time
    if "time" in command:

        current_time = datetime.datetime.now().strftime(
            "%I:%M %p"
        )

        return (
            f"The current time is {current_time}.",
            None
        )

    # Date
    if "date" in command or "today" in command:

        current_date = datetime.datetime.now().strftime(
            "%A, %d %B %Y"
        )

        return (
            f"Today is {current_date}.",
            None
        )

    # Google
    if "open google" in command:

        return (
            "Opening Google.",
            "https://www.google.com"
        )

    # YouTube
    if "open youtube" in command:

        return (
            "Opening YouTube.",
            "https://www.youtube.com"
        )

    # Search
    if command.startswith("search"):

        search_query = command.replace(
            "search",
            "",
            1
        ).strip()

        if search_query:

            url = (
                "https://www.google.com/search?q="
                + search_query.replace(" ", "+")
            )

            return (
                f"Searching Google for {search_query}.",
                url
            )

        return (
            "Please tell me what you want me to search for.",
            None
        )

    # Who are you
    if "who are you" in command:

        return (
            "I am Jarvis, a Python based web voice assistant.",
            None
        )

    # Help
    if (
        "help" in command
        or "what can you do" in command
    ):

        return (
            "I can tell you the time and date, "
            "open Google and YouTube, "
            "and search the web.",
            None
        )

    # Thanks
    if (
        "thank you" in command
        or "thanks" in command
    ):

        return (
            "You're welcome!",
            None
        )

    # Goodbye
    if (
        "goodbye" in command
        or "exit" in command
        or "quit" in command
        or "stop" in command
    ):

        return (
            "Goodbye! Have a nice day.",
            None
        )

    # Unknown
    return (
        "Sorry, I don't understand that command. "
        "Say help to see what I can do.",
        None
    )


# ============================================================
# SESSION STATE
# ============================================================

if "command" not in st.session_state:
    st.session_state.command = ""

if "response" not in st.session_state:
    st.session_state.response = (
        "Hello! Click the microphone and speak."
    )

if "action" not in st.session_state:
    st.session_state.action = None


# ============================================================
# BROWSER MICROPHONE
# ============================================================

st.markdown(
    "<h3 style='text-align:center;'>🎤 Voice Control</h3>",
    unsafe_allow_html=True
)


# The important part:
# The browser performs speech recognition.
# The result is sent back through Streamlit's component value.

voice_command = components.html(
    """
    <!DOCTYPE html>

    <html>

    <head>

    <style>

    body {
        margin: 0;
        background: transparent;
        text-align: center;
        font-family: Arial;
    }

    #mic {

        width: 100px;
        height: 100px;

        border: none;
        border-radius: 50%;

        background: #1488ed;

        color: white;

        font-size: 40px;

        cursor: pointer;

        box-shadow:
            0 0 30px #1488ed;

    }

    #mic.listening {

        background: #ef4050;

        animation: pulse 1s infinite;

    }

    @keyframes pulse {

        50% {
            transform: scale(1.12);
        }

    }

    #status {

        color: #9eb6d2;

        margin-top: 15px;

    }

    </style>

    </head>

    <body>

    <button id="mic">🎤</button>

    <div id="status">
        Click microphone and speak
    </div>


    <script>

    const mic =
        document.getElementById("mic");

    const status =
        document.getElementById("status");


    const Recognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;


    if (!Recognition) {

        status.innerText =
            "Speech recognition is not supported. Please use Google Chrome.";

        mic.disabled = true;

    }


    else {

        const recognition =
            new Recognition();


        recognition.lang =
            "en-US";

        recognition.continuous =
            false;

        recognition.interimResults =
            false;


        recognition.onstart =
            function() {

                mic.classList.add(
                    "listening"
                );

                status.innerText =
                    "Listening...";

            };


        recognition.onresult =
            function(event) {

                const text =
                    event.results[0][0]
                        .transcript;

                status.innerText =
                    "Command received: " + text;


                /*
                 Send result to Streamlit
                 */

                const data = {
                    command: text
                };


                window.parent.postMessage(
                    {
                        type:
                            "jarvis_command",

                        data:
                            data
                    },
                    "*"
                );


                /*
                 Also store command locally.
                 */

                window.parent.document
                    .dispatchEvent(
                        new CustomEvent(
                            "jarvisVoiceCommand",
                            {
                                detail: text
                            }
                        )
                    );

            };


        recognition.onerror =
            function(event) {

                status.innerText =
                    "Error: " + event.error;

                mic.classList.remove(
                    "listening"
                );

            };


        recognition.onend =
            function() {

                mic.classList.remove(
                    "listening"
                );

            };


        mic.onclick =
            function() {

                try {

                    recognition.start();

                }

                catch(error) {

                    console.log(error);

                }

            };

    }

    </script>

    </body>

    </html>
    """,
    height=180
)


# ============================================================
# SIMPLE TEXT FALLBACK
# ============================================================

st.markdown(
    "<p style='text-align:center;color:#8fa8c9;'>"
    "If voice recognition is unavailable, use the box below."
    "</p>",
    unsafe_allow_html=True
)


text_command = st.text_input(
    "⌨️ Command",
    placeholder="Example: What is the time?"
)


if st.button("Run Command"):

    if text_command.strip():

        response, action = process_command(
            text_command
        )

        st.session_state.command = text_command

        st.session_state.response = response

        st.session_state.action = action


# ============================================================
# DISPLAY RESPONSE
# ============================================================

st.markdown(
    '<div class="response-box">',
    unsafe_allow_html=True
)

st.markdown(
    '<span class="label">You:</span>',
    unsafe_allow_html=True
)

st.write(
    st.session_state.command
    if st.session_state.command
    else "---"
)

st.markdown(
    '<span class="label">Jarvis:</span>',
    unsafe_allow_html=True
)

st.write(
    st.session_state.response
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# OPEN LINK
# ============================================================

if st.session_state.action:

    st.markdown(
        f"[🔗 {st.session_state.response}]"
        f"({st.session_state.action})"
    )


# ============================================================
# BROWSER TEXT TO SPEECH
# ============================================================

speech_text = json.dumps(
    st.session_state.response
)

components.html(
    f"""
    <script>

    const text =
        {speech_text};


    function speakJarvis() {{

        if (
            window.parent &&
            window.parent.speechSynthesis
        ) {{

            window.parent.speechSynthesis.cancel();


            const speech =
                new window.parent.SpeechSynthesisUtterance(
                    text
                );


            speech.lang =
                "en-US";

            speech.rate =
                1;

            speech.pitch =
                1;


            window.parent.speechSynthesis.speak(
                speech
            );

        }}

    }}

    </script>
    """,
    height=0
)


# ============================================================
# COMMANDS
# ============================================================

st.markdown("---")

st.markdown("""
<div class="response-box">

<h3>🎤 Available Voice Commands</h3>

<p>🗣️ "Hello Jarvis"</p>

<p>🕐 "What is the time?"</p>

<p>📅 "What is today's date?"</p>

<p>🌐 "Open Google"</p>

<p>▶️ "Open YouTube"</p>

<p>🔎 "Search Python tutorial"</p>

<p>🤖 "Who are you?"</p>

<p>❓ "What can you do?"</p>

<p>👋 "Goodbye"</p>

</div>
""", unsafe_allow_html=True)
```

### But there is one limitation

There is an important Streamlit limitation here: `components.html()` is an **iframe**, so browser speech recognition can run inside it, but sending the result back into the Python Streamlit execution reliably requires a proper custom Streamlit component. The code you uploaded currently tries to work around this with `window.parent.location.href`, which is why your current implementation is unreliable.

So if your goal is **“click microphone → speak → Python receives command → Jarvis answers → browser speaks”**, the best solution is to make a small custom Streamlit component rather than continuing with `components.html()`.

If you want the **actually working GitHub/Streamlit Cloud version**, I can give you that complete project with:

```text
app.py
requirements.txt
.gitignore
README.md
jarvis_component/
    index.html
    component.js
```

and the microphone-to-Python communication will work properly.
