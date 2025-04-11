# app/backend/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import fitz  # PyMuPDF
from app.llm.model import KnowledgeBaseLLM  # Import the class from the separate file

# Global instance to store the knowledge base LLM.
llm_instance = None

# Define a Pydantic model for the LLM query.
class LLMQuery(BaseModel):
    question: str

# Initialize the FastAPI application.
app = FastAPI(
    title="LLM QA API",
    description="Upload a PDF to build a knowledge base and ask questions based on its content.",
    version="1.0.0"
)

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file, extract its text, and initialize the KnowledgeBaseLLM instance.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")
    
    try:
        # Read the uploaded file as bytes.
        contents = await file.read()
        # Open and extract text from the PDF.
        doc = fitz.open(stream=contents, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        # Create a new KnowledgeBaseLLM instance and store it globally.
        global llm_instance
        llm_instance = KnowledgeBaseLLM(text)
        return {"message": "PDF processed and knowledge base prepared.", "context": llm_instance.context}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {e}")

@app.post("/ask-llm")
async def ask_llm(query: LLMQuery):
    """
    Generate an answer to a question using the knowledge base created from the uploaded PDF.
    """
    if llm_instance is None:
        raise HTTPException(status_code=400, detail="No knowledge base available. Please upload a PDF first.")
    
    try:
        answer = llm_instance.answer_question(query.question)
        return {"response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {e}")
