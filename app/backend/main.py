from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import fitz  # PyMuPDF

app = FastAPI(
    title="PDF Extractor API",
    description="Extract text from PDF files and answer questions with a simulated LLM",
    version="1.0.0"
)

# Model for LLM query
class LLMQuery(BaseModel):
    pdf_content: str
    message: str

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    # Validate content type – only accept PDFs.
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are accepted.")
    
    try:
        # Read the uploaded file as bytes.
        contents = await file.read()
        # Open the PDF from the bytes stream.
        doc = fitz.open(stream=contents, filetype="pdf")
        text = ""
        # Iterate over all pages and extract text.
        for page in doc:
            text += page.get_text()
        return {"message": "PDF processed successfully", "text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {e}")

@app.post("/ask-llm")
async def ask_llm(query: LLMQuery):
    """
    This endpoint simulates sending a message along with PDF content to an LLM.
    For now, it returns a placeholder response that includes the user message.
    """
    # Simulate LLM processing (replace this with real LLM logic later)
    simulated_response = (
        f"Simulated LLM Response: Based on the PDF content provided, "
        f"here is an answer to your question '{query.message}'."
    )
    return {"response": simulated_response}
