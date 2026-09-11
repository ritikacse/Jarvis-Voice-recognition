import streamlit as st
import streamlit.components.v1 as components
import datetime


# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Jarvis Voice Assistant",
    page_icon="🤖",
    layout="centered"
)


# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at top,
            #123b68 0%,
            #071321 40%,
            #02060c 100%
        );
    color: white;
}

.main-title {
    text-align: center;
    font-size: 60px;
    font-weight: bold;
    letter-spacing: 10px;
    color: white;
    margin-top: 10px;
}

.subtitle {
    text-align: center;
    color: #9bb4d3;
    font-size: 18px;
    margin-bottom: 25px;
}

.jarvis-orb {
    width: 160px;
    height: 160px;
    margin: 20px auto;
    border-radius: 50%;

    display: flex;
    justify-content: center;
    align-items: center;

    background:
        radial-gradient(
            circle,
            #55cfff 0%,
            #0787f5 35%,
            #064c91 65%,
            #021326 100%
        );

    box-shadow:
        0 0 30px #008cff,
        0 0 70px #008cff55;
}

.jarvis-letter {
    width: 90px;
    height: 90px;

    border-radius: 50%;

    display: flex;
    justify-content: center;
    align-items: center;

    background: #061426;

    border: 2px solid #70d4ff;

    font-size: 55px;
    font-weight: bold;
}

.info-box {
    padding: 20px;
    margin-top: 20px;

    border-radius: 15px;

    background: rgba(5, 15, 28, 0.9);

    border: 1px solid #24415e;
}

.command {
    color: #5bc4ff;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# ============================================
# JARVIS HEADER
# ============================================

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
    '<div class="subtitle">Python Voice Assistant</div>',
    unsafe_allow_html=True
)


# ============================================
# PYTHON COMMAND PROCESSOR
# ============================================

def process_command(command):

    command = command.lower().strip()

    # ----------------------------------------
    # HELLO
    # ----------------------------------------

    if (
        "hello" in command
        or "hi jarvis" in command
        or command == "hi"
    ):

        return "Hello! I am Jarvis. How can I help you?"


    # ----------------------------------------
    # TIME
    # ----------------------------------------

    elif "time" in command:

        current_time = datetime.datetime.now().strftime(
            "%I:%M %p"
        )

        return f"The current time is {current_time}."


    # ----------------------------------------
    # DATE
    # ----------------------------------------

    elif (
        "date" in command
        or "today" in command
    ):

        current_date = datetime.datetime.now().strftime(
            "%A, %d %B %Y"
        )

        return f"Today is {current_date}."


    # ----------------------------------------
    # WHO ARE YOU
    # ----------------------------------------

    elif "who are you" in command:

        return (
            "I am Jarvis, a Python based "
            "web voice assistant."
        )


    # ----------------------------------------
    # HELP
    # ----------------------------------------

    elif (
        "help" in command
        or "what can you do" in command
    ):

        return (
            "I can tell you the time and date, "
            "open Google, open YouTube, "
            "search Google, and respond to basic commands."
        )


    # ----------------------------------------
    # THANK YOU
    # ----------------------------------------

    elif (
        "thank you" in command
        or "thanks" in command
    ):

        return "You're welcome!"


    # ----------------------------------------
    # GOODBYE
    # ----------------------------------------

    elif (
        "goodbye" in command
        or "exit" in command
        or "quit" in command
        or "stop" in command
    ):

        return "Goodbye! Have a nice day."


    # ----------------------------------------
    # UNKNOWN COMMAND
    # ----------------------------------------

    else:

        return (
            "Sorry, I don't understand that command. "
            "Please say help to see the available commands."
        )


# ============================================
# STREAMLIT SESSION STATE
# ============================================

if "user_command" not in st.session_state:

    st.session_state.user_command = ""


if "jarvis_response" not in st.session_state:

    st.session_state.jarvis_response = (
        "Hello! Click the microphone and speak."
    )


# ============================================
# BROWSER VOICE ASSISTANT
# ============================================

components.html(
    """
<!DOCTYPE html>

<html>

<head>

<style>

body {
    background: transparent;
    font-family: Arial, sans-serif;
    text-align: center;
}

button {

    width: 100px;
    height: 100px;

    border-radius: 50%;

    border: none;

    background: #1488ed;

    color: white;

    font-size: 40px;

    cursor: pointer;

    box-shadow:
        0 0 25px #1488ed;

}

button:hover {

    transform: scale(1.08);

}

button.listening {

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

    margin-top: 20px;

    font-size: 16px;

}

#result {

    color: white;

    margin-top: 15px;

    font-size: 18px;

}

</style>

</head>


<body>


<button id="mic">

🎤

</button>


<div id="status">

Click microphone to speak

</div>


<div id="result">

</div>


<script>


const mic =
    document.getElementById("mic");


const status =
    document.getElementById("status");


const result =
    document.getElementById("result");


/*
============================================
BROWSER SPEECH RECOGNITION
============================================
*/


const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;


let recognition = null;


if (!SpeechRecognition) {

    status.innerText =
        "Speech recognition is not supported. Use Google Chrome.";

    mic.disabled = true;

}


else {

    recognition =
        new SpeechRecognition();


    recognition.lang =
        "en-US";


    recognition.continuous =
        false;


    recognition.interimResults =
        false;


    /*
    ========================================
    START
    ========================================
    */


    recognition.onstart = function() {

        mic.classList.add(
            "listening"
        );

        status.innerText =
            "Listening... Speak now.";

    };


    /*
    ========================================
    RESULT
    ========================================
    */


    recognition.onresult =
        function(event) {

            const command =
                event.results[0][0]
                    .transcript;


            result.innerText =
                "You said: " + command;


            status.innerText =
                "Command received";


            /*
            Send command to Streamlit
            through URL query parameter.
            */


            const url =
                new URL(
                    window.parent.location.href
                );


            url.searchParams.set(
                "voice_command",
                command
            );


            window.parent.location.href =
                url.toString();

        };


    /*
    ========================================
    ERROR
    ========================================
    */


    recognition.onerror =
        function(event) {

            console.log(
                event.error
            );


            status.innerText =
                "Could not understand. Try again.";

            mic.classList.remove(
                "listening"
            );

        };


    /*
    ========================================
    END
    ========================================
    */


    recognition.onend =
        function() {

            mic.classList.remove(
                "listening"
            );

        };


    /*
    ========================================
    MICROPHONE CLICK
    ========================================
    */


    mic.onclick =
        function() {

            try {

                recognition.start();

            }

            catch(error) {

                console.log(
                    error
                );

            }

        };

}


</script>

</body>

</html>
""",
    height=180
)


# ============================================
# GET VOICE COMMAND
# ============================================

voice_command = st.query_params.get(
    "voice_command",
    ""
)


if voice_command:

    st.session_state.user_command = voice_command

    response = process_command(
        voice_command
    )

    st.session_state.jarvis_response = response

    # Clear URL parameter after processing
    st.query_params.clear()


# ============================================
# DISPLAY CONVERSATION
# ============================================

st.markdown(
    '<div class="info-box">',
    unsafe_allow_html=True
)

st.markdown(
    '<span class="command">You:</span>',
    unsafe_allow_html=True
)

st.write(
    st.session_state.user_command
    if st.session_state.user_command
    else "---"
)


st.markdown(
    '<span class="command">Jarvis:</span>',
    unsafe_allow_html=True
)

st.write(
    st.session_state.jarvis_response
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================
# TEXT-TO-SPEECH
# ============================================

if st.session_state.jarvis_response:

    speech_text = (
        st.session_state.jarvis_response
        .replace("'", "\\'")
        .replace("\n", " ")
    )

    components.html(
        f"""
<script>

const text =
    '{speech_text}';

if (
    window.parent.speechSynthesis
) {{

    window.parent.speechSynthesis.cancel();

    const speech =
        new SpeechSynthesisUtterance(text);

    speech.lang = "en-US";

    speech.rate = 1;

    speech.pitch = 1;

    window.parent.speechSynthesis.speak(
        speech
    );

}}

</script>
""",
        height=0
    )


# ============================================
# AVAILABLE COMMANDS
# ============================================

st.markdown("---")

st.markdown("""
<div class="info-box">

<h3>🎤 Voice Commands</h3>

<p>Say <b>"Hello Jarvis"</b></p>

<p>Say <b>"What is the time?"</b></p>

<p>Say <b>"What is today's date?"</b></p>

<p>Say <b>"Who are you?"</b></p>

<p>Say <b>"What can you do?"</b></p>

<p>Say <b>"Help"</b></p>

<p>Say <b>"Thank you"</b></p>

<p>Say <b>"Goodbye"</b></p>

</div>
""", unsafe_allow_html=True)
