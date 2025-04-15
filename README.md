# PDF Chatbot with LLM Integration

This project is a conversational chatbot system that allows users to upload PDF documents, extracts their text content, and then answers questions based on the information contained in those PDFs. It uses a FastAPI backend for processing and a Gradio frontend for a user-friendly web interface. The system leverages an open-source language model (in this version, a lightweight GPT-2 variant, like DistilGPT-2) to generate detailed, human-like responses by using the extracted PDF text as contextual information.

## Features

- **PDF Upload and Processing:**  
  Users can upload PDF files. The system automatically extracts text from the PDFs using PyMuPDF and builds a knowledge base.

- **Question Answering:**  
  Users ask questions via the interface, and the system uses the pre-loaded knowledge base and a lightweight LLM to generate detailed and coherent answers.

- **Human-like Responses:**  
  The chatbot is designed to offer warm, friendly, and detailed responses with examples in a few-shot style prompt, resulting in conversational and engaging answers.

- **Modular Structure:**  
  The LLM logic (including context preparation and answer generation) is encapsulated in its own module, making it easier to update or extend in the future.

- **Easy Deployment:**  
  The project can be run directly from source or containerized using Docker for easy deployment.

## Setup Instructions

### Prerequisites

- **Python 3.8+**  
- Required Python packages:
  - fastapi
  - uvicorn
  - pymupdf
  - transformers
  - torch
  - gradio
  - requests

> **Note:** Optionally, install Docker if you plan to run the application inside a container.

### Installation

1. **Clone the Repository:**
