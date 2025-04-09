import gradio as gr
import gradio.utils
import requests


def upload_pdf_api(file):
    """
    Sends the uploaded PDF file to the FastAPI /upload-pdf endpoint and returns:
      - a status message.
      - an update for the PDF content textbox (visible with the extracted text) if successful.
    """
    if file is None:
        return "No file uploaded.", gr.update(visible=False, value="")
    
    try:
        # If file is provided as a list (common with Gradio), use the first file.
        if isinstance(file, list):
            file = file[0]
        
        # Handle file passed as a file path (NamedString) or as a file-like object.
        if isinstance(file, (str, gradio.utils.NamedString)):
            file_path = file
            file_to_send = open(file_path, "rb")
        elif hasattr(file, "read"):
            file_to_send = file
        else:
            return f"Uploaded file format not recognized: {type(file)}", gr.update(visible=False, value="")
        
        url = "http://127.0.0.1:8000/upload-pdf"
        files = {"file": ("uploaded.pdf", file_to_send, "application/pdf")}
        response = requests.post(url, files=files)
        
        if response.status_code == 200:
            data = response.json()
            message = data.get("message", "Success")
            text = data.get("text", "")
            # On successful extraction, update the textbox to be visible.
            return message, gr.update(visible=True, value=text)
        else:
            return f"Error: API responded with status code {response.status_code}", gr.update(visible=False, value="")
    except Exception as e:
        return f"Exception occurred: {e}", gr.update(visible=False, value="")

def toggle_visibility(visible_state, content):
    """
    Toggles the visibility of the extracted PDF content textbox.
    """
    new_visible = not visible_state
    return gr.update(visible=new_visible, value=content), new_visible

def send_to_llm(message, pdf_content):
    """
    Sends the user message and the extracted PDF content to the FastAPI /ask-llm endpoint.
    For now, the endpoint returns a simulated LLM response.
    """
    if not message:
        return "Please enter a message."
    
    url = "http://127.0.0.1:8000/ask-llm"
    payload = {"pdf_content": pdf_content, "message": message}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "No response from LLM.")
        else:
            return f"Error: API responded with status code {response.status_code}"
    except Exception as e:
        return f"Exception occurred: {e}"

with gr.Blocks(theme=gr.themes.Soft(), css=".gradio-container { max-width: 1200px; margin: 0 auto; padding: 20px; }") as demo:
    gr.Markdown("""
    # 📚 PDF Chat Assistant
    
    Upload a PDF and chat with an AI about its contents! 
    """)
    
    with gr.Column(elem_classes=["main-container"]):
        # --- PDF Upload Section ---
        with gr.Row(elem_classes=["upload-section"]):
            with gr.Column(scale=2):
                file_input = gr.File(
                    label="Drop your PDF here",
                    file_types=[".pdf"],
                    interactive=True
                )
            with gr.Column(scale=1):
                upload_output = gr.Textbox(
                    label="Status",
                    interactive=False,
                    placeholder="Upload status will appear here..."
                )
        
        # --- Chat Interface ---
        with gr.Row(elem_classes=["chat-section"]):
            with gr.Column(scale=2):
                chat_interface = gr.Chatbot(
                    label="Chat with your PDF",
                    height=400,
                    elem_classes=["chat-window"]
                )
                with gr.Row():
                    message_input = gr.Textbox(
                        label="Type your message",
                        placeholder="Ask anything about your PDF...",
                        lines=2,
                        scale=4
                    )
                    send_button = gr.Button("Send", variant="primary", scale=1)
        
        # --- PDF Content Section (Hidden by default) ---
        with gr.Row(elem_classes=["pdf-content-section"]):
            with gr.Column(scale=2):
                pdf_content_display = gr.Textbox(
                    label="PDF Content",
                    lines=10,
                    interactive=False,
                    visible=False
                )
            with gr.Column(scale=1):
                toggle_btn = gr.Button("👁 Show/Hide PDF Content")
    
    # State to track visibility of PDF content
    visibility_state = gr.State(False)
    
    # Event handlers
    file_input.change(
        upload_pdf_api,
        inputs=file_input,
        outputs=[upload_output, pdf_content_display]
    )
    
    toggle_btn.click(
        toggle_visibility,
        inputs=[visibility_state, pdf_content_display],
        outputs=[pdf_content_display, visibility_state]
    )
    
    def chat_with_pdf(message, chat_history, pdf_content):
        if not message:
            return chat_history
        response = send_to_llm(message, pdf_content)
        chat_history.append((message, response))
        return chat_history
    
    send_button.click(
        chat_with_pdf,
        inputs=[message_input, chat_interface, pdf_content_display],
        outputs=[chat_interface]
    ).then(
        lambda: "",
        None,
        [message_input]
    )

demo.launch()