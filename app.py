import gradio as gr
from tutor import tutor
import os
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
    width: 100% !important;
    max-width: 1400px !important;
    margin: 0 auto !important;
    background: transparent !important;
    position: relative;
    z-index: 2;
}


/* ============================================================
   ABSTRACT BACKGROUND
   ============================================================ */

/* ============================================================
   GRID BACKGROUND
   ============================================================ */

#background-art {
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    z-index: 0;
    pointer-events: none;
    overflow: hidden;

    background-image:
        linear-gradient(
            rgba(0, 0, 0, 0.35),
            rgba(0, 0, 0, 0.35)
        ),
        url("/gradio_api/file=assets/grid-bg.png");

    background-size: cover;
    background-position: center;
    background-repeat: repeat;

    animation: gridMove 25s linear infinite;
}

@keyframes gridMove {
    from {
        background-position: 0 0;
    }

    to {
        background-position: 120px 120px;
    }
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
    background: rgba(8, 8, 10, 0.82) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 14px !important;
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
    background: rgba(8, 8, 10, 0.9) !important;
    color: #eeeeee !important;
    border: 1px solid #383838 !important;
    border-radius: 8px !important;
}

textarea::placeholder,
input::placeholder {
    color: #718497 !important;
}

textarea:focus,
input:focus {
    border-color: #888888 !important;
    box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.12) !important;
}


/* ============================================================
   COMPACT CODE EDITOR
   ============================================================ */

.code-container {
    background: #08080a !important;
    border: 1px solid #383838 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
    min-height: 0 !important;
    height: 300px !important;
}

.code-container textarea {
    background: #08080a !important;
    color: #eeeeee !important;
    font-family: "Cascadia Code", "Consolas", monospace !important;
    min-height: 0 !important;
    height: 300px !important;
}

/* ============================================================
   CODE EDITOR HEADER
   ============================================================ */

.code-container > div:first-child {
    background: #141416 !important;
    border-bottom: 1px solid #383838 !important;
}


/* ============================================================
   COMPACT CHAT
   ============================================================ */

.chatbot {
    background: rgba(5, 5, 7, 0.88) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(14px);
    height: 620px !important;
    min-height: 0 !important;
}

/* Chat messages */

/* Chat messages */

.chatbot .message {
    border-radius: 8px !important;
}

/* User message */
.chatbot .message.user {
    background: #eeeeee !important;
    color: #080808 !important;
    border: none !important;
}

.chatbot .message.user *,
.chatbot .message.user p {
    color: #080808 !important;
    background: transparent !important;
}

/* Tutor message */
.chatbot .message.bot {
    background: #18181a !important;
    color: #dddddd !important;
    border: 1px solid #333333 !important;
}


/* ============================================================
   PRIMARY BUTTON
   ============================================================ */

.primary-button {
    background: #f1f1f1 !important;
    color: #080808 !important;
    border: 1px solid #ffffff !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

.primary-button:hover {
    background: #d8d8d8 !important;
}


/* ============================================================
   SECONDARY BUTTON
   ============================================================ */

.secondary-button {
    background: rgba(20, 20, 22, 0.9) !important;
    color: #eeeeee !important;
    border: 1px solid #444444 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

.secondary-button:hover {
    background: #292929 !important;
    border-color: #777777 !important;
}


/* ============================================================
   RADIO BUTTONS
   ============================================================ */

input[type="radio"] {
    accent-color: #ffffff !important;
}

/* Selected mode */
label:has(input[type="radio"]:checked) {
    background: #eeeeee !important;
    border-color: #ffffff !important;
    color: #080808 !important;
}

label:has(input[type="radio"]:checked) span {
    color: #080808 !important;
}

/* Hover */
label:has(input[type="radio"]):hover {
    background: #292929 !important;
}


/* ============================================================
   NEW CHAT
   ============================================================ */

.new-chat {
    position: static !important;
    display: block !important;

    background: transparent !important;
    color: #cccccc !important;
    border: 1px solid #444444 !important;

    width: 140px !important;
    margin: 12px 0 0 auto !important;
    transform: none !important;
}

.new-chat:hover {
    color: white !important;
    border-color: #777777 !important;
}

/* ============================================================
   HIDE GRADIO FOOTER
   ============================================================ */

footer {
    display: none !important;
}

.gradio-container {
    width: 100% !important;
    max-width: 1400px !important;
    margin: 0 auto !important;
    background: transparent !important;
    position: relative;
    z-index: 2;
}

/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 768px) {

    .gradio-container {
        padding: 12px !important;
    }

    .app-title {
        font-size: 30px !important;
    }

    .app-subtitle {
        font-size: 14px !important;
    }

    .panel {
        padding: 12px !important;
    }

    .code-container {
        height: 250px !important;
    }

    .chatbot {
        height: 500px !important;
    }
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
    <div id="background-art"></div>
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

        with gr.Column(scale=1):

            chatbot = gr.Chatbot(
                label="Tutor Conversation",
                height=650,
                elem_classes="chatbot"
            )

            clear = gr.Button(
                "＋ New Chat",
                elem_classes="new-chat",
                size="sm"
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


app.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860)),
    allowed_paths=[os.path.abspath("assets")]
)