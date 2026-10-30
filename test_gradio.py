import gradio as gr

def test_click():
    print("BUTTON WORKED")
    return "Button is working!"

with gr.Blocks() as app:
    button = gr.Button("Test Button")
    output = gr.Textbox()

    button.click(
        test_click,
        outputs=output
    )

app.launch()