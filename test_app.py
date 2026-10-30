import gradio as gr

def execute_code(code):
    print("🔥 EVENT FIRED")
    return "HELLO — EVENT WORKS"

with gr.Blocks() as app:

    code = gr.Textbox(
        label="Java Code",
        lines=10
    )

    run = gr.Button("Run Code")

    output = gr.Textbox(
        label="Program Output"
    )

    run.click(
        execute_code,
        inputs=code,
        outputs=output
    )

app.launch()