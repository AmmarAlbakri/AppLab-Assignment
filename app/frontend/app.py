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
    payload = {"question":message}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "No response from LLM.")
        else:
            return f"Error: API responded with status code {response.status_code}"
    except Exception as e:
        return f"Exception occurred: {e}"

with gr.Blocks() as demo:
    gr.Markdown("## 📄 PDF Chatbot Example with LLM Integration")
    
    # --- PDF Upload Section ---
    with gr.Row():
        file_input = gr.File(label="Upload PDF", file_types=[".pdf"])
        upload_output = gr.Textbox(label="Upload Status", interactive=False)
    with gr.Row():
        # Initially hidden until a PDF is processed.
        pdf_content_display = gr.Textbox(label="Extracted PDF Content", lines=10, interactive=False, visible=False)
    with gr.Row():
        toggle_btn = gr.Button("Toggle Extracted PDF Content")
    
    # State to track visibility of PDF content.
    visibility_state = gr.State(False)
    
    # When a PDF is uploaded, call the API endpoint to extract text.
    file_input.change(upload_pdf_api, inputs=file_input, outputs=[upload_output, pdf_content_display])
    # Toggle button to manually show/hide the extracted PDF content.
    toggle_btn.click(toggle_visibility, 
                     inputs=[visibility_state, pdf_content_display], 
                     outputs=[pdf_content_display, visibility_state])
    
    # --- LLM Chat Section ---
    with gr.Row():
        llm_message = gr.Textbox(label="Send a Message to LLM", placeholder="Type your message here...")
        llm_send = gr.Button("Send Message")
    with gr.Row():
        llm_response = gr.Textbox(label="LLM Response", lines=5, interactive=False)
    
    # When "Send Message" is clicked, send both the user message and the extracted PDF content to the /ask-llm API.
    llm_send.click(send_to_llm, inputs=[llm_message, pdf_content_display], outputs=llm_response)

demo.launch( server_port=7860, debug=True, share=False)
