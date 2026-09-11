import streamlit as st
import datetime
import webbrowser


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Jarvis Voice Assistant",
    page_icon="🤖",
    layout="centered"
)


# ==========================================
# CSS
# ==========================================

st.markdown("""
<style>

body {
    background-color: #050b16;
}

.main {
    background-color: #050b16;
}

.jarvis-title {
    text-align: center;
    font-size: 60px;
    font-weight: bold;
    letter-spacing: 10px;
    color: white;
}

.subtitle {
    text-align: center;
    color: #8fa8c9;
    font-size: 18px;
}

.orb {
    width: 150px;
    height: 150px;
    margin: 30px auto;
    border-radius: 50%;
    background: radial-gradient(
        circle,
        #45c6ff,
        #0879e8 45%,
        #06244a 75%
    );

    box-shadow:
        0 0 50px #0879e8;

    display: flex;
    align-items: center;
    justify-content: center;
}

.orb-text {
    font-size: 60px;
    font-weight: bold;
    color: white;
}

.info {
    padding: 20px;
    border-radius: 15px;
    background-color: #0c1728;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# JARVIS HEADER
# ==========================================

st.markdown(
    '<div class="orb"><div class="orb-text">J</div></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="jarvis-title">JARVIS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Python Voice Assistant</div>',
    unsafe_allow_html=True
)


st.write("")


# ==========================================
# COMMAND INPUT
# ==========================================

command = st.text_input(
    "🎤 Type your command",
    placeholder="Example: What is the time?"
)


# ==========================================
# PROCESS COMMAND
# ==========================================

if st.button("🚀 Ask Jarvis"):

    if not command:

        st.warning(
            "Please enter a command."
        )

    else:

        query = command.lower().strip()


        # ----------------------------------
        # GREETING
        # ----------------------------------

        if (
            "hello" in query
            or "hi" in query
        ):

            response = (
                "Hello! I am Jarvis. "
                "How can I help you?"
            )

            st.success(response)


        # ----------------------------------
        # TIME
        # ----------------------------------

        elif "time" in query:

            current_time = (
                datetime.datetime.now()
                .strftime("%I:%M %p")
            )

            response = (
                f"The current time is "
                f"{current_time}."
            )

            st.success(response)


        # ----------------------------------
        # DATE
        # ----------------------------------

        elif (
            "date" in query
            or "today" in query
        ):

            current_date = (
                datetime.datetime.now()
                .strftime("%A, %d %B %Y")
            )

            response = (
                f"Today is {current_date}."
            )

            st.success(response)


        # ----------------------------------
        # YOUTUBE
        # ----------------------------------

        elif "open youtube" in query:

            response = "Opening YouTube."

            st.success(response)

            st.markdown(
                "[▶ Open YouTube](https://www.youtube.com)"
            )


        # ----------------------------------
        # GOOGLE
        # ----------------------------------

        elif "open google" in query:

            response = "Opening Google."

            st.success(response)

            st.markdown(
                "[🌐 Open Google](https://www.google.com)"
            )


        # ----------------------------------
        # SEARCH
        # ----------------------------------

        elif query.startswith("search"):

            search_query = (
                query
                .replace("search", "", 1)
                .strip()
            )

            if search_query:

                response = (
                    f"Searching Google for "
                    f"{search_query}."
                )

                st.success(response)

                url = (
                    "https://www.google.com/search?q="
                    + search_query.replace(" ", "+")
                )

                st.markdown(
                    f"[🔎 Search Google]({url})"
                )

            else:

                st.warning(
                    "Please tell me what to search for."
                )


        # ----------------------------------
        # WHO ARE YOU
        # ----------------------------------

        elif "who are you" in query:

            response = (
                "I am Jarvis, a Python-based "
                "voice assistant created using Streamlit."
            )

            st.success(response)


        # ----------------------------------
        # HELP
        # ----------------------------------

        elif (
            "help" in query
            or "what can you do" in query
        ):

            st.info("""
I can perform these commands:

• Tell the current time
• Tell today's date
• Open YouTube
• Open Google
• Search Google
• Respond to greetings
• Tell you about Jarvis
""")


        # ----------------------------------
        # EXIT
        # ----------------------------------

        elif (
            "stop" in query
            or "exit" in query
            or "quit" in query
        ):

            st.success(
                "Goodbye! Have a nice day."
            )


        # ----------------------------------
        # UNKNOWN
        # ----------------------------------

        else:

            st.warning(
                "Sorry, I don't understand "
                "that command yet."
            )


# ==========================================
# COMMAND LIST
# ==========================================

st.markdown("---")

st.markdown(
    '<div class="info">'
    '<h3>Available Commands</h3>'
    '<p>🕐 What is the time?</p>'
    '<p>📅 What is today\'s date?</p>'
    '<p>▶ Open YouTube</p>'
    '<p>🌐 Open Google</p>'
    '<p>🔎 Search Python tutorial</p>'
    '<p>👋 Hello Jarvis</p>'
    '<p>❓ Help</p>'
    '</div>',
    unsafe_allow_html=True
)
