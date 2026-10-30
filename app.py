import gradio as gr
from tutor import tutor

from executor import run_java


# ============================================================
# UI ONLY — Background + Theme
# Backend logic below is unchanged
# ============================================================

CUSTOM_CSS = """
/* ============================================================
   GLOBAL
   ============================================================ */

body {
    margin: 0 !important;
    background: #0b1118 !important;
    color: #e8eef5 !important;
}

.gradio-container {
    max-width: 1400px !important;
    margin: auto !important;
    background: transparent !important;
    position: relative;
    z-index: 2;
}


/* ============================================================
   ABSTRACT BACKGROUND
   ============================================================ */

#background-art {
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    z-index: 0;
    pointer-events: none;
    overflow: hidden;
}

#background-art svg {
    width: 100%;
    height: 100%;
}


/* ============================================================
   HEADER
   ============================================================ */

.app-title {
    color: #edf6ff !important;
    font-size: 38px !important;
    font-weight: 700 !important;
    letter-spacing: -1px;
}

.app-subtitle {
    color: #91a5b8 !important;
    font-size: 16px !important;
    margin-top: -12px;
}


/* ============================================================
   PANELS
   ============================================================ */

.panel {
    background: rgba(18, 28, 39, 0.82) !important;
    border: 1px solid rgba(150, 190, 220, 0.16) !important;
    border-radius: 12px !important;
    padding: 16px !important;
    backdrop-filter: blur(14px);
}


/* ============================================================
   LABELS
   ============================================================ */

label span {
    color: #dce8f2 !important;
    font-weight: 600 !important;
}


/* ============================================================
   INPUTS
   ============================================================ */

textarea,
input {
    background: rgba(17, 27, 38, 0.9) !important;
    color: #e8eef5 !important;
    border: 1px solid #304252 !important;
    border-radius: 8px !important;
}

textarea::placeholder,
input::placeholder {
    color: #718497 !important;
}

textarea:focus,
input:focus {
    border-color: #6fa8c9 !important;
    box-shadow: 0 0 0 1px rgba(111, 168, 201, 0.25) !important;
}


/* ============================================================
   COMPACT CODE EDITOR
   ============================================================ */

.code-container {
    background: #0d1721 !important;
    border: 1px solid #304252 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
    min-height: 0 !important;
    height: 300px !important;
}

.code-container textarea {
    background: #0d1721 !important;
    color: #dceaf3 !important;
    font-family: "Cascadia Code", "Consolas", monospace !important;
    font-size: 14px !important;
    line-height: 1.5 !important;
}


/* ============================================================
   CODE EDITOR HEADER
   ============================================================ */

.code-container > div:first-child {
    background: #142330 !important;
    border-bottom: 1px solid #304252 !important;
}


/* ============================================================
   COMPACT CHAT
   ============================================================ */

.chatbot {
    background: rgba(10, 17, 25, 0.88) !important;
    border: 1px solid rgba(150, 190, 220, 0.18) !important;
    border-radius: 10px !important;
    backdrop-filter: blur(14px);
    height: 620px !important;
    min-height: 0 !important;
}


/* Chat messages */

.chatbot .message {
    border-radius: 8px !important;
}


/* User message */

.chatbot .message.user {
    background: #245d7c !important;
    color: white !important;
}


/* Tutor message */

.chatbot .message.bot {
    background: #182531 !important;
    color: #dce8f2 !important;
    border: 1px solid #304252 !important;
}


/* ============================================================
   PRIMARY BUTTON
   ============================================================ */

.primary-button {
    background: #245d7c !important;
    color: white !important;
    border: 1px solid #397fa3 !important;
    border-radius: 7px !important;
    font-weight: 600 !important;
}

.primary-button:hover {
    background: #2d718f !important;
}


/* ============================================================
   SECONDARY BUTTON
   ============================================================ */

.secondary-button {
    background: rgba(22, 34, 47, 0.9) !important;
    color: #c9e2f2 !important;
    border: 1px solid #3b5366 !important;
    border-radius: 7px !important;
    font-weight: 600 !important;
}

.secondary-button:hover {
    background: #203546 !important;
}


/* ============================================================
   RADIO BUTTONS
   ============================================================ */

input[type="radio"] {
    accent-color: #8ed8f2 !important;
}

/* Selected mode */
label:has(input[type="radio"]:checked) {
    background: #245d7c !important;
    border-color: #6fa8c9 !important;
    color: #ffffff !important;
}

/* Text inside selected mode */
label:has(input[type="radio"]:checked) span {
    color: #ffffff !important;
}

/* Hover */
label:has(input[type="radio"]):hover {
    background: #203746 !important;
}


/* ============================================================
   NEW CHAT
   ============================================================ */

.new-chat {
    background: transparent !important;
    color: #9eb4c5 !important;
    border: 1px solid #34495a !important;
}

.new-chat:hover {
    color: white !important;
    border-color: #6fa8c9 !important;
}

/* ============================================================
   HIDE GRADIO FOOTER
   ============================================================ */

footer {
    display: none !important;
}

.gradio-container {
    max-width: 1400px !important;
    margin: auto !important;
    background: transparent !important;
    position: relative;
    z-index: 2;
}

"""


with gr.Blocks(
    title="DSA Tutor",
    css=CUSTOM_CSS
) as app:

    # ========================================================
    # ABSTRACT BACKGROUND — UI ONLY
    # ========================================================

    gr.HTML("""
    <div id="background-art">
        <svg viewBox="0 0 1600 900"
            preserveAspectRatio="none"
            xmlns="http://www.w3.org/2000/svg">

            <defs>
                <filter id="glow">
                    <feGaussianBlur stdDeviation="35"/>
                </filter>

                <linearGradient id="blueGlow"
                    x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#1688c9"/>
                    <stop offset="50%" stop-color="#2563eb"/>
                    <stop offset="100%" stop-color="#06b6d4"/>
                </linearGradient>
            </defs>

            <path
                d="M-100 650
                C250 300, 450 850, 800 500
                S1250 150, 1700 400"
                fill="none"
                stroke="url(#blueGlow)"
                stroke-width="120"
                opacity="0.18"
                filter="url(#glow)"
            />

            <path
                d="M-100 650
                C250 300, 450 850, 800 500
                S1250 150, 1700 400"
                fill="none"
                stroke="url(#blueGlow)"
                stroke-width="3"
                opacity="0.35"
            />

        </svg>
    </div>
    """)
    


    # ========================================================
    # HEADER
    # ========================================================

    gr.Markdown(
        """
        <div class="app-title">🧠 DSA Tutor</div>

        <div class="app-subtitle">
        Your personal AI tutor for Data Structures & Algorithms
        </div>
        """
    )


    # ========================================================
    # MAIN LAYOUT
    # ========================================================

    with gr.Row():

        # ====================================================
        # LEFT SIDE
        # ====================================================

        with gr.Column(
            scale=1,
            elem_classes="panel"
        ):

            mode = gr.Radio(
                [
                    "Give me a hint",
                    "Explain concept",
                    "Explain my code",
                    "Find my mistake",
                    "Explain approach"
                ],
                label="What do you need?"
            )


            question = gr.Textbox(
                label="Your Question",
                placeholder="Ask your DSA question...",
                lines=4
            )


            code = gr.Textbox(
                label="Java Code",
                lines=10
            )


            with gr.Row():

                run = gr.Button(
                    "▶ Run Code",
                    elem_classes="secondary-button"
                )

                ask = gr.Button(
                    "🤖 Ask Tutor",
                    elem_classes="primary-button"
                )


            output = gr.Textbox(
                label="Program Output",
                lines=5,
                interactive=False
            )


        # ====================================================
        # RIGHT SIDE
        # ====================================================

        with gr.Column(
            scale=1,
            elem_classes="panel"
        ):

            chatbot = gr.Chatbot(
                label="Tutor Conversation",
                height=650,
                elem_classes="chatbot"
            )


    clear = gr.Button(
        "New Chat",
        elem_classes="new-chat"
    )


    # ========================================================
    # STATE
    # ========================================================

    history = gr.State([])


    # ========================================================
    # RUN JAVA CODE
    # ========================================================

    def execute_code(code):
        print("🔥 RUN EVENT FIRED")
        return run_java(code)["output"] if code.strip() else "Please enter Java code."


    # ========================================================
    # ASK TUTOR
    # ========================================================

    def ask_tutor(
        mode,
        question,
        code,
        history,
        program_output
    ):

        print("🔥 ASK TUTOR CLICKED")

        history.append({
            "role": "user",
            "content": question
        })

        history.append({
            "role": "assistant",
            "content": ""
        })

        answer = ""

        for chunk in tutor(
            mode,
            question,
            code,
            history[:-2],
            program_output
        ):

            answer += chunk
            history[-1]["content"] = answer

            yield history, history


    # ========================================================
    # BUTTON EVENTS
    # ========================================================

    ask.click(
        ask_tutor,
        inputs=[
            mode,
            question,
            code,
            history,
            output
        ],
        outputs=[
            chatbot,
            history
        ]
    )


    run.click(
        execute_code,
        inputs=code,
        outputs=output
    )


    clear.click(
        lambda: ([], []),
        outputs=[
            chatbot,
            history
        ]
    )


app.launch(theme=gr.themes.Base())